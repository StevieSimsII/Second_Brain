# 🧠 Stevie's Second Brain

One repository and one workflow for capturing, developing, searching, and publishing durable knowledge.

The live site is [Stevie's Second Brain](https://steviesimsii.github.io/Second_Brain/).

## The Workflow

```text
Send a link to Telegram
        ↓
Normalize the URL and check for duplicates
        ↓
Retrieve source evidence
  • YouTube transcript
  • GitHub metadata, README, and file tree
  • Readable article content
        ↓
Reject thin sources instead of inventing a lesson
        ↓
Generate a structured lesson with OpenAI
        ↓
Commit canonical Markdown to wiki/pages/
        ↓
GitHub Actions rebuilds the searchable site
        ↓
Telegram returns the direct article link
```

Markdown is the source of truth. Notion and email are not part of the pipeline.

## Repository Layout

```text
Second_Brain/
├── ingest/                  # Always-on Telegram capture service
│   ├── __main__.py          # python -m ingest
│   ├── sources.py           # GitHub, YouTube, and web acquisition
│   ├── lesson.py            # Grounded lesson generation
│   ├── github.py            # Idempotent Markdown publishing
│   └── requirements.txt     # Bot runtime dependencies
├── wiki/pages/              # Canonical lesson Markdown
├── build_site.py            # Searchable static-site generator
├── index.html               # Generated GitHub Pages site
├── tests/                   # Ingestion and knowledge-linking tests
└── docs/OPERATIONS.md       # Mac mini setup and daily operations
```

## Intelligence That Compounds

Every new capture stores stable metadata with the lesson:

- normalized source URL
- source type and evidence size
- a URL fingerprint used for deduplication
- reusable topic tags
- capture date

The site automatically connects each lesson to related notes using shared topics and title concepts. This is deliberately transparent and inexpensive: no vector database is needed for the first intelligence layer.

The next natural layer is retrieval over the Markdown collection for a Telegram `/ask` command. The canonical files are already structured to support that without another content store.

## Run the Site Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build_site.py
```

Open `index.html` after the build.

## Run the Telegram Capture Bot

```bash
source .venv/bin/activate
python -m pip install -r ingest/requirements.txt
cp .env.example .env.local
# Fill in Telegram, OpenAI, and GitHub values.
python -m ingest
```

Only one instance should poll a Telegram bot token at a time. The Mac mini is the permanent host; use a separate Telegram bot token for development.

See [docs/OPERATIONS.md](docs/OPERATIONS.md) for `launchd`, updates, logs, and migration from the former `LinkToNotionLessons` service.

## Content Format

Lessons are normal Markdown with YAML frontmatter:

```md
---
title: "A durable lesson title"
source: "https://example.com/source"
date: "2026-07-16"
tags: [agents, retrieval, knowledge-management]
source_type: "web"
source_fingerprint: "d8c66f8213"
source_characters: 18420
---

## Overview
...
```

You can also write or edit files in `wiki/pages/` manually. Pushing them to `main` rebuilds the site.

## Design Principles

- One canonical store: Git-tracked Markdown.
- Capture should be easier than postponing the note.
- Weak evidence should fail visibly.
- Generated knowledge should remain inspectable and editable.
- Intelligence should grow from the corpus without locking it into a proprietary store.
