---
title: "GitHub Copilot CLI Through a Sample Book App"
source: "https://github.com/github/copilot-cli-for-beginners"
date: "2026-08-04"
tags: [github-copilot, command-line, developer-workflows, ai-assisted-development]
source_type: "github"
source_fingerprint: "58079a5a59"
source_characters: 15496
---

## Overview

This repository is a beginner course for learning GitHub Copilot CLI from the terminal. The material is organized as a sequence of Markdown chapters, and it uses a recurring book-collection sample app to teach installation, first prompts, multi-file context, code review, debugging, test generation, custom agents, reusable skills, MCP server integration, and end-to-end workflows. The evidence supports a documentation-first repository with runnable examples and sample code in multiple languages rather than a single production application.

## Key Concepts

- **Terminal-native AI workflow**: The course frames Copilot CLI as AI assistance that stays inside the terminal, so the learner can ask questions, review code, generate tests, and debug without switching to an editor or browser.
- **Progressive chapter design**: The repository is split into numbered chapters `00` through `07`, moving from quick start to combined workflows. Each chapter follows a repeated teaching pattern: analogy, core concepts, hands-on examples, assignment, and what comes next.
- **Context-aware conversations**: A full chapter is dedicated to context and conversations, including multi-file analysis and multi-turn interaction. That signals an important lesson: Copilot CLI becomes more useful when you provide the right project context, not just isolated prompts.
- **Workflow-oriented usage**: The course emphasizes practical development tasks such as code review, debugging, refactoring, Git integration, and test generation. The goal is not only asking questions, but fitting AI into normal engineering loops.
- **Custom agents and instructions**: The repository includes agent files such as `.github/agents/python-reviewer.agent.md` and chapter content about specialized assistants. This shows that the CLI can be guided with role-specific behavior instead of relying only on generic prompts.
- **Reusable skills and MCP integration**: Later chapters and sample files cover skills and MCP servers, including `SKILL.md` examples and `samples/mcp-configs/mcp-config.json`. The practical idea is extending the CLI with reusable capabilities and external system connections.

## How It Works

Observed architecture: the root contains course documentation (`README.md`, chapter folders `00-quick-start` through `07-putting-it-together`, and appendices), repository policy files, and a large asset library of screenshots, GIFs, and diagrams. Sample material is separated under `samples/`, including a Python book app (`samples/book-app-project`), a buggy Python variant, a JavaScript book app, a C# book app with tests, buggy code examples in Python and JavaScript, sample agents, sample skills, and a small `src` tree with API, auth, components, models, services, and utilities. The repository also contains `.github/agents`, `.github/skills`, Copilot instructions, automation scripts, and workflow files, which suggests the course itself is maintained with supporting tooling. A practical way to use the lesson is to follow the chapters in order while inspecting the sample projects: start by verifying setup in `00-quick-start`, use `01` and `02` to practice prompt and context habits, apply `03` on the buggy and tested sample code, then study `04`, `05`, and `06` to see how agents, skills, and MCP servers expand the base CLI workflow.

## Training Exercise

Open the repository's Python sample at `samples/book-app-project` and the buggy variant at `samples/book-app-buggy`. First, write down three concrete questions you would ask Copilot CLI about the code structure, data flow, and likely failure points. Next, compare those questions with the course progression: use the mindset of chapter `02` for context gathering, then chapter `03` for debugging or test generation. Finish by drafting one custom agent idea and one reusable skill idea that would help maintain the book app repeatedly. Your success criterion is not a perfect answer from the model, but whether your prompts become more specific, context-rich, and workflow-oriented across the exercise.

## Further Reading

- [GitHub Copilot CLI for Beginners Repository](https://github.com/github/copilot-cli-for-beginners)
- [Official Copilot CLI Documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli)
- [GitHub Copilot CLI Command Reference](https://docs.github.com/en/copilot/reference/cli-command-reference)
- [GitHub Copilot CLI Getting Started](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)
- [About GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [Awesome Copilot Learning Hub Version](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/)
