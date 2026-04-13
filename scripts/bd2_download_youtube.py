#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


def require_tool(tool_name: str) -> None:
    if shutil.which(tool_name) is None:
        raise RuntimeError(f"Missing required tool: {tool_name}. Install it and try again.")


def download_youtube_video(url: str, download_dir: Path) -> None:
    require_tool("yt-dlp")
    download_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(download_dir / "%(id)s.%(ext)s")
    output_path_file = download_dir / f".yt_dlp_output_{uuid4().hex}.txt"
    command = [
        "yt-dlp",
        "--progress",
        "--newline",
        "-f",
        "bv*",
        "--write-info-json",
        "-o",
        output_template,
        "--print-to-file",
        "after_move:filepath",
        str(output_path_file),
        url,
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"yt-dlp failed with exit code {exc.returncode}") from exc
    if not output_path_file.exists():
        raise RuntimeError("yt-dlp did not return a downloaded filepath.")
    output_path = Path(output_path_file.read_text(encoding="utf-8").strip()).expanduser()
    output_path_file.unlink(missing_ok=True)
    if not output_path.exists():
        raise RuntimeError(f"Downloaded video not found at {output_path}.")
    print(output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a YouTube video with yt-dlp.")
    parser.add_argument("--youtube-url", help="YouTube URL to download.")
    parser.add_argument("--video-id", help="YouTube video ID to download.")
    parser.add_argument(
        "--download-dir",
        default="inputs",
        help="Directory to store downloaded videos.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.youtube_url and not args.video_id:
        raise RuntimeError("Provide --youtube-url or --video-id.")
    url = args.youtube_url or f"https://www.youtube.com/watch?v={args.video_id}"
    download_youtube_video(url, Path(args.download_dir))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - simple CLI
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
