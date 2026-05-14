"""OpenAI GPT client — turns raw fetched content into a structured lesson."""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from openai import OpenAI

import config

log = logging.getLogger(__name__)

_client = OpenAI(api_key=config.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert technical educator. You take raw content from a web \
article or a GitHub repository and transform it into a structured, self-contained \
training lesson aimed at a curious engineer who has not seen this material before.

You MUST return valid JSON matching this exact schema:

{
  "title": "A concise, descriptive lesson title (max 120 chars).",
  "tags": ["3-6 lowercase tag strings capturing the core topics/technologies"],
  "overview": "1-2 paragraphs explaining what this is, why it matters, and who would care.",
  "key_concepts": [
    {"name": "Short concept name", "explanation": "2-4 sentence explanation of the concept."}
  ],
  "how_it_works": "A multi-paragraph walkthrough of the mechanics. If it's a repo, explain the code structure, main modules, and data flow. If it's an article, explain the central ideas and reasoning step by step. Markdown is allowed (bullets, code blocks with triple backticks).",
  "training_exercise": "A concrete hands-on exercise the reader can do to cement the learning. Include step-by-step instructions and, where useful, a small code snippet or command. Markdown allowed.",
  "further_reading": [
    {"title": "Resource title", "url": "https://..."}
  ]
}

Rules:
- Return ONLY the JSON object. No prose, no markdown fences around it.
- 4-8 key_concepts. 2-5 further_reading items (infer likely canonical resources if none are in the source).
- Keep the tone practical and technical; assume the reader is a working engineer.
- If the source is a repository, always describe the actual code/architecture — don't just paraphrase the README.
"""


def _extract_json(text: str) -> dict[str, Any]:
    """Be forgiving if the model wraps the JSON in ```json fences."""
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```\s*$", "", stripped)
    return json.loads(stripped)


def generate_lesson(url: str, source_type: str, content: str) -> dict[str, Any]:
    """Call OpenAI and return the parsed lesson dict."""
    user_message = (
        f"Source URL: {url}\n"
        f"Source type: {source_type}\n\n"
        f"Source content follows between the BEGIN/END markers.\n"
        f"--- BEGIN SOURCE ---\n{content}\n--- END SOURCE ---\n\n"
        "Produce the lesson JSON now."
    )

    response = _client.chat.completions.create(
        model=config.OPENAI_MODEL,
        max_completion_tokens=4096,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content or ""
    log.debug("OpenAI raw response: %s", raw[:500])

    lesson = _extract_json(raw)
    required = ("title", "overview", "key_concepts", "how_it_works", "training_exercise")
    missing = [k for k in required if not lesson.get(k)]
    if missing:
        raise ValueError(f"Lesson JSON missing required fields: {missing}")

    lesson.setdefault("tags", [])
    lesson.setdefault("further_reading", [])
    return lesson


def lesson_to_wiki_markdown(
    lesson: dict[str, Any],
    *,
    source_url: str,
    personal_notes: str,
    date: str,
) -> str:
    """Convert a lesson dict to a wiki-page markdown string (no extra LLM call)."""
    title = lesson.get("title", "Untitled")
    tags = lesson.get("tags", [])
    tag_list = "[" + ", ".join(tags) + "]" if tags else "[]"

    key_concepts_md = "\n".join(
        f"- **{kc['name']}**: {kc['explanation']}"
        for kc in lesson.get("key_concepts", [])
    )

    further_reading_md = "\n".join(
        f"- [{fr['title']}]({fr['url']})"
        for fr in lesson.get("further_reading", [])
    ) or "- (none)"

    notes_section = personal_notes.strip() if personal_notes.strip() else "(no personal notes)"

    return f"""---
title: "{title}"
source: "{source_url}"
date: "{date}"
tags: {tag_list}
---

## Overview
{lesson.get("overview", "")}

## Key Concepts
{key_concepts_md}

## How It Works
{lesson.get("how_it_works", "")}

## Training Exercise
{lesson.get("training_exercise", "")}

## Personal Notes
{notes_section}

## Further Reading
{further_reading_md}
""".strip()


NOTES_SYSTEM_PROMPT = """You are a personal knowledge base curator. Convert the provided \
personal notes into a well-structured wiki page in Markdown format.

Output a single Markdown document with this structure:

---
title: "Concise title derived from the notes (max 100 chars)"
source: "personal notes"
date: "<YYYY-MM-DD>"
tags: [tag1, tag2, tag3]
---

## Overview
1-2 paragraphs summarising what the notes cover and why it matters.

## Key Concepts
- **Concept**: explanation. (3-6 bullets)

## How It Works
Expand on the mechanics or ideas in the notes with additional context where helpful.

## Personal Notes
<reproduce the original notes verbatim here>

## Further Reading
- [Title](url) (2-3 inferred resources, or "(none)" if not applicable)

Rules:
- Output ONLY the markdown document. No preamble.
- Tags: 3-6 lowercase strings.
- Keep tone practical and useful for future reference.
"""


def generate_notes_page(*, subject: str, notes: str, date: str) -> str:
    """Generate a wiki markdown page from a plain-text email body (no URL fetching)."""
    user_message = (
        f"Email subject: {subject}\n"
        f"Date: {date}\n\n"
        f"--- NOTES ---\n{notes}\n--- END NOTES ---\n\n"
        "Generate the wiki page now."
    )

    response = _client.chat.completions.create(
        model=config.OPENAI_MODEL,
        max_completion_tokens=2048,
        messages=[
            {"role": "system", "content": NOTES_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content or ""
    if raw.strip().startswith("```"):
        raw = re.sub(r"^```(?:markdown)?\s*\n?", "", raw.strip())
        raw = re.sub(r"\n?```\s*$", "", raw)
    return raw.strip()
