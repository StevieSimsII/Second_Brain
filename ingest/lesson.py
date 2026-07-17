"""Generate and render grounded Second Brain lessons."""
from __future__ import annotations

import json
import re
from typing import Any

from openai import OpenAI

from ingest import config
from ingest.sources import FetchedSource


SYSTEM_PROMPT = """You are an expert technical educator building a durable personal
knowledge base. Transform the supplied source into a self-contained, practical lesson.

Return only JSON matching this schema:
{
  "title": "Concise descriptive title, at most 120 characters",
  "tags": ["3-6 stable lowercase topic tags"],
  "overview": "Why this matters in 1-2 paragraphs",
  "key_concepts": [{"name": "Concept", "explanation": "Grounded explanation"}],
  "how_it_works": "Detailed Markdown walkthrough",
  "training_exercise": "Concrete step-by-step exercise in Markdown",
  "further_reading": [{"title": "Resource", "url": "https://..."}]
}

Rules:
- Base factual claims on the supplied source. Never conceal thin or uncertain evidence.
- For repositories, describe the observed architecture and files, not an imagined codebase.
- Use 4-8 key concepts.
- Include further-reading URLs only when they appear in the supplied source; otherwise use [].
- Prefer reusable topic tags over news-cycle or marketing tags.
"""


def _extract_json(text: str) -> dict[str, Any]:
    value = text.strip()
    if value.startswith("```"):
        value = re.sub(r"^```(?:json)?\s*", "", value)
        value = re.sub(r"\s*```\s*$", "", value)
    return json.loads(value)


def generate_lesson(source: FetchedSource) -> dict[str, Any]:
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        max_completion_tokens=4096,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Source URL: {source.url}\n"
                    f"Source type: {source.kind}\n"
                    f"Retrieved characters: {source.character_count}\n\n"
                    f"--- BEGIN SOURCE ---\n{source.content}\n--- END SOURCE ---"
                ),
            },
        ],
    )
    lesson = _extract_json(response.choices[0].message.content or "")
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

