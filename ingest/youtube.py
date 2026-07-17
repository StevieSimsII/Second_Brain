"""Hard-bounded YouTube transcript retrieval.

The transcript library does not expose an overall network deadline. Running it in a
short-lived child process lets the bot stop a DNS or socket stall reliably.
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
from pathlib import Path


def _fetch_direct(video_id: str) -> str:
    # This Mac's resolver can prefer an unreachable IPv6 route for YouTube while
    # IPv4 is healthy. Keep the isolated worker on the reliable address family.
    from urllib3.util import connection as urllib3_connection
    from youtube_transcript_api import YouTubeTranscriptApi

    urllib3_connection.allowed_gai_family = lambda: socket.AF_INET
    api = YouTubeTranscriptApi()
    if hasattr(api, "fetch"):
        transcript = api.fetch(video_id, languages=["en"])
    else:  # Compatibility with pre-1.0 releases.
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

    snippets: list[str] = []
    for item in transcript:
        if isinstance(item, dict):
            text = item.get("text", "")
        else:
            text = getattr(item, "text", "")
        if text:
            snippets.append(str(text).strip())
    return " ".join(snippets)


def fetch_transcript(video_id: str, *, timeout: int = 45) -> str:
    try:
        process = subprocess.run(
            [sys.executable, "-m", "ingest.youtube", video_id],
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(f"YouTube transcript timed out after {timeout} seconds") from exc

    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or "YouTube transcript retrieval failed")
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("YouTube transcript worker returned invalid output") from exc
    transcript = str(payload.get("transcript", "")).strip()
    if not transcript:
        raise RuntimeError("YouTube transcript was empty")
    return transcript


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m ingest.youtube VIDEO_ID")
    try:
        transcript = _fetch_direct(sys.argv[1])
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps({"transcript": transcript}, ensure_ascii=False))


if __name__ == "__main__":
    main()
