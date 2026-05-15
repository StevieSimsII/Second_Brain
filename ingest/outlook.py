"""Read emails from Microsoft 365 via Microsoft Graph API.

Local dev:  device code flow (interactive browser sign-in, token cached locally)
CI/Actions: client credentials flow (non-interactive, needs Mail.Read app permission)
"""
from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import msal
import requests

import config

log = logging.getLogger(__name__)

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
SCOPES = ["Mail.Read"]
TOKEN_CACHE_FILE = Path(__file__).resolve().parent.parent / ".token_cache.json"

URL_RE = re.compile(
    r"https?://[^\s\"'<>\(\)\[\]{}|\\^`]+(?<![.,;:!?])",
    re.IGNORECASE,
)


@dataclass
class EmailItem:
    entry_id: str
    subject: str
    body: str
    received: datetime
    urls: list[str] = field(default_factory=list)


# ── Auth ──────────────────────────────────────────────────────────────────────

def _is_ci() -> bool:
    return bool(os.getenv("GITHUB_ACTIONS") or config.GRAPH_CLIENT_SECRET)


def _get_token_client_credentials() -> str:
    """Non-interactive CI auth. Requires Mail.Read *Application* permission in Azure."""
    app = msal.ConfidentialClientApplication(
        client_id=config.GRAPH_CLIENT_ID,
        client_credential=config.GRAPH_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{config.GRAPH_TENANT_ID}",
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(
            f"Client credentials auth failed: {result.get('error_description', result.get('error'))}"
        )
    log.info("Authenticated via client credentials (CI mode).")
    return result["access_token"]


def _load_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_FILE.exists():
        cache.deserialize(TOKEN_CACHE_FILE.read_text(encoding="utf-8"))
    return cache


def _save_cache(cache: msal.SerializableTokenCache) -> None:
    if cache.has_state_changed:
        TOKEN_CACHE_FILE.write_text(cache.serialize(), encoding="utf-8")


def _get_token_device_code() -> str:
    """Interactive device code flow for local development."""
    cache = _load_cache()
    app = msal.PublicClientApplication(
        client_id=config.GRAPH_CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{config.GRAPH_TENANT_ID}",
        token_cache=cache,
    )

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            _save_cache(cache)
            return result["access_token"]

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError(f"Device flow failed: {flow.get('error_description')}")

    print("\n" + "=" * 60)
    print(flow["message"])
    print("=" * 60 + "\n")

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(
            f"Authentication failed: {result.get('error_description', result.get('error'))}"
        )

    _save_cache(cache)
    log.info("Authentication successful.")
    return result["access_token"]


def _get_token() -> str:
    return _get_token_client_credentials() if _is_ci() else _get_token_device_code()


# ── Graph helpers ─────────────────────────────────────────────────────────────

def _base_path() -> str:
    """Use /users/{email}/... for app permissions (CI), /me/... for delegated (local)."""
    return f"/users/{config.GRAPH_USER_EMAIL}" if _is_ci() else "/me"


def _get(token: str, path: str, params: dict | None = None) -> dict:
    url = path if path.startswith("https://") else f"{GRAPH_BASE}{path}"
    resp = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Prefer": 'outlook.body-content-type="text"',
        },
        params=params,
        timeout=30,
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        detail = resp.text.strip()
        hints: list[str] = []
        if resp.status_code == 403 and "/mailFolders" in url:
            hints.extend([
                "verify the Azure app has Microsoft Graph Application permission Mail.Read",
                "grant admin consent for the application permission in Microsoft Entra",
                "confirm GRAPH_USER_EMAIL is the exact Microsoft 365 mailbox address in this tenant",
                "check Exchange Online app mailbox restrictions such as App RBAC or Application Access Policies",
            ])
        hint_text = f" Likely fixes: {'; '.join(hints)}." if hints else ""
        if detail:
            raise RuntimeError(
                f"Graph request failed ({resp.status_code}) for {url}: {detail}{hint_text}"
            ) from exc
        raise RuntimeError(
            f"Graph request failed ({resp.status_code}) for {url}.{hint_text}"
        ) from exc
    return resp.json()


def _ascii_lower(s: str) -> str:
    return "".join(c for c in s if ord(c) < 128).lower().strip()


def _name_matches(display_name: str, target: str) -> bool:
    return (
        display_name.lower().strip() == target.lower().strip()
        or _ascii_lower(display_name) == _ascii_lower(target)
        or _ascii_lower(target) in _ascii_lower(display_name)
    )


def _find_folder_id(token: str, folder_name: str) -> str:
    base = _base_path()
    data = _get(token, f"{base}/mailFolders", {"$top": 100})
    folders = data.get("value", [])

    for f in folders:
        if _name_matches(f["displayName"], folder_name):
            log.info("Found folder '%s' (top-level)", f["displayName"])
            return f["id"]

    for f in folders:
        try:
            children = _get(token, f"{base}/mailFolders/{f['id']}/childFolders", {"$top": 100})
            for child in children.get("value", []):
                if _name_matches(child["displayName"], folder_name):
                    log.info("Found folder '%s' (child of %s)", child["displayName"], f["displayName"])
                    return child["id"]
        except Exception as exc:
            log.debug("Could not list children of %s: %s", f["displayName"], exc)

    available = [f["displayName"] for f in folders]
    raise RuntimeError(
        f"Folder '{folder_name}' not found.\nTop-level folders: {available}\n"
        f"Check the OUTLOOK_FOLDER env var."
    )


# ── Public API ────────────────────────────────────────────────────────────────

def _extract_urls(text: str) -> list[str]:
    return list(dict.fromkeys(URL_RE.findall(text)))


def read_learnings_folder(folder_name: str) -> list[EmailItem]:
    """Return all emails from the named folder, oldest first."""
    token = _get_token()
    base = _base_path()

    log.info("Searching for folder '%s'...", folder_name)
    folder_id = _find_folder_id(token, folder_name)

    items: list[EmailItem] = []
    next_url: str | None = f"{base}/mailFolders/{folder_id}/messages"
    params: dict | None = {
        "$top": 50,
        "$select": "id,subject,body,receivedDateTime",
        "$orderby": "receivedDateTime asc",
    }

    while next_url:
        data = _get(token, next_url, params)
        params = None

        for msg in data.get("value", []):
            body_text = msg.get("body", {}).get("content", "") or ""
            received_str = msg.get("receivedDateTime", "")
            try:
                received = datetime.fromisoformat(received_str.replace("Z", "+00:00"))
            except Exception:
                received = datetime.utcnow()

            items.append(EmailItem(
                entry_id=msg["id"],
                subject=msg.get("subject") or "(no subject)",
                body=body_text,
                received=received,
                urls=_extract_urls(body_text),
            ))

        next_url = data.get("@odata.nextLink")

    log.info("Found %d email(s) in '%s'", len(items), folder_name)
    return items
