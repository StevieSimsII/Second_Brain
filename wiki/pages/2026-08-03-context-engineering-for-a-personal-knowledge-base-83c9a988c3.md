---
title: "Context Engineering for a Personal Knowledge Base"
source: "https://www.youtube.com/watch?v=gQeRjkb_Hlc"
date: "2026-08-03"
tags: [ai-agents, context-engineering, knowledge-management, prompting]
source_type: "youtube"
source_fingerprint: "83c9a988c3"
source_characters: 28816
---

## Overview

This lesson distills a YouTube transcript about "new rules" for working with Claude-style coding agents. The core takeaway is that stronger models may need less rigid prompting and more structured context design: thin top-level routing, selective loading of files, lightweight tool descriptions, richer reference artifacts, and deliberate memory capture. Evidence in the source is partly second-hand: the speaker summarizes an Anthropic engineer's article and mixes it with examples from his own workspace.

## Key Concepts

- **Context engineering**: A model's output depends on more than the current prompt. In the source, context includes connected applications and tools, recurring routines, stored memory, and reusable skills or procedures.
- **Judgment over rigid rules**: The transcript argues that newer models can perform better when given higher-level guidance instead of many narrow rules. The practical implication is to describe intent and style, then let the agent adapt to local context.
- **Design interfaces instead of many examples**: Rather than constraining the model with repeated examples, the source recommends giving it a design system or brand interface. This preserves consistency while still allowing exploration.
- **Progressive disclosure**: Do not front-load every rule and reference into one giant root file. Use a thin top-level router that points to sub-routers and only load detailed context when the task actually needs it.
- **Token efficiency**: A thinner always-loaded instruction file reduces repeated token spend at session start. The lesson is operational as much as conceptual: better context structure can improve both cost and responsiveness.
- **Automatic and deliberate memory**: The transcript claims newer tooling can save useful memories automatically, but the speaker still recommends explicit end-of-session review to update skills, memory files, and workflow docs when the session produced durable learning.
- **Richer references**: Markdown is still useful, but the source argues that newer models can work with more expressive artifacts such as HTML. These can be better for visual systems like brand books, infographics, and interface specs.

## How It Works

Treat your knowledge base as a layered context system. Start with a small root instruction file whose job is routing, not storing every rule. Under that, create domain-specific index files for areas like content, product, operations, or personal work. For each domain, store reusable skills, memory files, and references close to the work they support. When defining agent behavior, prefer short intent-level guidance over long rule lists, and prefer design systems over many copied examples. Keep tool descriptions simple unless the task truly needs more detail. When a concept is visual or structural, consider a richer artifact such as HTML instead of plain markdown. After productive sessions, capture durable learnings by updating memory or skills so the system improves over time. The six shifts presented in the transcript are: more judgment, design interfaces over examples, progressive disclosure over loading everything up front, less repetition in tool instructions, more automatic memory behavior, and richer references over simple specs.

## Training Exercise

Pick one area of your knowledge base, such as writing or research. Create a thin root router file with links to 3 sub-files only. In one sub-file, replace a long block of rules with 5-7 high-level principles. In another, replace example-heavy guidance with a small design interface or checklist. Then run the same task twice: once with your old setup and once with the routed setup. Compare output quality, token usage if visible, and how easily you can maintain the files. Finish by writing a short calibration note describing one rule, one memory, and one reference artifact you would keep.

## Further Reading

- [YouTube source video](https://www.youtube.com/watch?v=gQeRjkb_Hlc)
