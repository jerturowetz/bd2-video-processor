#!/usr/bin/env python3
from __future__ import annotations

import base64
import csv
import io
import json
import os
import re
import shutil
import statistics
import time
import urllib.error
import urllib.request
import sys
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import typer


VISION_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_DETECTIONS = "detections.jsonl"
DEFAULT_BOUNDARIES = "turn_boundaries.csv"
DEFAULT_DISCOVER_FRAMES = 40
DEFAULT_REGION_EXPAND_RIGHT = 0.02
DEFAULT_REGION_EXPAND_LEFT = 0.005
DEFAULT_REGION_EXPAND_VERTICAL = 0.005
DEFAULT_LOG_EVERY = 10
FOUND_FRAMES_DIR = "found_frames"
CACHE_ROOT = Path(".cache")
OUTPUT_ROOT = Path("outputs")
INPUTS_ROOT = Path("inputs")
MAX_TITLE_LENGTH = 80
MAX_CHANNEL_LENGTH = 40
DEFAULT_RESUME_BACK = 5
TURN_CONFIRM_FRAMES = 2
TURN_MAX_BACK = 4
TURN_STEP = 2
DETECTION_LOGIC_VERSION = "turn-confirm-v1"

try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
except Exception:  # pragma: no cover - optional dependency
    Console = None
    Table = None
    Text = None


@dataclass
class FrameInfo:
    index: int
    timestamp: float
    path: Path


@dataclass
class Region:
    x: float
    y: float
    w: float
    h: float


def require_dependency(module: str, install_hint: str) -> None:
    """Ensure a dependency is available, raising with install hint if missing."""
    try:
        __import__(module)
    except Exception as exc:  # pragma: no cover - import guard
        raise RuntimeError(f"Missing dependency: {module}. Install with: {install_hint}") from exc


def get_access_token() -> str:
    """Fetch an ADC access token for Vision API."""
    require_dependency("google.auth", "pip install google-auth")
    import google.auth  # type: ignore
    from google.auth.transport.requests import Request  # type: ignore

    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not creds:
        raise RuntimeError("No Application Default Credentials found.")
    creds.refresh(Request())
    if not creds.token:
        raise RuntimeError("Failed to obtain access token.")
    return creds.token


def get_gemini_api_key() -> str | None:
    """Return Gemini API key from environment, if present."""
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def get_gemini_model() -> str:
    """Return Gemini model name from environment or default."""
    return os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL


def gemini_generate_content(image_bytes: bytes, prompt: str, api_key: str, model: str) -> dict[str, Any]:
    """Call Gemini generateContent with an image + prompt."""
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": base64.b64encode(image_bytes).decode("utf-8"),
                        }
                    },
                    {"text": prompt},
                ]
            }
        ]
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{GEMINI_ENDPOINT}/{model}:generateContent",
        data=data,
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def reset_cache_root(use_cache: bool) -> None:
    """Clear .cache at start unless --use-cache is set."""
    if use_cache:
        return
    if CACHE_ROOT.exists():
        shutil.rmtree(CACHE_ROOT)


def load_boundaries(path: Path) -> list[tuple[int, float, int]]:
    """Load turn boundaries from CSV."""
    rows: list[tuple[int, float, int]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                (
                    int(row["turn_number"]),
                    float(row["last_seen_timestamp"]),
                    int(row["frame_index"]),
                )
            )
    return rows


def compute_file_hash(path: Path) -> str:
    """Compute a hash for cache matching."""
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_frame_index_map(frames_csv_path: Path) -> dict[int, Path]:
    """Map frame_index to frame path."""
    mapping: dict[int, Path] = {}
    with frames_csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            mapping[int(row["frame_index"])] = frames_csv_path.parent / row["filename"]
    return mapping


def extract_video_id_from_frames(frames_csv_path: Path) -> str:
    """Infer the video id from a cached frames directory name."""
    name = frames_csv_path.parent.name
    if "-" in name:
        return name.rsplit("-", 1)[0]
    return name


def sanitize_filename_component(value: str, max_length: int) -> str:
    """Sanitize text for safe filenames and truncate to max length."""
    cleaned = []
    for char in value.strip():
        if char.isalnum() or char in {" ", "-", "_"}:
            cleaned.append(char)
        else:
            cleaned.append(" ")
    normalized = " ".join("".join(cleaned).split())
    if not normalized:
        return ""
    return normalized[:max_length].strip()


def load_video_metadata(video_id: str) -> dict[str, Any]:
    """Load yt-dlp metadata for a given video id when available."""
    info_path = INPUTS_ROOT / f"{video_id}.info.json"
    if not info_path.exists():
        return {}
    try:
        return json.loads(info_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_found_frames_prefix(metadata: dict[str, Any]) -> str:
    """Build the filename prefix from metadata with safe truncation."""
    channel = metadata.get("channel") or metadata.get("uploader") or metadata.get(
        "uploader_id"
    )
    title = metadata.get("title")
    channel = sanitize_filename_component(channel or "unknown-channel", MAX_CHANNEL_LENGTH)
    title = sanitize_filename_component(title or "untitled", MAX_TITLE_LENGTH)
    if channel and title:
        return f"{channel} - {title}"
    return channel or title or "untitled"


def build_found_frame_name(prefix: str, frame_path: Path) -> str:
    """Build the output filename for a found frame."""
    return f"{prefix} - {frame_path.stem}{frame_path.suffix}"


def load_existing_detections(path: Path) -> list[dict[str, Any]]:
    """Load JSONL detections, ignoring malformed trailing lines."""
    if not path.exists():
        return []
    detections: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                detections.append(json.loads(line))
            except json.JSONDecodeError:
                break
    return detections


def rebuild_state_from_detections(
    detections: list[dict[str, Any]],
) -> tuple[int | None, float | None, int | None, list[tuple[int, float, int]]]:
    """Rebuild boundary state from prior detections using confirmation rules."""
    current_turn: int | None = None
    last_seen_ts: float | None = None
    last_seen_frame: int | None = None
    boundaries_rows: list[tuple[int, float, int]] = []
    pending_turn: int | None = None
    pending_count = 0

    for result in detections:
        turn_number = result.get("turn_number")
        current_turn, last_seen_ts, last_seen_frame, pending_turn, pending_count = update_turn_state(
            current_turn=current_turn,
            last_seen_ts=last_seen_ts,
            last_seen_frame=last_seen_frame,
            pending_turn=pending_turn,
            pending_count=pending_count,
            turn_number=turn_number,
            timestamp=float(result["timestamp"]),
            frame_index=int(result["frame_index"]),
            boundaries_rows=boundaries_rows,
        )

    return current_turn, last_seen_ts, last_seen_frame, boundaries_rows


def has_turn_label(text: str) -> bool:
    """Return True when OCR text includes a turn label."""
    return "turn" in text.lower()


def allowed_turn_candidates(current_turn: int) -> set[int]:
    """Return valid turn numbers relative to current turn."""
    candidates = {
        current_turn,
        current_turn + TURN_STEP,
        current_turn - TURN_STEP,
        current_turn - TURN_MAX_BACK,
    }
    return {value for value in candidates if value > 0}


def update_turn_state(
    *,
    current_turn: int | None,
    last_seen_ts: float | None,
    last_seen_frame: int | None,
    pending_turn: int | None,
    pending_count: int,
    turn_number: int | None,
    timestamp: float,
    frame_index: int,
    boundaries_rows: list[tuple[int, float, int]],
) -> tuple[int | None, float | None, int | None, int | None, int]:
    """Update turn boundary state with confirmation and rollback constraints."""
    if turn_number is None:
        return current_turn, last_seen_ts, last_seen_frame, pending_turn, pending_count

    if current_turn is None:
        return turn_number, timestamp, frame_index, None, 0

    if turn_number == current_turn:
        return current_turn, timestamp, frame_index, None, 0

    if turn_number not in allowed_turn_candidates(current_turn):
        return current_turn, last_seen_ts, last_seen_frame, None, 0

    if pending_turn == turn_number:
        pending_count += 1
    else:
        pending_turn = turn_number
        pending_count = 1

    if pending_count >= TURN_CONFIRM_FRAMES and last_seen_ts is not None and last_seen_frame is not None:
        boundaries_rows.append((current_turn, last_seen_ts, last_seen_frame))
        return turn_number, timestamp, frame_index, None, 0

    return current_turn, last_seen_ts, last_seen_frame, pending_turn, pending_count


def copy_boundary_frames(
    boundaries_rows: list[tuple[int, float, int]],
    frames_csv_path: Path,
    found_frames_dir: Path,
) -> dict[int, tuple[str | None, str | None, str | None]]:
    """Copy boundary frames plus two previous frames to found_frames directory."""
    if found_frames_dir.exists():
        shutil.rmtree(found_frames_dir)
    found_frames_dir.mkdir(parents=True, exist_ok=True)
    frame_map = build_frame_index_map(frames_csv_path)
    video_id = extract_video_id_from_frames(frames_csv_path)
    metadata = load_video_metadata(video_id)
    prefix = build_found_frames_prefix(metadata)
    summary: dict[int, tuple[str | None, str | None, str | None]] = {}
    for _, _, frame_index in boundaries_rows:
        prev2_path = frame_map.get(frame_index - 2)
        prev1_path = frame_map.get(frame_index - 1)
        frame_path = frame_map.get(frame_index)
        dest_names: dict[Path, str] = {}
        for path in (prev2_path, prev1_path, frame_path):
            if path and path.exists():
                dest_name = build_found_frame_name(prefix, path)
                dest_names[path] = dest_name
                shutil.copy2(path, found_frames_dir / dest_name)
        summary[frame_index] = (
            dest_names.get(prev2_path) if prev2_path else None,
            dest_names.get(prev1_path) if prev1_path else None,
            dest_names.get(frame_path) if frame_path else None,
        )
    return summary


def format_found_frame(name: str | None, found_frames_dir: Path) -> str:
    """Format found frame filename as markdown link for summary output."""
    if not name:
        return "-"
    return f"[{name}]({found_frames_dir / name})"


def format_found_frame_rich(name: str | None, found_frames_dir: Path) -> object:
    """Format found frame filename for Rich tables."""
    if not name or Text is None:
        return name or "-"
    link_path = (found_frames_dir / name).resolve()
    return Text(name, style=f"link file://{link_path}")


def gemini_extract_text(response: dict[str, Any]) -> str:
    """Extract primary text response from Gemini output."""
    candidates = response.get("candidates") or []
    if not candidates:
        return ""
    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    if not parts:
        return ""
    return parts[0].get("text", "")



def crop_image_bytes(path: Path, region: Region) -> bytes:
    """Crop a region from a frame and return PNG bytes."""
    require_dependency("PIL", "pip install pillow")
    from PIL import Image  # type: ignore

    with Image.open(path) as img:
        width, height = img.size
        left = int(region.x * width)
        top = int(region.y * height)
        right = int((region.x + region.w) * width)
        bottom = int((region.y + region.h) * height)
        cropped = img.crop((left, top, right, bottom))
        buffer = io.BytesIO()
        cropped.save(buffer, format="PNG")
        return buffer.getvalue()


def crop_image_bytes_with_size(path: Path, region: Region) -> tuple[bytes, int, int]:
    """Crop a region and return PNG bytes plus cropped width/height."""
    require_dependency("PIL", "pip install pillow")
    from PIL import Image  # type: ignore

    with Image.open(path) as img:
        width, height = img.size
        left = int(region.x * width)
        top = int(region.y * height)
        right = int((region.x + region.w) * width)
        bottom = int((region.y + region.h) * height)
        cropped = img.crop((left, top, right, bottom))
        buffer = io.BytesIO()
        cropped.save(buffer, format="PNG")
        return buffer.getvalue(), cropped.width, cropped.height


def load_image_bytes(path: Path) -> tuple[bytes, int, int]:
    """Load a full frame as PNG bytes and return width/height."""
    require_dependency("PIL", "pip install pillow")
    from PIL import Image  # type: ignore

    with Image.open(path) as img:
        width, height = img.size
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue(), width, height


def post_json(payload: dict[str, Any], token: str) -> dict[str, Any]:
    """POST JSON to Vision API with bearer token."""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        VISION_ENDPOINT,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc




def vision_text_detect(image_bytes: bytes, token: str) -> dict[str, Any]:
    """Call Vision OCR on provided image bytes."""
    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(image_bytes).decode("utf-8")},
                "features": [{"type": "TEXT_DETECTION", "maxResults": 5}],
            }
        ]
    }
    return post_json(payload, token)


def extract_text(response: dict[str, Any]) -> str:
    """Extract full OCR text from Vision response."""
    responses = response.get("responses") or []
    if not responses:
        return ""
    annotations = responses[0].get("textAnnotations") or []
    if not annotations:
        return ""
    return annotations[0].get("description", "")


def parse_turn_number(text: str) -> int | None:
    """Parse the number following the 'turn' label from OCR text."""
    match = re.search(r"\bturn\b\D+(\d+)", text, re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1))


def parse_region_json(text: str) -> Region | None:
    """Parse Gemini JSON output into a Region."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    if data.get("found") is False:
        return None
    try:
        x = float(data["x"])
        y = float(data["y"])
        w = float(data["w"])
        h = float(data["h"])
    except (KeyError, TypeError, ValueError):
        return None
    return Region(x=x, y=y, w=w, h=h)


def extract_text_boxes(response: dict[str, Any]) -> list[tuple[str, list[dict[str, int]]]]:
    """Extract word-level text boxes from Vision response."""
    responses = response.get("responses") or []
    if not responses:
        return []
    annotations = responses[0].get("textAnnotations") or []
    if len(annotations) <= 1:
        return []
    boxes: list[tuple[str, list[dict[str, int]]]] = []
    for item in annotations[1:]:
        text = item.get("description", "")
        vertices = (item.get("boundingPoly") or {}).get("vertices") or []
        boxes.append((text, vertices))
    return boxes


def vertices_to_region(vertices: list[dict[str, int]], width: int, height: int) -> Region | None:
    """Convert Vision vertices into normalized Region."""
    if not vertices:
        return None
    xs = [v.get("x", 0) for v in vertices]
    ys = [v.get("y", 0) for v in vertices]
    left, right = min(xs), max(xs)
    top, bottom = min(ys), max(ys)
    if width == 0 or height == 0:
        return None
    x = left / width
    y = top / height
    w = (right - left) / width
    h = (bottom - top) / height
    return Region(x=x, y=y, w=w, h=h)


def discover_region(
    frames: Iterable[FrameInfo],
    token: str,
    max_frames: int,
) -> Region:
    """Discover region via Vision OCR on bottom-right grid cell."""
    candidates: list[Region] = []
    grid_region = Region(x=2 / 3, y=2 / 3, w=1 / 3, h=1 / 3)
    processed = 0
    for frame in frames:
        if processed >= max_frames:
            break
        image_bytes, width, height = crop_image_bytes_with_size(frame.path, grid_region)
        response = vision_text_detect(image_bytes, token)

        for text, vertices in extract_text_boxes(response):
            if not re.search(r"\bturn\b", text, re.IGNORECASE):
                continue
            region = vertices_to_region(vertices, width, height)
            if region is None:
                continue
            if region.w > 0.8 or region.h > 0.8:
                continue
            full_region = Region(
                x=grid_region.x + (region.x * grid_region.w),
                y=grid_region.y + (region.y * grid_region.h),
                w=region.w * grid_region.w,
                h=region.h * grid_region.h,
            )
            candidates.append(full_region)

        processed += 1

    if len(candidates) < 2:
        raise RuntimeError("Region discovery failed: not enough matches in sampled frames.")

    xs = statistics.median([c.x for c in candidates])
    ys = statistics.median([c.y for c in candidates])
    ws = statistics.median([c.w for c in candidates])
    hs = statistics.median([c.h for c in candidates])
    return Region(x=xs, y=ys, w=ws, h=hs)


def discover_region_gemini(
    frames: Iterable[FrameInfo],
    max_frames: int,
    api_key: str,
    model: str,
) -> Region:
    """Discover region via Gemini bounding-box responses."""
    prompt = (
        "You are locating a UI button in the bottom-right of the image. "
        "Return ONLY JSON with normalized bounding box for the full button: "
        '{"found": true|false, "x": 0-1, "y": 0-1, "w": 0-1, "h": 0-1}. '
        "x,y is top-left. If not found, return {\"found\": false}."
    )
    candidates: list[Region] = []
    processed = 0
    for frame in frames:
        if processed >= max_frames:
            break
        image_bytes, _, _ = load_image_bytes(frame.path)
        response = gemini_generate_content(image_bytes, prompt, api_key, model)
        text = gemini_extract_text(response)

        region = parse_region_json(text)
        if region is None:
            processed += 1
            continue
        candidates.append(region)
        processed += 1

    if len(candidates) < 2:
        raise RuntimeError("Gemini region discovery failed: not enough matches in sampled frames.")

    xs = statistics.median([c.x for c in candidates])
    ys = statistics.median([c.y for c in candidates])
    ws = statistics.median([c.w for c in candidates])
    hs = statistics.median([c.h for c in candidates])
    return Region(x=xs, y=ys, w=ws, h=hs)


def iter_frames(csv_path: Path) -> Iterable[FrameInfo]:
    """Yield FrameInfo entries from frames.csv."""
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield FrameInfo(
                index=int(row["frame_index"]),
                timestamp=float(row["timestamp_seconds"]),
                path=csv_path.parent / row["filename"],
            )


def resolve_frames_csv_interactive() -> Path:
    """Prompt to select frames.csv under .cache/frames."""
    candidates = list(Path(".cache/frames").glob("**/frames.csv"))
    if not candidates:
        raise FileNotFoundError("No frames.csv found under .cache/frames. Run bd2_extract_frames.py first.")
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if len(candidates) == 1:
        return candidates[0]
    typer.echo("Select a frames.csv to use:")
    for idx, path in enumerate(candidates, start=1):
        display = str(path.parent)
        typer.echo(f"  {idx}) {display}")
    choice = typer.prompt("Enter number", default="1")
    try:
        index = int(choice)
    except ValueError:
        raise RuntimeError("Invalid selection. Enter a number from the list.") from None
    if index < 1 or index > len(candidates):
        raise RuntimeError("Selection out of range.")
    return candidates[index - 1]


def resolve_frames_csv_for_video(video_id: str) -> Path:
    """Resolve frames.csv path for a given video id."""
    candidates = list(Path(".cache/frames").glob(f"{video_id}-*/frames.csv"))
    if not candidates:
        raise FileNotFoundError(
            f"No frames.csv found for video id '{video_id}'. Run bd2_extract_frames.py first."
        )
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if len(candidates) == 1:
        return candidates[0]
    choices = "\n".join(f"- {path.parent}" for path in candidates)
    raise RuntimeError(
        "Multiple frames.csv candidates found for this video id. "
        "Pass --frames-csv explicitly:\n"
        f"{choices}"
    )



def expand_region_right(region: Region, pad: float) -> Region:
    """Expand region to the right by a fractional padding, clamped to [0,1]."""
    w = min(1.0 - region.x, region.w + pad)
    return Region(x=region.x, y=region.y, w=w, h=region.h)


def expand_region_left(region: Region, pad: float) -> Region:
    """Expand region to the left by a fractional padding, clamped to [0,1]."""
    x = max(0.0, region.x - pad)
    w = min(1.0 - x, region.w + pad)
    return Region(x=x, y=region.y, w=w, h=region.h)


def expand_region_vertical(region: Region, pad: float) -> Region:
    """Expand region vertically (top+bottom) by a fractional padding, clamped to [0,1]."""
    y = max(0.0, region.y - pad)
    h = min(1.0 - y, region.h + (2 * pad))
    return Region(x=region.x, y=y, w=region.w, h=h)


def run(
    frames_csv: str | None = typer.Option(
        None,
        "--frames-csv",
        help="Path to frames.csv (overrides --video-id lookup).",
    ),
    video_id: str = typer.Option(
        ...,
        "--video-id",
        help="YouTube video id used to resolve frames.csv (required unless --frames-csv is provided).",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        help="Allow interactive selection when no frames.csv is provided.",
    ),
    use_cache: bool = typer.Option(
        False,
        "--use-cache",
        help="Preserve extracted frames under .cache/frames.",
    ),
    start_index: int = typer.Option(0, "--start-index", help="Start frame index."),
    every: int = typer.Option(1, "--every", help="Process every Nth frame."),
    detections: str = typer.Option(
        str(DEFAULT_DETECTIONS),
        "--detections",
        help="Output JSONL file for detections.",
    ),
    boundaries: str = typer.Option(
        str(DEFAULT_BOUNDARIES),
        "--boundaries",
        help="Output CSV file for turn boundaries.",
    ),
    save_region: bool = typer.Option(
        False,
        "--save-region",
        help="Save cropped region images for processed frames.",
    ),
    region_dir: str = typer.Option(
        ".cache/region",
        "--region-dir",
        help="Directory to write saved region crops.",
    ),
    preview_only: bool = typer.Option(
        False,
        "--preview-only",
        help="Only save region crops and exit before OCR pass.",
    ),
) -> None:
    """CLI entrypoint: discover region then run OCR and boundaries.

    Main OCR pass sends the padded, region-cropped images for analysis.
    Existing detections resume with a small rollback to avoid partial lines.
    """
    reset_cache_root(use_cache)
    if not use_cache and frames_csv is None:
        raise RuntimeError("Cache cleared. Run bd2_extract_frames.py first or pass --use-cache.")
    if frames_csv:
        frames_csv_path = Path(frames_csv)
    elif interactive:
        frames_csv_path = resolve_frames_csv_interactive()
    else:
        frames_csv_path = resolve_frames_csv_for_video(video_id)
    frames_hash = compute_file_hash(frames_csv_path)
    output_dir = OUTPUT_ROOT / frames_csv_path.parent.name
    detections_path = Path(detections)
    boundaries_path = Path(boundaries)
    if detections_path == Path(DEFAULT_DETECTIONS):
        detections_path = output_dir / DEFAULT_DETECTIONS
    if boundaries_path == Path(DEFAULT_BOUNDARIES):
        boundaries_path = output_dir / DEFAULT_BOUNDARIES
    found_frames_dir = output_dir / FOUND_FRAMES_DIR
    detect_meta_path = output_dir / "detect_meta.json"
    cache_ready = detections_path.exists() and boundaries_path.exists() and detect_meta_path.exists()
    if cache_ready:
        try:
            cached_meta = json.loads(detect_meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cached_meta = {}
        cache_ready = (
            cached_meta.get("frames_csv_hash") == frames_hash
            and cached_meta.get("logic_version") == DETECTION_LOGIC_VERSION
        )
        if use_cache and not cache_ready:
            typer.echo("Cached detections/boundaries do not match selected frames; re-running OCR.")
    if use_cache and cache_ready:
        boundaries_rows = load_boundaries(boundaries_path)
        frame_files = copy_boundary_frames(boundaries_rows, frames_csv_path, found_frames_dir)
        if Console and Table:
            console = Console()
            console.print(f"[bold]Detections:[/bold] {detections_path}")
            console.print(f"[bold]Boundaries:[/bold] {boundaries_path}")
            if boundaries_rows:
                table = Table(title="Turn Boundaries", show_header=True, header_style="bold magenta")
                table.add_column("Turn", justify="right")
                table.add_column("Last Seen", justify="right")
                table.add_column("Frame", justify="right")
                table.add_column("Prev-2", justify="left")
                table.add_column("Prev-1", justify="left")
                table.add_column("Curr", justify="left")
                for turn_number, timestamp, frame_index in boundaries_rows:
                    prev2_name, prev1_name, curr_name = frame_files.get(
                        frame_index, (None, None, None)
                    )
                    table.add_row(
                        str(turn_number),
                        f"{timestamp:.1f}s",
                        str(frame_index),
                        format_found_frame_rich(prev2_name, found_frames_dir),
                        format_found_frame_rich(prev1_name, found_frames_dir),
                        format_found_frame_rich(curr_name, found_frames_dir),
                    )
                console.print(table)
        else:
            typer.echo(f"Detections: {detections_path}")
            typer.echo(f"Boundaries: {boundaries_path}")
            if boundaries_rows:
                typer.echo("Turn boundaries:")
                for turn_number, timestamp, frame_index in boundaries_rows:
                    prev2_name, prev1_name, curr_name = frame_files.get(
                        frame_index, (None, None, None)
                    )
                    typer.echo(
                        f"  {turn_number} → {timestamp:.1f}s (frame {frame_index}) "
                        f"[{format_found_frame(prev2_name, found_frames_dir)}, {format_found_frame(prev1_name, found_frames_dir)}, {format_found_frame(curr_name, found_frames_dir)}]"
                    )
        return

    token = get_access_token()

    detections_path.parent.mkdir(parents=True, exist_ok=True)
    boundaries_path.parent.mkdir(parents=True, exist_ok=True)
    api_key = get_gemini_api_key()
    if api_key:
        model = get_gemini_model()
        typer.echo(f"Discovering region with Gemini ({model})...")
        suggested = discover_region_gemini(
            frames=iter_frames(frames_csv_path),
            max_frames=DEFAULT_DISCOVER_FRAMES,
            api_key=api_key,
            model=model,
        )
    else:
        typer.echo("Discovering region with Vision OCR...")
        suggested = discover_region(
            frames=iter_frames(frames_csv_path),
            token=token,
            max_frames=DEFAULT_DISCOVER_FRAMES,
        )
    region_box = Region(
        x=suggested.x,
        y=suggested.y,
        w=suggested.w,
        h=suggested.h,
    )
    typer.echo(
        "Discovered region: "
        f"{region_box.x:.4f},{region_box.y:.4f},{region_box.w:.4f},{region_box.h:.4f}"
    )
    region_box = expand_region_right(region_box, DEFAULT_REGION_EXPAND_RIGHT)
    region_box = expand_region_left(region_box, DEFAULT_REGION_EXPAND_LEFT)
    region_box = expand_region_vertical(region_box, DEFAULT_REGION_EXPAND_VERTICAL)

    current_turn: int | None = None
    last_seen_ts: float | None = None
    last_seen_frame: int | None = None
    boundaries_rows: list[tuple[int, float, int]] = []
    resume_index: int | None = None
    existing: list[dict[str, Any]] = []
    if detections_path.exists():
        existing = load_existing_detections(detections_path)
        if existing:
            if len(existing) > DEFAULT_RESUME_BACK:
                existing = existing[:-DEFAULT_RESUME_BACK]
            else:
                existing = []
            if existing:
                detections_path.parent.mkdir(parents=True, exist_ok=True)
                with detections_path.open("w", encoding="utf-8") as handle:
                    for item in existing:
                        handle.write(json.dumps(item) + "\n")
                (
                    current_turn,
                    last_seen_ts,
                    last_seen_frame,
                    boundaries_rows,
                ) = rebuild_state_from_detections(existing)
                resume_index = int(existing[-1]["frame_index"])
    pending_turn: int | None = None
    pending_count = 0

    total_frames = 0
    for frame in iter_frames(frames_csv_path):
        if frame.index < start_index:
            continue
        if resume_index is not None and frame.index <= resume_index:
            continue
        if (frame.index - start_index) % every != 0:
            continue
        total_frames += 1

    processed = 0
    if resume_index is not None:
        processed = len(existing)
    region_dir_path = Path(region_dir)
    if save_region:
        if region_dir_path.exists():
            shutil.rmtree(region_dir_path)
        region_dir_path.mkdir(parents=True, exist_ok=True)
    file_mode = "a" if processed else "w"
    with detections_path.open(file_mode, encoding="utf-8") as handle:
        for frame in iter_frames(frames_csv_path):
            if frame.index < start_index:
                continue
            if resume_index is not None and frame.index <= resume_index:
                continue
            if (frame.index - start_index) % every != 0:
                continue

            crop_bytes: bytes | None = None
            if save_region:
                crop_bytes = crop_image_bytes(frame.path, region_box)
                region_path = region_dir_path / frame.path.name
                region_path.write_bytes(crop_bytes)

            if preview_only:
                processed += 1
                if processed % DEFAULT_LOG_EVERY == 0 or processed == total_frames:
                    percent = (processed / total_frames * 100) if total_frames else 0
                    sys.stdout.write(
                        f"\rPreviewed {processed}/{total_frames} frames "
                        f"({percent:.1f}%)..."
                    )
                    sys.stdout.flush()
                continue

            start_time = time.time()
            if crop_bytes is None:
                crop_bytes = crop_image_bytes(frame.path, region_box)
            response = vision_text_detect(crop_bytes, token)
            elapsed = time.time() - start_time
            text = extract_text(response)
            candidate_turn = parse_turn_number(text)
            if candidate_turn is not None and (has_turn_label(text) or current_turn is None):
                turn_number = candidate_turn
            else:
                turn_number = None
            result = {
                "frame_index": frame.index,
                "timestamp": frame.timestamp,
                "image": str(frame.path),
                "region": {
                    "x": region_box.x,
                    "y": region_box.y,
                    "w": region_box.w,
                    "h": region_box.h,
                },
                "text": text,
                "turn_number": turn_number,
                "button_present": turn_number is not None,
                "raw_response": response,
                "latency_seconds": round(elapsed, 3),
            }

            handle.write(json.dumps(result) + "\n")

            current_turn, last_seen_ts, last_seen_frame, pending_turn, pending_count = update_turn_state(
                current_turn=current_turn,
                last_seen_ts=last_seen_ts,
                last_seen_frame=last_seen_frame,
                pending_turn=pending_turn,
                pending_count=pending_count,
                turn_number=turn_number,
                timestamp=float(result["timestamp"]),
                frame_index=int(result["frame_index"]),
                boundaries_rows=boundaries_rows,
            )

            processed += 1
            if processed % DEFAULT_LOG_EVERY == 0 or processed == total_frames:
                percent = (processed / total_frames * 100) if total_frames else 0
                sys.stdout.write(
                    f"\rProcessed {processed}/{total_frames} frames "
                    f"({percent:.1f}%)..."
                )
                sys.stdout.flush()

    if current_turn is not None and last_seen_ts is not None and last_seen_frame is not None:
        boundaries_rows.append((current_turn, last_seen_ts, last_seen_frame))

    frame_files = copy_boundary_frames(boundaries_rows, frames_csv_path, found_frames_dir)

    with boundaries_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["turn_number", "last_seen_timestamp", "frame_index"])
        for row in boundaries_rows:
            writer.writerow(row)
    detect_meta_path.write_text(
        json.dumps(
            {
                "frames_csv": str(frames_csv_path),
                "frames_csv_hash": frames_hash,
                "logic_version": DETECTION_LOGIC_VERSION,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    sys.stdout.write("\n")
    typer.echo(f"Processed {processed} frames.")
    if Console and Table:
        console = Console()
        console.print(f"[bold]Detections:[/bold] {detections_path}")
        console.print(f"[bold]Boundaries:[/bold] {boundaries_path}")
        if boundaries_rows:
            table = Table(title="Turn Boundaries", show_header=True, header_style="bold magenta")
            table.add_column("Turn", justify="right")
            table.add_column("Last Seen", justify="right")
            table.add_column("Frame", justify="right")
            table.add_column("Prev-2", justify="left")
            table.add_column("Prev-1", justify="left")
            table.add_column("Curr", justify="left")
            for turn_number, timestamp, frame_index in boundaries_rows:
                prev2_name, prev1_name, curr_name = frame_files.get(
                    frame_index, (None, None, None)
                )
                table.add_row(
                    str(turn_number),
                    f"{timestamp:.1f}s",
                    str(frame_index),
                    format_found_frame_rich(prev2_name, found_frames_dir),
                    format_found_frame_rich(prev1_name, found_frames_dir),
                    format_found_frame_rich(curr_name, found_frames_dir),
                )
            console.print(table)
    else:
        typer.echo(f"Detections: {detections_path}")
        typer.echo(f"Boundaries: {boundaries_path}")
        if boundaries_rows:
            typer.echo("Turn boundaries:")
            for turn_number, timestamp, frame_index in boundaries_rows:
                prev2_name, prev1_name, curr_name = frame_files.get(
                    frame_index, (None, None, None)
                )
                typer.echo(
                    f"  {turn_number} → {timestamp:.1f}s (frame {frame_index}) "
                    f"[{format_found_frame(prev2_name, found_frames_dir)}, {format_found_frame(prev1_name, found_frames_dir)}, {format_found_frame(curr_name, found_frames_dir)}]"
                )


if __name__ == "__main__":
    try:
        typer.run(run)
    except Exception as exc:
        raise typer.Exit(code=1) from exc
