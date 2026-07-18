"""URL -> evidence -> lesson -> canonical Markdown."""
from __future__ import annotations

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from ingest import config
from ingest.github import PublishResult, find_existing, publish_markdown
from ingest.lesson import generate_lesson, render_markdown
from ingest.sources import fetch_source
from ingest.urls import normalize_url, source_fingerprint


log = logging.getLogger(__name__)


def process_link(raw_url: str) -> dict[str, str | bool]:
    url = normalize_url(raw_url)
    fingerprint = source_fingerprint(url)

    existing = find_existing(fingerprint, source_url=url)
    if existing:
        return _result(existing, title="Already in your Second Brain")

    source = fetch_source(url)
    log.info("Generating lesson from %s", source.kind)
    lesson = generate_lesson(source)
    date = datetime.now(ZoneInfo(config.CAPTURE_TIMEZONE)).strftime("%Y-%m-%d")
    markdown = render_markdown(
        lesson, source=source, date=date, fingerprint=fingerprint
    )
    published = publish_markdown(
        title=lesson["title"],
        markdown=markdown,
        fingerprint=fingerprint,
        date=date,
        check_existing=False,
    )
    log.info("Published %s", published.path)
    return _result(published, title=lesson["title"])


def _result(published: PublishResult, *, title: str) -> dict[str, str | bool]:
    return {
        "title": title,
        "site_url": published.site_url,
        "path": published.path,
        "duplicate": published.duplicate,
    }
