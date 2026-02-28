"""Shared utilities for YouTube video analysis."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse


def parse_youtube_url(url: str) -> str | None:
    """Extract video ID from any YouTube URL format.

    Supports:
        - youtube.com/watch?v=ID
        - youtu.be/ID
        - youtube.com/shorts/ID
        - youtube.com/embed/ID
        - youtube.com/v/ID
        - youtube.com/live/ID
        - URLs with extra params (timestamps, playlists, etc.)
        - Bare video IDs (11 chars, alphanumeric + - _)

    Args:
        url: YouTube URL or bare video ID.

    Returns:
        Video ID string, or None if unparseable.
    """
    url = url.strip()

    # Bare video ID: exactly 11 chars of [A-Za-z0-9_-]
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url

    parsed = urlparse(url)

    # youtu.be/ID
    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        video_id = parsed.path.lstrip("/").split("/")[0]
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
            return video_id
        return None

    # youtube.com variants
    if parsed.hostname not in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
    ):
        return None

    # /watch?v=ID
    if parsed.path == "/watch":
        params = parse_qs(parsed.query)
        video_ids = params.get("v")
        if video_ids:
            video_id = video_ids[0]
            if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
                return video_id
        return None

    # /shorts/ID, /embed/ID, /v/ID, /live/ID
    path_match = re.match(r"/(?:shorts|embed|v|live)/([A-Za-z0-9_-]{11})", parsed.path)
    if path_match:
        return path_match.group(1)

    return None


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format.

    Args:
        seconds: Time in seconds.

    Returns:
        Formatted timestamp string.
    """
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def sanitize_filename(title: str) -> str:
    """Clean a video title for filesystem use.

    Args:
        title: Raw video title.

    Returns:
        Filesystem-safe filename (no extension).
    """
    # Replace filesystem-unsafe chars with hyphens
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", title)
    # Collapse whitespace and hyphens
    cleaned = re.sub(r"[\s-]+", "-", cleaned)
    # Strip leading/trailing hyphens and dots
    cleaned = cleaned.strip("-.")
    # Truncate to 200 chars to avoid path length issues
    return cleaned[:200] if cleaned else "untitled"


def chunk_transcript(
    transcript: list[dict], chunk_minutes: int = 5
) -> list[dict]:
    """Group transcript segments into N-minute chunks for analysis.

    Args:
        transcript: List of segments with 'start', 'duration', 'text' keys.
        chunk_minutes: Size of each chunk in minutes.

    Returns:
        List of chunk dicts with 'start', 'end', 'text', 'start_formatted',
        'end_formatted' keys.
    """
    if not transcript:
        return []

    chunk_seconds = chunk_minutes * 60
    chunks: list[dict] = []
    current_texts: list[str] = []
    chunk_start = 0.0
    chunk_boundary = chunk_seconds

    for segment in transcript:
        seg_start = segment.get("start", 0.0)
        seg_text = segment.get("text", "").strip()

        if seg_start >= chunk_boundary and current_texts:
            chunks.append({
                "start": chunk_start,
                "end": seg_start,
                "start_formatted": format_timestamp(chunk_start),
                "end_formatted": format_timestamp(seg_start),
                "text": " ".join(current_texts),
            })
            current_texts = []
            chunk_start = seg_start
            chunk_boundary = chunk_start + chunk_seconds

        if seg_text:
            current_texts.append(seg_text)

    # Final chunk
    if current_texts:
        last_seg = transcript[-1]
        end_time = last_seg.get("start", 0.0) + last_seg.get("duration", 0.0)
        chunks.append({
            "start": chunk_start,
            "end": end_time,
            "start_formatted": format_timestamp(chunk_start),
            "end_formatted": format_timestamp(end_time),
            "text": " ".join(current_texts),
        })

    return chunks


def estimate_duration_category(seconds: int) -> str:
    """Classify video duration for analysis depth calibration.

    Args:
        seconds: Video duration in seconds.

    Returns:
        One of: 'short' (<10m), 'medium' (10-30m), 'long' (30-90m), 'extended' (>90m).
    """
    if seconds < 600:
        return "short"
    if seconds < 1800:
        return "medium"
    if seconds < 5400:
        return "long"
    return "extended"
