"""Configuration for the Telegram ingestion service."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env.local")
load_dotenv(REPO_ROOT / ".env")


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_TELEGRAM_USER_ID = int(os.getenv("ALLOWED_TELEGRAM_USER_ID", "0"))

# Lesson generation uses Codex CLI ChatGPT-plan auth (`codex login`), not API keys.
CODEX_BIN = os.getenv("CODEX_BIN", "codex")
CODEX_MODEL = os.getenv("CODEX_MODEL", "gpt-5.4")
CODEX_TIMEOUT_SECONDS = int(os.getenv("CODEX_TIMEOUT_SECONDS", "300"))

# Accept the former service's variable during migration; GITHUB_TOKEN is canonical.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("SECOND_BRAIN_GITHUB_TOKEN", "")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "StevieSimsII/Second_Brain")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
SITE_URL = os.getenv(
    "SECOND_BRAIN_SITE_URL", "https://steviesimsii.github.io/Second_Brain/"
)

CAPTURE_TIMEZONE = os.getenv("CAPTURE_TIMEZONE", "America/Chicago")
MIN_WEB_SOURCE_CHARS = int(os.getenv("MIN_WEB_SOURCE_CHARS", "800"))
MIN_YOUTUBE_SOURCE_CHARS = int(os.getenv("MIN_YOUTUBE_SOURCE_CHARS", "1500"))
YOUTUBE_FETCH_TIMEOUT_SECONDS = int(os.getenv("YOUTUBE_FETCH_TIMEOUT_SECONDS", "45"))


def validate_runtime() -> None:
    """Fail once at startup with a concise list of missing settings."""
    from ingest.codex import validate_codex_runtime

    required = {
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "ALLOWED_TELEGRAM_USER_ID": ALLOWED_TELEGRAM_USER_ID,
        "GITHUB_TOKEN": GITHUB_TOKEN,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeError(f"Missing required settings: {', '.join(missing)}")
    validate_codex_runtime()
