# 🧠 Stevie's Second Brain

This repository is now the publishing layer for the site, not the ingestion pipeline. Its job is simple: take markdown pages in `wiki/pages/`, turn them into a searchable static site, and publish the result through GitHub Pages.

The generated site uses this README as its desktop landing page, so keeping this file accurate affects both the repository docs and the live site experience.

## How It Works Now

```text
Capture or generate notes elsewhere
(manual writing, a bot, another repo, or any script)
        ↓
Write a publish-ready markdown file to wiki/pages/
        ↓
Push to main
        ↓
GitHub Actions runs build_site.py
        ↓
build_site.py:
  - parses frontmatter
  - sorts pages by date
  - strips ## Personal Notes from public output
  - extracts a source URL when possible
  - rebuilds index.html
        ↓
Workflow commits the rebuilt index.html
        ↓
GitHub Pages serves the updated site
```

In my current setup, an upstream automation writes the markdown and pushes it here. This repo no longer fetches from Outlook, Microsoft Graph, Notion, or OpenAI directly. If you fork this project, anything that can write good markdown files into `wiki/pages/` can be your upstream.

## What This Repo Owns

- `wiki/pages/*.md` as the source of truth for published notes
- `build_site.py` as the static site builder
- `README.md` as the desktop landing page content inside the generated site
- `.github/workflows/build.yml` as the rebuild-and-publish automation
- `index.html` as the generated artifact GitHub Pages serves

## Content Format

Each note is one markdown file under `wiki/pages/`. The builder expects simple YAML frontmatter and a markdown body.

```md
---
title: "Inside VS Code's GitHub Copilot Coding Harness"
date: "2026-05-20"
tags: [copilot, vscode, ai-agents]
source: "https://example.com/post"
---

## Overview
A concise summary of what the piece is about.

## Key Concepts
- First concept
- Second concept

## How It Works
Describe the mechanism, workflow, or architecture.

## Personal Notes
Source: https://example.com/post
Notion page: https://www.notion.so/...
Private reminders that should not be published verbatim.
```

Notes:

- `date` controls sort order, so use `YYYY-MM-DD`.
- `title` and the markdown body are what readers see in the site.
- `tags` drive filtering and search discovery.
- `source` is optional, but recommended.
- The `## Personal Notes` section is removed from the public article view.
- If `source` is blank or set to `personal notes`, the builder tries to recover a `Source: https://...` URL from the `## Personal Notes` section before stripping it.

## Local Workflow

Prerequisites:

- Python 3.11+ is enough.
- Install the build dependency before running the generator.

```bash
python -m pip install -r requirements.txt
```

Build the site locally:

```bash
python build_site.py
```

Write the generated file somewhere else:

```bash
python build_site.py --out C:/path/to/index.html
```

Then open `index.html` in a browser to inspect the result.

## Publishing Flow

- GitHub Pages serves the root `index.html` from `main`.
- The build workflow runs on pushes that change `wiki/pages/**`, `build_site.py`, or `README.md`, and it also supports manual dispatch.
- The workflow rebuilds `index.html`, commits it with a `build:` timestamp, and pushes the generated file back to `main`.

## Project Layout

```text
Second_Brain/
├── .github/
│   └── workflows/
│       └── build.yml       # Rebuilds index.html on content or builder changes
├── wiki/
│   └── pages/              # Publish-ready markdown notes
├── build_site.py           # Converts wiki pages + README into the site
├── README.md               # Repo docs and desktop landing page content
├── index.html              # Generated site artifact
├── requirements.txt        # Build-time markdown dependency
└── apple-touch-icon.png    # GitHub Pages asset
```

The active runtime path is intentionally small: markdown in, static site out. Some legacy directories may still exist in the repo, but the current build and deploy path is driven by `wiki/pages/`, `build_site.py`, `README.md`, and the build workflow.

## Adding Content

You have two basic options:

1. Write markdown files directly in `wiki/pages/`.
2. Use an upstream capture or summarization tool that generates markdown and commits or pushes it here.

As long as the final artifact is a correctly formatted markdown file in `wiki/pages/`, this repo will publish it.

## License

MIT — fork it, adapt it, and point it at your own upstream content pipeline.
