#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

VIDEO_EXTENSIONS = [".mp4", ".webm", ".mkv", ".mov"]
DEFAULT_INPUT_DIR = Path("inputs")


@dataclass
class VideoSelection:
    path: Path
    reason: str


def find_default_video(search_dir: Path) -> VideoSelection:
    candidates: list[Path] = []
    for ext in VIDEO_EXTENSIONS:
        candidates.extend(search_dir.glob(f"*{ext}"))

    if not candidates:
        raise FileNotFoundError(
            "No video files found. Provide a path or place an .mp4/.webm/.mkv/.mov in inputs/."
        )

    def score(path: Path) -> tuple[int, int]:
        ext_rank = VIDEO_EXTENSIONS.index(path.suffix.lower())
        size_rank = -path.stat().st_size
        return (ext_rank, size_rank)

    selected = sorted(candidates, key=score)[0]
    reason = "preferred .mp4 format" if selected.suffix.lower() == ".mp4" else "best available format"
    return VideoSelection(path=selected, reason=reason)


def require_tool(tool_name: str) -> None:
    if shutil.which(tool_name) is None:
        raise RuntimeError(f"Missing required tool: {tool_name}. Install it and try again.")


def run_ffmpeg(command: list[str], show_progress: bool = False) -> None:
    if not show_progress:
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"ffmpeg failed with exit code {exc.returncode}") from exc
        return

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to start ffmpeg: {exc}") from exc

    frame = "?"
    out_time = "?"
    if process.stdout:
        for line in process.stdout:
            line = line.strip()
            if line.startswith("frame="):
                frame = line.split("=", 1)[1].strip()
            elif line.startswith("out_time="):
                out_time = line.split("=", 1)[1].strip()
            elif line.startswith("progress="):
                sys.stdout.write(f"\rffmpeg progress: frame {frame} time {out_time}")
                sys.stdout.flush()
                if line.endswith("end"):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"ffmpeg failed with exit code {return_code}")

def choose_video_file(search_dir: Path) -> Path:
    try:
        from tkinter import Tk, filedialog  # type: ignore

        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        filename = filedialog.askopenfilename(
            initialdir=str(search_dir.resolve()),
            title="Select a video file",
            filetypes=[
                ("Video files", "*.mp4 *.webm *.mkv *.mov"),
                ("All files", "*.*"),
            ],
        )
        root.destroy()
        if filename:
            return Path(filename).expanduser().resolve()
    except Exception:
        pass

    candidates: list[Path] = []
    for ext in VIDEO_EXTENSIONS:
        candidates.extend(search_dir.glob(f"*{ext}"))
    candidates = sorted(candidates)
    if not candidates:
        selection = find_default_video(search_dir)
        return selection.path.resolve()

    print("Select a video from inputs/:")
    for idx, path in enumerate(candidates, start=1):
        print(f"  {idx}) {path.name}")
    choice = input("Enter number (or press Enter for 1): ").strip()
    if not choice:
        return candidates[0].resolve()
    try:
        index = int(choice)
    except ValueError:
        raise RuntimeError("Invalid selection. Enter a number from the list.") from None
    if index < 1 or index > len(candidates):
        raise RuntimeError("Selection out of range.")
    return candidates[index - 1].resolve()


def build_cache_key(path: Path) -> str:
    stats = path.stat()
    payload = f"{path.resolve()}|{stats.st_size}|{int(stats.st_mtime)}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:10]




def build_ffmpeg_command(
    input_path: Path,
    output_pattern: Path,
    fps: float,
    start: float | None,
    end: float | None,
    limit: int | None,
    show_progress: bool,
) -> list[str]:
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
    ]
    if show_progress:
        cmd.extend(
            [
                "-progress",
                "pipe:1",
                "-nostats",
            ]
        )
    cmd.extend(
        [
        "-i",
        str(input_path),
        ]
    )

    if start is not None:
        cmd.extend(["-ss", str(start)])
    if end is not None:
        cmd.extend(["-to", str(end)])

    cmd.extend(
        [
            "-vf",
            f"fps={fps}",
            "-vsync",
            "vfr",
        ]
    )

    if limit is not None:
        cmd.extend(["-vframes", str(limit)])

    cmd.append(str(output_pattern))
    return cmd


def write_index_csv(output_dir: Path, fps: float, start: float, csv_path: Path) -> int:
    frames = sorted(output_dir.glob("frame_*.png"))
    with csv_path.open("w", encoding="utf-8") as handle:
        handle.write("frame_index,timestamp_seconds,filename\n")
        for idx, frame in enumerate(frames):
            timestamp = start + (idx / fps)
            handle.write(f"{idx},{timestamp:.3f},{frame.name}\n")
    return len(frames)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sample frames from a local video and emit timestamps.",
    )
    parser.add_argument(
        "video",
        nargs="?",
        help="Path to input video (defaults to best local file in current directory).",
    )
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help="Directory to search and prompt for videos.",
    )
    parser.add_argument("--fps", type=float, default=2.0, help="Frames per second to sample.")
    parser.add_argument("--start", type=float, default=0.0, help="Start time in seconds.")
    parser.add_argument("--end", type=float, help="End time in seconds.")
    parser.add_argument("--limit", type=int, help="Maximum number of frames to extract.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-extract frames even if cached output exists.",
    )
    parser.add_argument(
        "--out-dir",
        default=".cache/frames",
        help="Directory to write extracted frames and index.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_tool("ffmpeg")

    if args.video:
        input_path = Path(args.video).expanduser().resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Video not found: {input_path}")
        selection = VideoSelection(path=input_path, reason="explicit path provided")
    else:
        input_dir = Path(args.input_dir)
        input_dir.mkdir(parents=True, exist_ok=True)
        input_path = choose_video_file(input_dir)
        selection = VideoSelection(path=input_path, reason=f"selected from {input_dir}")

    cache_key = build_cache_key(input_path)
    output_dir = Path(args.out_dir) / f"{input_path.stem}-{cache_key}"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "frames.csv"
    if csv_path.exists() and not args.force:
        print(f"Using cached frames at {output_dir} (pass --force to re-extract).")
        print(f"Index: {csv_path}")
        return 0

    output_pattern = output_dir / "frame_%06d.png"
    print(f"Extracting frames at {args.fps} fps from {input_path.name}...")
    command = build_ffmpeg_command(
        input_path=input_path,
        output_pattern=output_pattern,
        fps=args.fps,
        start=args.start,
        end=args.end,
        limit=args.limit,
        show_progress=True,
    )
    run_ffmpeg(command, show_progress=True)

    frame_count = write_index_csv(
        output_dir=output_dir,
        fps=args.fps,
        start=args.start,
        csv_path=csv_path,
    )

    print(f"Video: {input_path.name} ({selection.reason})")
    print(f"Frames: {frame_count} at {args.fps} fps")
    print(f"Output: {output_dir}")
    print(f"Index: {csv_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - simple CLI
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
