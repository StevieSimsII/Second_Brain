---
title: "AI-Assisted Markdown Presentations with Obsidian and Slidev"
source: "personal notes"
date: "2026-05-01"
tags: [markdown, slidev, obsidian, ai-tools, presentations]
---

## Overview

These notes describe a Markdown-first workflow for building presentations using local text files, Obsidian for editing, Slidev for rendering slides, and AI coding tools for research summarization and file transformation. Instead of treating slide creation as a separate activity in PowerPoint or another GUI tool, the process keeps research notes and final presentation content in the same file-based system.

This matters because it creates a tighter loop between knowledge capture, synthesis, and output. For people who already work comfortably with Markdown and local files, the approach makes presentations feel more like software artifacts: searchable, reusable, versionable, and easier for AI tools to manipulate with precision.

## Key Concepts

- **Local Markdown knowledge base**: Research, summaries, references, and drafts are stored as local `.md` files instead of being spread across browser tabs, chat logs, and presentation tools. This improves portability, searchability, version control, and reuse.
- **AI-assisted research**: CLI-oriented AI tools such as Claude Code or Codex can help gather information, summarize documentation, and reshape notes into usable Markdown. Human verification remains necessary for important claims and source fidelity.
- **Markdown-native slide authoring**: Slidev turns Markdown into presentation decks using frontmatter, slide separators, layout directives, and themes. The deck becomes a structured text file rather than a binary presentation artifact.
- **Obsidian as a unified workspace**: Obsidian serves as the main interface for reading, linking, editing, and refining both research notes and the final deck. This reduces context switching and supports iterative writing.
- **AI as a transformation tool**: Instead of asking AI to invent an entire presentation from scratch, the workflow uses AI to edit and improve existing source-grounded files, such as rewriting paragraphs into bullets or adding Slidev syntax.
- **Integrated research-to-deck pipeline**: Because research and slides are both text, content can move directly from notes into the presentation. This improves traceability and reduces the need to repeatedly repackage context for prompts.

## How It Works

The workflow begins with research captured as local Markdown files. Notes include facts, summaries, references, and links, all stored in a directory structure that AI tools can inspect directly. This keeps the source material close to the final output and avoids burying key context in transient chat sessions or disconnected apps.

From there, the presentation is authored as another Markdown file, usually a Slidev deck with frontmatter and slide delimiters. This keeps the authoring model consistent: research and presentation are just different representations of the same underlying knowledge. Obsidian acts as the workspace for browsing, cross-referencing, and editing both.

A practical benefit of this approach is that AI can operate on explicit files rather than vague prompts. That makes tasks like converting a rough outline into slides, adding a comparison table, rewriting dense text into concise bullets, or applying Slidev-compatible formatting much easier and more controllable. The AI is acting like a copilot for structured text transformation, not a black-box deck generator.

This setup is especially well suited to technical users, independent consultants, developer advocates, and anyone who prefers text-first workflows. It is less ideal when the environment depends heavily on enterprise coauthoring, formal review workflows, or strict PowerPoint-native compatibility. In those cases, Markdown may still be useful upstream, but extra export or collaboration steps will likely be needed.

The central idea is simple: if both research and slides live as text, then AI can assist across the full pipeline without repeated copy-paste or prompt reconstruction. The deck becomes a direct transformation of the knowledge base.

## Personal Notes

Building AI-Assisted Markdown Presentations with Obsidian and Slidev

Source: https://www.linkedin.com/posts/jukkaniiranen_people-often-ask-me-how-i-build-my-presentations-share-7456019772883820545-bWY0?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY
Notion page: https://app.notion.com/p/Building-AI-Assisted-Markdown-Presentations-with-Obsidian-and-Slidev-35301bb0839a81cd8c4ed3583326a5a8

Tags: markdown, slidev, obsidian, ai-tools, presentations

Overview

This lesson explains a lightweight workflow for creating presentations without PowerPoint by keeping both research notes and slide decks as local Markdown files. The source describes a practical setup where CLI-based AI tools help gather and reshape knowledge, Obsidian provides the editing environment, and Slidev turns Markdown into a themed presentation.

This matters to engineers, technical consultants, developer advocates, and solo operators who already think in text files and want presentation creation to feel more like software development than manual slide design. The core idea is to keep knowledge capture, synthesis, and final output in the same textual workflow so that research and presentation generation are tightly connected.

Key Concepts

  *   Local Markdown knowledge base: Instead of scattering research across browser tabs, chat histories, and presentation notes, the workflow stores findings as local .md files. This makes knowledge portable, searchable, versionable, and easy to reuse across future projects.
  *   AI-assisted research: CLI-based AI tools such as Claude Code or Codex are used to accelerate research and summarize reference material into Markdown. The human still validates important claims against source links because hallucinations remain a real risk.
  *   Markdown-native slide authoring: Slidev treats presentations as Markdown documents with frontmatter, layout syntax, and theming. This means slide creation is no longer a separate binary format or GUI-driven process but an extension of the same writing workflow used for research.
  *   Obsidian as a unified workspace: Obsidian acts as the reading and editing interface for both source notes and the final deck. Using one environment reduces context switching and encourages iterative refinement from raw notes into polished slides.
  *   AI as a formatting and transformation agent: The author does not memorize every detail of Slidev syntax and instead uses coding agents to make structural and styling changes. AI is used less as a one-shot deck generator and more as a copilot that edits files already grounded in the source material.
  *   Integrated research-to-deck pipeline: A major benefit of this approach is that deck creation is not detached from knowledge gathering. The same source material that informed the analysis can be directly transformed into slides, preserving traceability and reducing prompt packaging overhead.

How It Works

The workflow starts with research, not slide design. Instead of collecting ideas directly inside a presentation tool, the user works with local Markdown documents that contain notes, summaries, references, and supporting links. AI tools help accelerate this phase by extracting useful details from documentation or other technical references and storing the results in human-readable files.

A key design choice is that the knowledge stays local and file-based. This has several practical benefits:

- notes can be reorganized without losing context - source links can be preserved next to claims - content can be reused across blog posts, talks, and customer deliverables - AI tools can operate directly on a directory of files instead of requiring long prompt context windows

Once research is complete, the same Markdown-first mindset continues into presentation authoring. Rather than exporting notes into PowerPoint or asking an AI assistant to invent a deck from scratch, the presentation itself is created as a Markdown file using Slidev. In Slidev, a deck typically contains frontmatter at the top, then slide content separated by delimiters. Conceptually, the deck becomes another structured text artifact derived from the research notes.

A minimal Slidev-style document looks like this:

```md --- theme: default title: AI-Assisted Presentation Workflow ---

# AI-Assisted Presentation Workflow

From research notes to slides in Markdown

--- layout: section ---

# Why Markdown?

- Easy to version - Easy to search - Easy for AI tools to edit

---

# Workflow

1. Research with AI 2. Store findings in local `.md` files 3. Summarize into a Slidev deck 4. Refine styling and layout ```

Obsidian is used as the main interface for interacting with these files. That means the user can browse research notes, open the slide deck, cross-reference source material, and make edits in one environment. This is especially useful for solo work, where speed and coherence matter more than multi-user collaboration workflows.

The role of AI here is specific and practical. Rather than depending on a generic "make me a slide deck" prompt, the author uses coding-oriented AI agents to manipulate Markdown files directly. For example, the AI might:

- convert a rough outline into Slidev slide separators - add frontmatter and layout directives - rewrite dense paragraphs into speaker-friendly bullets - insert HTML snippets for better visual structure - adjust theming or formatting based on a design request

This is a meaningful distinction from many AI deck generators. In the described workflow, AI operates on explicit source files that already contain curated research. That reduces the disconnect between knowledge gathering and presentation output, and it gives the user better control over accuracy, structure, and revision.

The tradeoff is that this workflow favors technically inclined users and independent creators. It works best when you are comfortable with files, Markdown, and iterative editing. If your environment depends heavily on enterprise review workflows, live coauthoring, or strict PowerPoint compatibility, you may need additional export and collaboration steps.

The central reasoning from the source is straightforward: if research and final presentation are both text, then AI tools can help at every stage without forcing repeated copy-paste or brittle prompt reconstruction. The deck becomes a transformation of your knowledge base, not a disconnected artifact.

Training Exercise

Create a small Markdown-native presentation pipeline