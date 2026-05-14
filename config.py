"""Load configuration from .env.local / .env and expose as module-level constants."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_BASE = Path(__file__).resolve().parent
load_dotenv(_BASE / ".env.local")
load_dotenv(_BASE / ".env")


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


# OpenAI
OPENAI_API_KEY = _required("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Notion (optional — pages are created if these are set, otherwise skipped)
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
NOTION_PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID", "")

# GitHub (optional)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or None

# Outlook folder to watch
OUTLOOK_FOLDER = os.getenv("OUTLOOK_FOLDER", "Learnings")

# Microsoft Graph — authentication
# Local dev: device code flow (only CLIENT_ID + TENANT_ID needed)
# CI/GitHub Actions: client credentials flow (CLIENT_ID + TENANT_ID + CLIENT_SECRET + USER_EMAIL)
GRAPH_CLIENT_ID = _required("GRAPH_CLIENT_ID")
GRAPH_TENANT_ID = _required("GRAPH_TENANT_ID")
GRAPH_CLIENT_SECRET = os.getenv("GRAPH_CLIENT_SECRET", "")   # CI only
GRAPH_USER_EMAIL = os.getenv("GRAPH_USER_EMAIL", "")         # CI only

# Wiki paths
WIKI_DIR = _BASE / "wiki"
PAGES_DIR = WIKI_DIR / "pages"
PROCESSED_FILE = _BASE / ".processed.json"
