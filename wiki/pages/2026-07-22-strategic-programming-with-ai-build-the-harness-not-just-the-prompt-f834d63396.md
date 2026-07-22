---
title: "Strategic Programming With AI: Build the Harness, Not Just the Prompt"
source: "https://www.youtube.com/watch?v=nQwJVHCtDDY"
date: "2026-07-22"
tags: [software-design, ai-agents, developer-tooling, prompting, engineering-management]
source_type: "youtube"
source_fingerprint: "f834d63396"
source_characters: 65724
---

## Overview

This lesson argues that the highest-leverage way to improve AI-assisted software development is not obsessing over the newest model, but improving the harness around it: task scoping, codebase design, tests, documentation, skills, and execution environment. The source presents this mainly as practitioner opinion and workflow advice rather than controlled evidence. The central claim is that AI is strongest at tactical programming work, so humans gain more by staying responsible for strategy, architecture, product intent, and system improvement.

## Key Concepts

- **Strategic vs. tactical programming**: Using John Ousterhout’s distinction, the speaker frames tactical work as writing code, fixing syntax, and handling local bugs, while strategic work is shaping architecture, interfaces, task boundaries, and long-term velocity. The lesson’s core recommendation is to let AI absorb more tactical work while the human stays accountable for strategic decisions.
- **Harness over model**: The speaker repeatedly argues that teams over-focus on the model and under-focus on the surrounding system. In this lesson, 'harness' includes prompts, skills, sandboxing, codebase quality, tests, documentation, and review loops. The claim is not that models do not matter, but that harness quality is more controllable and often more durable than model-specific tuning.
- **Procedure skills vs. ability skills**: The source distinguishes between skills the user explicitly invokes ('procedures') and skills the model may invoke on its own ('abilities'). The speaker prefers procedures because they keep the human in control and avoid leaking many skill descriptions into the context window. A short 'grill me' skill is given as an example of a lightweight, high-leverage procedure.
- **Stateful teaching workflows**: The demonstrated 'teach' skill is described as stateful because it stores mission context, learning records, references, and lessons in the workspace. The educational idea is that a good teacher should remember the learner’s goal, current level, and prior progress rather than treat each interaction as stateless prompting.
- **AFK agents, queues, and checkpoints**: The speaker prefers 'away-from-keyboard' agent work for scoped tasks, especially when run in sandboxes or CI. He pushes back on hype around endless 'agentic loops' and instead describes software work as a queue of tasks with human-in-the-loop checkpoints placed as far to the right as safety allows.
- **Agent experience (AX)**: Alongside developer experience (DX), the source introduces 'agent experience': how easy a codebase is for an AI agent to navigate and change safely. Better architecture, clearer boundaries, useful docs, and stronger tests are presented as improvements that help both humans and agents.
- **Self-improving systems**: When an AI finds a bug or security issue, the recommended response is not just to patch that instance but to ask why the system allowed it. The speaker treats review, tests, refactoring, recurring audits, and richer observability as feedback loops that improve the harness over time.

## How It Works

Use AI as a scalable tactical workforce, but do not delegate product vision or architectural judgment. Start with a clean setup rather than a bloated one: remove unnecessary skills, plugins, and global instructions, then observe the agent’s default behavior. Add back only the procedures you can justify. Scope tasks tightly, design interfaces up front, and give the agent a codebase that is easy to change. Prefer AFK execution for bounded tasks, ideally inside sandboxes and automation systems such as GitHub Actions, but keep human review checkpoints for risky or poorly understood changes. Treat every surprising success or failure as harness feedback: if an agent found a deep bug, improve the review, testing, or auditing system so similar issues are found systematically next time. Several concrete examples in the source support this workflow, including a stateful 'teach' skill that generates HTML lessons and a sandbox-based setup for parallel agent execution. Broader claims, such as seniors getting '10x' more value from AI or tactical programming being 'gone,' are presented as experience-based opinions, not formal evidence.

## Training Exercise

Create a small repo or scratch workspace and run this five-step harness audit. 1. Write a `mission.md` with one concrete software goal, success criteria, and the user problem. 2. Remove optional AI setup bloat: extra skills, plugins, or standing instructions you cannot justify. 3. Pick one narrow task and write a brief that specifies scope, interfaces to touch, tests to run, and what not to change. 4. After the task is completed, review not only the code change but the process: where did the agent hesitate, waste tokens, or need clarification? 5. Make one harness improvement based on that review, such as better docs, a clearer interface, a regression test, or a reusable procedure skill. Repeat this on three tasks and compare whether later tasks require less steering.

## Further Reading

- [Source video](https://www.youtube.com/watch?v=nQwJVHCtDDY)
- [AI Hero](https://aihero.dev)
- [AI Hero Skills](https://aihero.dev/skills)
