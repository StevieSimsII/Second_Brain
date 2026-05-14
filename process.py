"""
Outlook → Wiki + Notion pipeline — manual entry point.

Reads unprocessed emails from the Outlook Learnings folder, generates wiki pages
via OpenAI, creates Notion pages, and maintains wiki/index.md and wiki/log.md.

Usage:
    python process.py               # fetch URLs + use body as notes (ideal for new emails)
    python process.py --body-only   # use email body directly, skip URL fetching (for backlog)
    python process.py --dry-run     # preview without writing or calling APIs
    python process.py --reprocess   # ignore processed history and re-run all emails
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone

import config
from fetchers.github import fetch_github_repo, is_github_url
from fetchers.web import fetch_article
from ingest.outlook import read_learnings_folder
from llm.gpt import generate_lesson, generate_notes_page, lesson_to_wiki_markdown
from notionapi.client import create_lesson_page
from wiki_manager import append_log, update_index, write_page

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


def _load_processed() -> set[str]:
    if config.PROCESSED_FILE.exists():
        return set(json.loads(config.PROCESSED_FILE.read_text(encoding="utf-8")))
    return set()


def _save_processed(processed: set[str]) -> None:
    config.PROCESSED_FILE.write_text(
        json.dumps(sorted(processed), indent=2), encoding="utf-8"
    )


def _fetch_url(url: str) -> tuple[str, str]:
    if is_github_url(url):
        log.info("  Fetching GitHub repo: %s", url)
        return "github", fetch_github_repo(url)
    log.info("  Fetching article: %s", url)
    return "web", fetch_article(url)


def _personal_notes(email_body: str, urls: list[str]) -> str:
    """Strip URLs from the body to isolate the human-written notes."""
    text = email_body
    for url in urls:
        text = text.replace(url, "")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines)


def process_email_body_only(email, *, dry_run: bool) -> int:
    """Body-only mode: convert the full email body directly into a wiki page.
    No URL fetching. One page per email. Good for backlog with pre-written notes."""
    try:
        date_str = email.received.strftime("%Y-%m-%d")
    except Exception:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    body = email.body.strip()
    if not body:
        log.info("  Empty body — skipping '%s'", email.subject)
        return 0

    if dry_run:
        log.info("  [dry-run] Would generate notes page from body: %s", email.subject)
        return 1

    try:
        markdown = generate_notes_page(
            subject=email.subject,
            notes=body,
            date=date_str,
        )
    except Exception as exc:
        log.error("  OpenAI error for '%s': %s", email.subject, exc)
        return 0

    # Best-effort Notion page using a minimal lesson dict
    try:
        lesson = {
            "title": email.subject,
            "tags": [],
            "overview": body[:500],
            "key_concepts": [],
            "how_it_works": body,
            "training_exercise": "",
            "further_reading": [],
        }
        notion_url = create_lesson_page(lesson=lesson, source_url="personal notes")
        log.info("  Notion page created: %s", notion_url)
    except Exception as exc:
        log.warning("  Notion skipped for '%s': %s", email.subject, exc)
        notion_url = "(notion skipped)"

    page_path = write_page(markdown)
    update_index(page_path, markdown)
    append_log(
        email_subject=email.subject,
        source_url="personal notes",
        page_path=page_path,
        notion_url=notion_url,
        date=date_str,
    )
    return 1


def process_email(email, *, dry_run: bool) -> int:
    """URL mode: fetch each URL in the email, generate a lesson, create wiki + Notion pages."""
    try:
        date_str = email.received.strftime("%Y-%m-%d")
    except Exception:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    personal_notes = _personal_notes(email.body, email.urls)
    pages_created = 0

    if not email.urls:
        log.info("  No URLs found — skipping '%s'", email.subject)
        return 0

    for url in email.urls:
        log.info("  Processing URL: %s", url)

        try:
            source_type, content = _fetch_url(url)
        except Exception as exc:
            log.warning("  Could not fetch %s: %s", url, exc)
            continue

        if dry_run:
            log.info("  [dry-run] Would generate lesson + wiki page for: %s", url)
            pages_created += 1
            continue

        try:
            lesson = generate_lesson(url, source_type, content)
        except Exception as exc:
            log.error("  OpenAI error for %s: %s", url, exc)
            continue

        try:
            notion_url = create_lesson_page(lesson=lesson, source_url=url)
            log.info("  Notion page created: %s", notion_url)
        except Exception as exc:
            log.error("  Notion error for %s: %s", url, exc)
            notion_url = "(notion error)"

        markdown = lesson_to_wiki_markdown(
            lesson,
            source_url=url,
            personal_notes=personal_notes,
            date=date_str,
        )

        page_path = write_page(markdown)
        update_index(page_path, markdown)
        append_log(
            email_subject=email.subject,
            source_url=url,
            page_path=page_path,
            notion_url=notion_url,
            date=date_str,
        )
        pages_created += 1

    return pages_created


def main() -> None:
    parser = argparse.ArgumentParser(description="Process Outlook Learnings folder into wiki + Notion.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files or calling APIs.")
    parser.add_argument("--reprocess", action="store_true", help="Ignore processed history and re-run all emails.")
    parser.add_argument("--body-only", action="store_true",
                        help="Use email body directly as wiki content. Skips URL fetching. "
                             "Use this for backlog emails that already contain your notes.")
    args = parser.parse_args()

    processed = set() if args.reprocess else _load_processed()

    mode = "body-only" if args.body_only else "url-fetch"
    log.info("Mode: %s | Reading emails from: %s", mode, config.OUTLOOK_FOLDER)

    try:
        emails = read_learnings_folder(config.OUTLOOK_FOLDER)
    except RuntimeError as exc:
        log.error("%s", exc)
        sys.exit(1)

    new_emails = [e for e in emails if e.entry_id not in processed]
    log.info(
        "%d new email(s) to process (skipping %d already processed).",
        len(new_emails), len(emails) - len(new_emails),
    )

    if not new_emails:
        log.info("Nothing to do.")
        return

    total_pages = 0
    for i, email in enumerate(new_emails, 1):
        log.info("[%d/%d] %s", i, len(new_emails), email.subject)
        if args.body_only:
            pages = process_email_body_only(email, dry_run=args.dry_run)
        else:
            pages = process_email(email, dry_run=args.dry_run)
        total_pages += pages
        if not args.dry_run:
            processed.add(email.entry_id)
            _save_processed(processed)

    verb = "would be created (dry run)" if args.dry_run else "created"
    log.info("Done. %d wiki page(s) %s from %d email(s).", total_pages, verb, len(new_emails))


if __name__ == "__main__":
    main()
