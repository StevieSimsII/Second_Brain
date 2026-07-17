"""Source-aware content retrieval with evidence-quality safeguards."""
from __future__ import annotations

import base64
import logging
from dataclasses import dataclass
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from ingest import config
from ingest.urls import normalize_url, youtube_video_id
from ingest.youtube import fetch_transcript


log = logging.getLogger(__name__)
GITHUB_API = "https://api.github.com"
USER_AGENT = "Mozilla/5.0 (compatible; SecondBrainCapture/2.0)"
MAX_SOURCE_CHARS = 80_000


class SourceQualityError(ValueError):
    """The source could not support a trustworthy lesson."""


@dataclass(frozen=True)
class FetchedSource:
    url: str
    kind: str
    content: str

    @property
    def character_count(self) -> int:
        return len(self.content)


def _github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    if config.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {config.GITHUB_TOKEN}"
    return headers


def _is_github_repo(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.lower() in {"github.com", "www.github.com"} and len(
        parsed.path.strip("/").split("/")
    ) >= 2


def _github_get(path: str) -> requests.Response:
    response = requests.get(
        f"{GITHUB_API}{path}", headers=_github_headers(), timeout=30
    )
    response.raise_for_status()
    return response


def _fetch_github(url: str) -> FetchedSource:
    owner, repo, *_ = urlparse(url).path.strip("/").split("/")
    repo = repo.removesuffix(".git")
    metadata = _github_get(f"/repos/{owner}/{repo}").json()
    branch = metadata.get("default_branch", "main")

    try:
        readme_data = _github_get(f"/repos/{owner}/{repo}/readme").json()
        readme = base64.b64decode(readme_data.get("content", "")).decode(
            "utf-8", errors="replace"
        )
    except requests.HTTPError:
        readme = ""

    try:
        tree_data = _github_get(
            f"/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        ).json()
        paths = [
            item["path"]
            for item in tree_data.get("tree", [])
            if item.get("type") == "blob"
        ]
        paths.sort(key=lambda path: (path.count("/"), path.lower()))
        paths = paths[:250]
    except requests.HTTPError:
        paths = []

    content = "\n".join(
        [
            f"REPOSITORY: {owner}/{repo}",
            f"URL: {url}",
            f"DESCRIPTION: {metadata.get('description') or ''}",
            f"PRIMARY LANGUAGE: {metadata.get('language') or ''}",
            f"TOPICS: {', '.join(metadata.get('topics') or [])}",
            "\n===== README =====\n",
            readme,
            "\n===== FILE TREE =====\n",
            "\n".join(paths),
        ]
    )[:MAX_SOURCE_CHARS]
    return FetchedSource(url=url, kind="github", content=content)


def _fetch_youtube(url: str, video_id: str) -> FetchedSource:
    try:
        transcript = fetch_transcript(
            video_id, timeout=config.YOUTUBE_FETCH_TIMEOUT_SECONDS
        )
    except TimeoutError as exc:
        raise SourceQualityError(
            "YouTube did not return a transcript before the capture timeout."
        ) from exc
    except RuntimeError as exc:
        raise SourceQualityError(
            "I could not retrieve a usable transcript for that YouTube video."
        ) from exc
    content = (
        f"YOUTUBE VIDEO ID: {video_id}\nURL: {url}\n\n"
        f"===== TRANSCRIPT =====\n{transcript}"
    )
    return FetchedSource(url=url, kind="youtube", content=content[:MAX_SOURCE_CHARS])


def _fetch_web(url: str) -> FetchedSource:
    response = requests.get(
        url, headers={"User-Agent": USER_AGENT}, timeout=(10, 30)
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else url
    for tag in soup(
        ["script", "style", "noscript", "iframe", "svg", "nav", "footer", "header", "form"]
    ):
        tag.decompose()
    candidate = soup.find("article") or soup.find("main") or soup.body or soup
    lines = [line.strip() for line in candidate.get_text("\n").splitlines() if line.strip()]
    text = "\n".join(lines)
    content = f"TITLE: {title}\nURL: {url}\n\n{text}"[:MAX_SOURCE_CHARS]
    return FetchedSource(url=url, kind="web", content=content)


def validate_source(source: FetchedSource) -> FetchedSource:
    minimum = (
        config.MIN_YOUTUBE_SOURCE_CHARS
        if source.kind == "youtube"
        else config.MIN_WEB_SOURCE_CHARS
    )
    if source.kind == "github":
        minimum = 1_000
    if source.character_count < minimum:
        host = urlparse(source.url).netloc
        raise SourceQualityError(
            f"I only retrieved {source.character_count:,} characters from {host}; "
            f"at least {minimum:,} are required for a trustworthy lesson."
        )
    return source


def fetch_source(raw_url: str) -> FetchedSource:
    url = normalize_url(raw_url)
    video_id = youtube_video_id(url)
    if video_id:
        source = _fetch_youtube(url, video_id)
    elif _is_github_repo(url):
        source = _fetch_github(url)
    else:
        source = _fetch_web(url)
    log.info("Fetched %s source (%d characters)", source.kind, source.character_count)
    return validate_source(source)
