"""Orchestrator: fetch transcript + metadata, structure output for Claude analysis.

This script handles data acquisition and formatting. The actual concept analysis
is performed by Claude using SKILL.md instructions, not by this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fetch_transcript import fetch_video
from utils import (
    chunk_transcript,
    estimate_duration_category,
    format_timestamp,
    sanitize_filename,
)


def load_template() -> str:
    """Load the output Markdown template.

    Returns:
        Template string with {placeholders}.
    """
    template_path = Path(__file__).parent.parent / "assets" / "output-template.md"
    return template_path.read_text()


def build_scaffold(
    data: dict,
    depth: str,
    video_type: str,
) -> str:
    """Build the Markdown scaffold from video data.

    Populates metadata fields and prepares transcript sections.
    Analysis placeholders remain for Claude to fill.

    Args:
        data: Video data dict from fetch_video().
        depth: Analysis depth (quick, standard, deep).
        video_type: Video type hint (auto, lecture, tutorial, etc.).

    Returns:
        Markdown string with metadata populated and transcript appended.
    """
    template = load_template()
    duration = format_timestamp(data["duration_seconds"])
    video_url = f"https://www.youtube.com/watch?v={data['video_id']}"

    # Populate metadata fields
    output = template.format(
        title=data["title"],
        channel=data["channel"],
        duration=duration,
        upload_date=data["upload_date"],
        video_url=video_url,
        tldr="[TO BE ANALYZED]",
        key_concepts="[TO BE ANALYZED]",
        detailed_analysis="[TO BE ANALYZED]",
        notable_quotes="[TO BE ANALYZED]",
        terms="[TO BE ANALYZED]",
        takeaways="[TO BE ANALYZED]",
        related="[TO BE ANALYZED]",
    )

    # Append analysis context
    duration_cat = estimate_duration_category(data["duration_seconds"])
    sections = [
        output,
        "",
        "---",
        "",
        "## Analysis Context",
        "",
        f"- **Video type**: {video_type}",
        f"- **Analysis depth**: {depth}",
        f"- **Duration category**: {duration_cat}",
        f"- **Transcript language**: {data['language']}",
        f"- **Transcript source**: {data['source']}",
        f"- **Segment count**: {len(data['transcript'])}",
    ]

    if data.get("tags"):
        sections.append(f"- **Tags**: {', '.join(data['tags'][:20])}")

    if data.get("description"):
        desc = data["description"][:500]
        if len(data["description"]) > 500:
            desc += "..."
        sections.extend(["", "### Video Description", "", desc])

    # Chunked transcript for deep analysis
    if depth == "deep":
        chunks = chunk_transcript(data["transcript"], chunk_minutes=5)
        sections.extend(["", "### Transcript (Chunked by 5-minute segments)", ""])
        for chunk in chunks:
            sections.append(
                f"**[{chunk['start_formatted']} - {chunk['end_formatted']}]**"
            )
            sections.append("")
            sections.append(chunk["text"])
            sections.append("")
    else:
        sections.extend(["", "### Full Transcript", "", data["transcript_text"]])

    return "\n".join(sections)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch and structure YouTube video data for analysis."
    )
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument(
        "--output",
        help="Output file path (default: ./{sanitized_title}.md)",
    )
    parser.add_argument(
        "--depth",
        choices=["quick", "standard", "deep"],
        default="standard",
        help="Analysis depth (default: standard)",
    )
    parser.add_argument(
        "--type",
        dest="video_type",
        choices=["auto", "lecture", "tutorial", "interview", "podcast", "tech-talk", "panel"],
        default="auto",
        help="Video type hint (default: auto)",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Preferred transcript language (default: en)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of Markdown scaffold",
    )
    args = parser.parse_args()

    # Fetch video data
    data = fetch_video(args.url, args.lang)

    if args.json:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        print()
        sys.exit(0)

    # Build scaffold
    scaffold = build_scaffold(data, args.depth, args.video_type)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        filename = sanitize_filename(data["title"]) + ".md"
        output_path = Path.cwd() / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(scaffold)
    print(f"Output written to: {output_path}", file=sys.stderr)
    print(str(output_path))


if __name__ == "__main__":
    main()
