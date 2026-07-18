"""Telegram commands for capturing links into the Second Brain."""
from __future__ import annotations

import asyncio
import logging
import re

from telegram import Update
from telegram.ext import ContextTypes

from ingest import config
from ingest.github import github_healthcheck
from ingest.pipeline import process_link
from ingest.sources import SourceQualityError


log = logging.getLogger(__name__)
URL_RE = re.compile(r"https?://[^\s]+", re.IGNORECASE)


def _authorized(update: Update) -> bool:
    user = update.effective_user
    return user is not None and user.id == config.ALLOWED_TELEGRAM_USER_ID


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _authorized(update):
        await update.message.reply_text("Not authorized.")
        return
    await update.message.reply_text(
        "Send me an article, GitHub repository, or YouTube link. I’ll create a "
        "grounded lesson in your Second Brain and return its direct link.\n\n"
        "Commands: /status"
    )


async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _authorized(update):
        await update.message.reply_text("Not authorized.")
        return
    try:
        repository = await asyncio.to_thread(github_healthcheck)
    except Exception:
        log.exception("Second Brain health check failed")
        await update.message.reply_text("The bot is running, but GitHub is not reachable.")
        return
    await update.message.reply_text(
        f"Second Brain is ready.\nRepository: {repository}\nCodex model: {config.CODEX_MODEL}"
    )


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _authorized(update):
        log.warning("Unauthorized Telegram user: %s", update.effective_user)
        await update.message.reply_text("Not authorized.")
        return

    text = update.message.text or ""
    match = URL_RE.search(text)
    if not match:
        await update.message.reply_text("I didn’t find a URL in that message.")
        return

    url = match.group(0).rstrip(").,;!?")
    await update.message.reply_text("Capturing the source and checking its evidence…")
    try:
        result = await asyncio.to_thread(process_link, url)
    except SourceQualityError as exc:
        log.warning("Source rejected: %s", exc)
        await update.message.reply_text(
            f"I didn’t save this one because the source was too thin.\n\n{exc}"
        )
        return
    except Exception:
        log.exception("Capture failed for %s", url)
        await update.message.reply_text(
            "The capture failed before it was published. You can safely send the link again."
        )
        return

    if result["duplicate"]:
        prefix = "Already saved."
    else:
        prefix = "Saved."
    await update.message.reply_text(
        f"{prefix}\n\n{result['title']}\n{result['site_url']}",
        disable_web_page_preview=False,
    )


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.exception("Unhandled Telegram error", exc_info=context.error)

