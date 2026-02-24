#!/usr/bin/env python3
"""
render_video.py — Render Manim scenes to video files with simplified CLI.

Wraps the Manim CLI to handle quality presets, output format, and file path
management (Manim's default output nesting is deep and unintuitive).

Usage:
    python3 render_video.py scene.py SceneName --quality high --format mp4
    python3 render_video.py scene.py SceneName --quality low --format gif --output /path/to/output.gif
"""

import argparse
import subprocess
import sys
import shutil
from pathlib import Path

QUALITY_MAP = {
    "low":    ("-ql",  "480p15"),
    "medium": ("-qm",  "720p30"),
    "high":   ("-qh",  "1080p60"),
    "4k":     ("-qk",  "2160p60"),
}

FORMAT_MAP = {
    "mp4":  "--format=mp4",
    "gif":  "--format=gif",
    "webm": "--format=webm",
    "png":  "--format=png",   # renders each frame as PNG sequence
}


def find_rendered_file(media_dir: Path, scene_name: str, quality_dir: str, fmt: str) -> Path | None:
    """
    Locate the rendered file in Manim's nested output structure.
    Manim outputs to: media/videos/<script_name>/<quality_dir>/<SceneName>.<ext>
    """
    ext = fmt if fmt != "png" else "mp4"  # png sequence still gets combined

    # Search all video subdirs for the scene
    for video_dir in media_dir.rglob(quality_dir):
        candidate = video_dir / f"{scene_name}.{ext}"
        if candidate.exists():
            return candidate

    # Fallback: search by scene name anywhere under media
    for match in media_dir.rglob(f"{scene_name}.{ext}"):
        return match

    # GIF fallback: manim sometimes puts gifs in a different subdir
    if fmt == "gif":
        for match in media_dir.rglob(f"{scene_name}.gif"):
            return match

    return None


def ensure_manim_installed() -> bool:
    """Check if manim is importable."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import manim; print(manim.__version__)"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print(f"Manim version: {result.stdout.strip()}")
            return True
    except Exception:
        pass
    return False


def main():
    parser = argparse.ArgumentParser(description="Render Manim scene to video")
    parser.add_argument("scene_file", help="Path to the .py file containing the Scene class")
    parser.add_argument("scene_name", help="Name of the Scene class to render")
    parser.add_argument("--quality", choices=QUALITY_MAP.keys(), default="high",
                        help="Render quality preset (default: high)")
    parser.add_argument("--format", dest="fmt", choices=FORMAT_MAP.keys(), default="mp4",
                        help="Output format (default: mp4)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output file path. If not specified, outputs next to scene file.")
    parser.add_argument("--media-dir", type=str, default=None,
                        help="Custom media directory for Manim output")

    args = parser.parse_args()

    scene_path = Path(args.scene_file).resolve()
    if not scene_path.exists():
        print(f"ERROR: Scene file not found: {scene_path}", file=sys.stderr)
        sys.exit(1)

    if not ensure_manim_installed():
        print("ERROR: Manim is not installed. Run: pip install manim --break-system-packages", file=sys.stderr)
        sys.exit(1)

    quality_flag, quality_dir = QUALITY_MAP[args.quality]
    format_flag = FORMAT_MAP[args.fmt]

    # Build manim command
    media_dir = Path(args.media_dir) if args.media_dir else scene_path.parent / "media"

    cmd = [
        sys.executable, "-m", "manim", "render",
        quality_flag,
        format_flag,
        f"--media_dir={media_dir}",
        str(scene_path),
        args.scene_name,
    ]

    print(f"Rendering: {args.scene_name} @ {args.quality} quality ({args.fmt})")
    print(f"Command: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"\nERROR: Manim render failed with exit code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)

    # Find the rendered file
    rendered = find_rendered_file(media_dir, args.scene_name, quality_dir, args.fmt)

    if not rendered:
        print(f"\nWARNING: Could not locate rendered file. Check {media_dir} manually.", file=sys.stderr)
        # List what's there for debugging
        print("Contents of media dir:", file=sys.stderr)
        for p in sorted(media_dir.rglob("*")):
            if p.is_file():
                print(f"  {p} ({p.stat().st_size:,} bytes)", file=sys.stderr)
        sys.exit(1)

    # Copy to output location if specified
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rendered, output_path)
        final_path = output_path
    else:
        final_path = rendered

    size = final_path.stat().st_size
    print(f"\nRendered: {final_path}")
    print(f"  Quality:   {args.quality} ({quality_dir})")
    print(f"  Format:    {args.fmt}")
    print(f"  File size: {size:,} bytes ({size / 1024:.1f} KB)")

    return str(final_path)


if __name__ == "__main__":
    main()
