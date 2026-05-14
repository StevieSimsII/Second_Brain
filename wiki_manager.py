"""Manage wiki files: write pages, update index.md and log.md."""
from __future__ import annotations

import re
import logging
from pathlib import Path

import config

log = logging.getLogger(__name__)


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80]


def _extract_frontmatter_value(markdown: str, key: str) -> str:
    match = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', markdown, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _extract_tags(markdown: str) -> list[str]:
    match = re.search(r'^tags:\s*\[([^\]]*)\]', markdown, re.MULTILINE)
    if not match:
        return []
    return [t.strip().strip('"').strip("'") for t in match.group(1).split(",") if t.strip()]


def write_page(markdown: str, slug: str | None = None) -> Path:
    """Write a wiki page to wiki/pages/<slug>.md and return its path."""
    config.PAGES_DIR.mkdir(parents=True, exist_ok=True)

    title = _extract_frontmatter_value(markdown, "title")
    if not slug:
        date = _extract_frontmatter_value(markdown, "date")
        slug = f"{date}-{_slugify(title)}" if date else _slugify(title)

    path = config.PAGES_DIR / f"{slug}.md"
    counter = 1
    while path.exists():
        path = config.PAGES_DIR / f"{slug}-{counter}.md"
        counter += 1

    path.write_text(markdown, encoding="utf-8")
    log.info("Wrote wiki page: %s", path.name)
    return path


def update_index(page_path: Path, markdown: str) -> None:
    """Add an entry for page_path in wiki/index.md."""
    config.WIKI_DIR.mkdir(parents=True, exist_ok=True)
    index_path = config.WIKI_DIR / "index.md"

    title = _extract_frontmatter_value(markdown, "title") or page_path.stem
    tags = _extract_tags(markdown)
    date = _extract_frontmatter_value(markdown, "date")
    tag_str = ", ".join(f"`{t}`" for t in tags) if tags else ""

    rel_link = f"pages/{page_path.name}"
    entry = f"- [{title}]({rel_link}) — {date}{' | ' + tag_str if tag_str else ''}"

    if not index_path.exists():
        index_path.write_text(
            "# Wiki Index\n\n"
            "All pages are listed below. Updated automatically on each ingest.\n\n",
            encoding="utf-8",
        )

    content = index_path.read_text(encoding="utf-8")
    if page_path.name in content:
        log.debug("Index already contains %s, skipping.", page_path.name)
        return

    content = content.rstrip() + "\n" + entry + "\n"
    index_path.write_text(content, encoding="utf-8")
    log.info("Updated index.md with: %s", title)


def append_log(*, email_subject: str, source_url: str, page_path: Path, notion_url: str, date: str) -> None:
    """Append a single entry to wiki/log.md."""
    config.WIKI_DIR.mkdir(parents=True, exist_ok=True)
    log_path = config.WIKI_DIR / "log.md"

    if not log_path.exists():
        log_path.write_text(
            "# Ingest Log\n\nAppend-only record of all ingested sources.\n\n",
            encoding="utf-8",
        )

    rel_link = f"pages/{page_path.name}"
    entry = (
        f"## [{date}] ingest | {email_subject}\n"
        f"- Source: {source_url}\n"
        f"- Wiki page: [{page_path.stem}]({rel_link})\n"
        f"- Notion: {notion_url}\n\n"
    )

    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)
    log.info("Appended to log.md: %s", email_subject)
