---
title: "Agentic software delivery across models, repositories, tools, and Git"
source: "https://www.youtube.com/watch?v=xbCa0aa4tRM"
date: "2026-11-03"
tags: [github, developer-tools, ai-agents, software-delivery, code-review, git]
source_type: "youtube"
source_fingerprint: "aa911d4212"
source_characters: 9727
channel: "GitHub"
published: "2026-10-29"
duration_seconds: 474
topics: [ai-agents, coding-agents, github-copilot, automation-workflows]
kind: "news"
depth: 2
actionability: 2
---

## TL;DR

> GitHub is turning Copilot into a multi-agent delivery system that can choose models, coordinate work across repositories, and preserve sessions across devices and tools. Supporting this workflow requires not only agent interfaces but also stronger review, security, and Git infrastructure built for highly parallel activity.

## Key Takeaways

1. Treat multi-repository features as coordinated projects: Copilot Projects assigns agents to the repositories where each part of the work belongs.
2. Use Copilot Fusion’s single, cascade, and critique patterns to match model orchestration to the task rather than applying one model configuration everywhere.
3. Preserve task continuity through cloud sandboxes so work can begin on a phone and continue in the Copilot app, VS Code, the CLI, or GitHub.com.
4. Keep security and review in the agent workflow: code scanning identifies vulnerabilities, while Code Review Max targets deeper review of high-severity issues.
5. Design source-control infrastructure for concurrent agents; GitHub reports that branch-level write locking produced three to four times more write throughput than repository-wide locking.
6. Evaluate benchmark announcements carefully: GitHub reports Fusion Max scored 60 on Artificial Analysis’s Coding Agent Index at half the cost and 40% less time per task than the cited comparison, but the keynote does not provide the underlying methodology.

## Key Moments

- [0:45](https://www.youtube.com/watch?v=xbCa0aa4tRM&t=45s) — See how the Copilot app and reusable connectors unify agents with external services.
- [1:26](https://www.youtube.com/watch?v=xbCa0aa4tRM&t=86s) — Learn how Fusion chooses among single, cascade, and critique execution patterns.
- [2:06](https://www.youtube.com/watch?v=xbCa0aa4tRM&t=126s) — Watch Projects distribute a feature across agents and multiple repositories.
- [3:43](https://www.youtube.com/watch?v=xbCa0aa4tRM&t=223s) — Follow a cloud-sandbox task from a phone to other Copilot surfaces.
- [4:55](https://www.youtube.com/watch?v=xbCa0aa4tRM&t=295s) — See scanning and deeper code review integrated into the development loop.
- [5:51](https://www.youtube.com/watch?v=xbCa0aa4tRM&t=351s) — Understand why GitHub replaced repository-wide write locks with branch-level locking.
- [7:20](https://www.youtube.com/watch?v=xbCa0aa4tRM&t=440s) — Connect the app, orchestration, continuity, review, and Git changes into one agentic delivery stack.

## Overview

The keynote presents an agentic software-delivery stack rather than a single coding assistant. Its layers include a dedicated Copilot app, connectors to external systems, model orchestration through Copilot Fusion, multi-repository coordination through Copilot Projects, portable cloud sessions, automated security and review, and redesigned Git infrastructure.

The lesson matters to engineering teams adopting agents at scale: better model output alone is insufficient. Useful systems must carry context across services and interfaces, divide work without excessive supervision, validate generated changes, and absorb many concurrent Git operations.

## Key Concepts

- **Copilot app and connectors**: The Copilot app is presented as one place to operate agents across projects, tools, and automations. Managed connectors authenticate services such as Slack, Work IQ, Vercel, Netlify, and Sentry once, then make them available across supported Copilot surfaces.
- **Copilot Fusion**: Fusion coordinates multiple models and selects an execution pattern based on the task. The three named patterns are single, cascade, and critique, representing one-model execution, staged execution, and model-based evaluation or refinement.
- **Copilot Projects**: Projects supplies multiple repositories as shared context for a larger objective. Copilot creates the required agents and assigns work according to the repository involved, reducing the need to micromanage individual sessions.
- **Cross-surface continuity**: A task can start on a phone inside a cloud sandbox and later continue in the Copilot app, VS Code, the CLI, or GitHub.com. A common Copilot harness underpins this continuity; the presenters also say the harness can be used to build agents through Microsoft Foundry.
- **Security and automated review**: GitHub code scanning examines new and existing code for vulnerabilities and provides location, category, and remediation information. The presented safety stack also includes secret scanning, AI push protection, Copilot code review, and the deeper Code Review Max tier.
- **Agent-driven Git load**: Every agent session may read history, create branches, and push changes, often concurrently with other agents. This shifts scaling pressure from the assistant interface to the underlying repository infrastructure.
- **Branch-level write locking**: GitHub says its former architecture locked an entire repository for each write, limiting parallel work. The rebuilt system locks only the branch being updated, allowing agents on separate branches to proceed concurrently; GitHub reports three to four times greater write throughput.

## How It Works

1. Define a feature or incident as a project and attach every relevant repository.
2. Bring operational context into the workflow through managed connectors such as Slack, Sentry, or deployment platforms.
3. Let Fusion select a single, cascade, or critique execution pattern based on the task.
4. Use Projects to create and assign agents across the repositories involved.
5. Run sessions in cloud sandboxes so developers can switch devices and interfaces without discarding progress.
6. Inspect proposed changes with code scanning, secret scanning, push protection, and code review before merging.
7. Store each agent’s work on separate branches, allowing the branch-level Git architecture to process independent writes in parallel.
8. Judge the combined outcome—not merely individual agent responses—using correctness, security findings, review quality, elapsed time, and cost.

## Training Exercise

Design a small agentic workflow without requiring access to the announced products:

1. Choose a feature that spans two repositories, such as an API change plus a client update.
2. List the external context needed from issue tracking, monitoring, chat, and deployment systems; mark which items would be supplied through connectors.
3. Split the feature into repository-specific agent tasks and define the contract between them.
4. Assign each task a Fusion-style pattern: single for straightforward work, cascade for staged work, or critique when independent review is valuable.
5. Give every task its own branch and write down how parallel pushes avoid interfering with one another.
6. Create a handoff record containing the goal, repository, branch, current status, evidence, and next action; verify that another developer could resume it from a different interface.
7. Add gates for vulnerability scanning, secret detection, automated review, tests, and human approval.
8. Evaluate the design by asking where context could be lost, where agents could conflict, and which claim would require a real benchmark before adoption.

## Test Yourself

<details><summary>Why is Copilot Projects more than a chat interface with several repositories attached?</summary>

It treats a cross-repository objective as coordinated work, creating as many agents as needed and assigning each agent according to the repository where its task belongs. The developer focuses on the combined result instead of manually directing every agent.

</details>

<details><summary>How do cloud sandboxes and a shared Copilot harness improve an agent workflow?</summary>

A cloud sandbox preserves the running session independently of the current device. The shared harness then lets the developer continue that task through the Copilot app, VS Code, the CLI, GitHub.com, or another supported surface.

</details>

<details><summary>Why did increased agent activity require architectural changes beneath Copilot?</summary>

Agent sessions create branches, read history, and push changes concurrently, which amplifies pressure on Git. GitHub says moving from repository-wide locks to branch-level locks allows independent branches to progress in parallel and raises write throughput.

</details>

## Further Reading

- [GitHub Universe 2026 sessions and technical deep dives](https://githubuniverse.com)
- [More GitHub Universe 2026 videos](https://www.youtube.com/watch?v=AArI948SDz8&list=PLENrlACZ7mnU)
- [GitHub Blog](https://github.blog)
