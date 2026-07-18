"""Generate and render grounded Second Brain lessons via Codex ChatGPT auth."""
from __future__ import annotations

import re
from typing import Any

from ingest import config
from ingest.codex import LESSON_OUTPUT_SCHEMA, run_codex_structured
from ingest.sources import FetchedSource


SYSTEM_PROMPT = """You are an expert technical educator building a durable personal
knowledge base. Transform the supplied source into a self-contained, practical lesson.

Return only JSON matching the provided schema.

Rules:
- Base factual claims on the supplied source. Never conceal thin or uncertain evidence.
- For repositories, describe the observed architecture and files, not an imagined codebase.
- Use 4-8 key concepts.
- Include further-reading URLs only when they appear in the supplied source; otherwise use [].
- Prefer reusable topic tags over news-cycle or marketing tags.
- Title at most 120 characters.
- Tags should be 3-6 stable lowercase topic tags.
"""


def generate_lesson(source: FetchedSource) -> dict[str, Any]:
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Source URL: {source.url}\n"
        f"Source type: {source.kind}\n"
        f"Retrieved characters: {source.character_count}\n\n"
        f"--- BEGIN SOURCE ---\n{source.content}\n--- END SOURCE ---"
    )
    lesson = run_codex_structured(
        prompt,
        schema=LESSON_OUTPUT_SCHEMA,
        model=config.CODEX_MODEL,
        timeout=config.CODEX_TIMEOUT_SECONDS,
    )
    required = ("title", "overview", "key_concepts", "how_it_works", "training_exercise")
    missing = [key for key in required if not lesson.get(key)]
    if missing:
        raise ValueError(f"Generated lesson is missing: {', '.join(missing)}")
    lesson.setdefault("tags", [])
    lesson.setdefault("further_reading", [])
    return lesson


def _yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render_markdown(
    lesson: dict[str, Any], *, source: FetchedSource, date: str, fingerprint: str
) -> str:
    title = str(lesson.get("title") or "Untitled Lesson").strip()
    tags = [
        re.sub(r"[^a-z0-9-]+", "-", str(tag).strip().lower()).strip("-")
        for tag in lesson.get("tags", [])
        if str(tag).strip()
    ]
    lines = [
        "---",
        f'title: "{_yaml_quote(title)}"',
        f'source: "{_yaml_quote(source.url)}"',
        f'date: "{date}"',
        f"tags: [{', '.join(dict.fromkeys(tags))}]",
        f'source_type: "{source.kind}"',
        f'source_fingerprint: "{fingerprint}"',
        f"source_characters: {source.character_count}",
        "---",
        "",
        "## Overview",
        "",
        str(lesson["overview"]).strip(),
        "",
        "## Key Concepts",
        "",
    ]
    for concept in lesson.get("key_concepts", []):
        name = str(concept.get("name", "")).strip()
        explanation = str(concept.get("explanation", "")).strip()
        if name and explanation:
            lines.append(f"- **{name}**: {explanation}")

    lines.extend(
        [
            "",
            "## How It Works",
            "",
            str(lesson["how_it_works"]).strip(),
            "",
            "## Training Exercise",
            "",
            str(lesson["training_exercise"]).strip(),
        ]
    )
    reading = lesson.get("further_reading") or []
    if reading:
        lines.extend(["", "## Further Reading", ""])
        for item in reading:
            item_title = str(item.get("title", "")).strip()
            item_url = str(item.get("url", "")).strip()
            if item_url:
                lines.append(f"- [{item_title or item_url}]({item_url})")
    return "\n".join(lines).rstrip() + "\n"
