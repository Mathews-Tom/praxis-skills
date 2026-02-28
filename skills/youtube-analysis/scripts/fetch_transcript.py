"""Fetch YouTube video transcript and metadata.

Standalone CLI tool. Outputs JSON to stdout, status messages to stderr.
Primary: youtube-transcript-api (no API key). Fallback: yt-dlp subtitles.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any

from utils import parse_youtube_url


def _log(msg: str) -> None:
    """Print status message to stderr."""
    print(msg, file=sys.stderr)


def fetch_transcript_api(video_id: str, lang: str) -> tuple[list[dict], str, str]:
    """Fetch transcript via youtube-transcript-api.

    Args:
        video_id: YouTube video ID.
        lang: Preferred language code.

    Returns:
        Tuple of (transcript_segments, language_used, source_name).

    Raises:
        RuntimeError: If transcript unavailable or library fails.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    _log(f"Fetching transcript via youtube-transcript-api (lang={lang})...")

    ytt = YouTubeTranscriptApi()

    # Try direct fetch with requested language first
    try:
        fetched = ytt.fetch(video_id, languages=[lang])
        segments = [
            {"start": s.start, "duration": s.duration, "text": s.text}
            for s in fetched
        ]
        return segments, lang, "youtube-transcript-api"
    except Exception:
        pass

    # Fall back: list available transcripts, pick first available
    try:
        transcript_list = ytt.list(video_id)
        available = list(transcript_list)
        if not available:
            raise RuntimeError("No transcripts available for this video")
        transcript = available[0]
        _log(f"Requested lang '{lang}' unavailable. Using '{transcript.language_code}'")
        fetched = transcript.fetch()
        segments = [
            {"start": s.start, "duration": s.duration, "text": s.text}
            for s in fetched
        ]
        return segments, transcript.language_code, "youtube-transcript-api"
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"No usable transcript found: {exc}") from exc


def fetch_transcript_ytdlp(video_id: str, lang: str) -> tuple[list[dict], str, str]:
    """Fetch transcript via yt-dlp subtitle extraction.

    Args:
        video_id: YouTube video ID.
        lang: Preferred language code.

    Returns:
        Tuple of (transcript_segments, language_used, source_name).

    Raises:
        RuntimeError: If yt-dlp fails or no subtitles found.
    """
    import json as _json
    import tempfile
    from pathlib import Path

    _log("Falling back to yt-dlp for transcript...")
    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--write-auto-sub",
            "--sub-lang", lang,
            "--sub-format", "json3",
            "--skip-download",
            "--output", f"{tmpdir}/%(id)s",
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp subtitle extraction failed: {result.stderr.strip()}")

        # Find the subtitle file
        sub_files = list(Path(tmpdir).glob("*.json3"))
        if not sub_files:
            raise RuntimeError("yt-dlp produced no subtitle files")

        sub_data = _json.loads(sub_files[0].read_text())
        events = sub_data.get("events", [])
        segments = []
        for event in events:
            segs = event.get("segs")
            if not segs:
                continue
            text = "".join(s.get("utf8", "") for s in segs).strip()
            if not text or text == "\n":
                continue
            start_ms = event.get("tStartMs", 0)
            duration_ms = event.get("dDurationMs", 0)
            segments.append({
                "start": start_ms / 1000.0,
                "duration": duration_ms / 1000.0,
                "text": text,
            })

        if not segments:
            raise RuntimeError("yt-dlp subtitle file contained no usable segments")

        # Determine actual language from filename
        actual_lang = lang
        fname = sub_files[0].name
        parts = fname.rsplit(".", 2)
        if len(parts) >= 3:
            actual_lang = parts[-2]

        return segments, actual_lang, "yt-dlp"


def fetch_metadata(video_id: str) -> dict[str, Any]:
    """Extract video metadata via yt-dlp.

    Args:
        video_id: YouTube video ID.

    Returns:
        Dict with title, channel, duration_seconds, upload_date,
        description, view_count, tags.
    """
    _log("Fetching metadata via yt-dlp...")
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = ["yt-dlp", "--dump-json", "--no-download", url]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        _log(f"Metadata fetch failed: {result.stderr.strip()}")
        return {
            "title": "Unknown",
            "channel": "Unknown",
            "duration_seconds": 0,
            "upload_date": "Unknown",
            "description": "",
            "view_count": 0,
            "tags": [],
        }

    data = json.loads(result.stdout)
    upload_date = data.get("upload_date", "")
    if len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

    return {
        "title": data.get("title", "Unknown"),
        "channel": data.get("channel", data.get("uploader", "Unknown")),
        "duration_seconds": data.get("duration", 0),
        "upload_date": upload_date,
        "description": data.get("description", ""),
        "view_count": data.get("view_count", 0),
        "tags": data.get("tags") or [],
    }


def fetch_video(url_or_id: str, lang: str = "en") -> dict[str, Any]:
    """Fetch transcript and metadata for a YouTube video.

    Args:
        url_or_id: YouTube URL or video ID.
        lang: Preferred transcript language.

    Returns:
        Complete video data dict ready for JSON serialization.

    Raises:
        SystemExit: On unrecoverable errors.
    """
    video_id = parse_youtube_url(url_or_id)
    if not video_id:
        _log(f"ERROR: Cannot parse YouTube URL or video ID: {url_or_id}")
        sys.exit(1)

    _log(f"Video ID: {video_id}")

    # Fetch transcript: primary then fallback
    segments: list[dict] = []
    language = lang
    source = ""

    try:
        segments, language, source = fetch_transcript_api(video_id, lang)
    except (RuntimeError, ImportError) as exc:
        _log(f"Primary transcript fetch failed: {exc}")
        try:
            segments, language, source = fetch_transcript_ytdlp(video_id, lang)
        except RuntimeError as exc2:
            _log(f"Fallback transcript fetch failed: {exc2}")
            _log("ERROR: No transcript available for this video")
            sys.exit(2)

    _log(f"Transcript: {len(segments)} segments via {source} (lang={language})")

    # Fetch metadata
    metadata = fetch_metadata(video_id)

    transcript_text = " ".join(seg["text"] for seg in segments)

    return {
        "video_id": video_id,
        "title": metadata["title"],
        "channel": metadata["channel"],
        "duration_seconds": metadata["duration_seconds"],
        "upload_date": metadata["upload_date"],
        "description": metadata["description"],
        "view_count": metadata["view_count"],
        "tags": metadata["tags"],
        "transcript": segments,
        "transcript_text": transcript_text,
        "language": language,
        "source": source,
    }


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch YouTube video transcript and metadata."
    )
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument(
        "--lang",
        default="en",
        help="Preferred transcript language (default: en)",
    )
    args = parser.parse_args()

    data = fetch_video(args.url, args.lang)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
