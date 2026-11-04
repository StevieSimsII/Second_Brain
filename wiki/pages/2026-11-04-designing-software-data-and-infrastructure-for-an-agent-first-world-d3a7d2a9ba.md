---
title: "Designing Software, Data, and Infrastructure for an Agent-First World"
source: "https://www.youtube.com/watch?v=vl7HiMdGfjo"
date: "2026-11-04"
tags: [ai-agents, software-development, databases, product-design, entrepreneurship]
source_type: "youtube"
source_fingerprint: "d3a7d2a9ba"
source_characters: 52212
channel: "Y Combinator"
published: "2026-10-30"
duration_seconds: 2925
topics: [ai-agents, ai-strategy, coding-agents]
kind: "interview"
depth: 2
actionability: 2
---

## TL;DR

> As AI makes software creation accessible to more people, knowing what to build becomes more valuable than writing every line of code. Products serving this market must give agents code-first interfaces, actionable errors, durable user-owned data, and measurable feedback loops.

## Key Takeaways

1. Treat builders as a broader audience than professional developers: domain experts can now create niche and personal software without first recruiting an engineering team.
2. Keep personal data in a durable store of record that multiple applications and agents can use; otherwise, essential context becomes trapped inside one vendor or agent.
3. Design agent-facing products around code, CLIs, APIs, infrastructure as code, and sandbox compatibility—not only human-operated dashboards.
4. Make errors self-remediating by explaining the cause, the corrective action, and the relevant documentation so an agent can recover instead of abandoning the product.
5. Evaluate complete use cases across different models, then optimize correctness, retrieval quality, cost, and latency from real execution traces.
6. The Supabase CEO reports growth to 13 million sign-ups, nearly 50 million managed databases, and more than one million new databases per week; he attributes much of the inflection to AI-assisted building.
7. Choose durable problem categories, dogfood emerging workflows, preserve team capacity for experiments, and adapt quickly as development interfaces change.

## Key Moments

- [4:34](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=274s) — Why domain experts are becoming builders even without traditional software-engineering backgrounds
- [8:42](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=522s) — How personalized taxi, finance, and health applications become economically practical
- [12:12](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=732s) — Why a user-owned database can serve as the shared record beneath many agents
- [20:12](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=1212s) — How Supabase moved from dashboard-first to API-first and then code-first interfaces
- [27:29](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=1649s) — How dogfooding through conversation exposes the needs of personal agents
- [30:01](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=1801s) — How actionable errors and model evaluations help agents recover and complete tasks
- [36:20](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=2180s) — How traces, evaluation sets, and automated loops can continuously improve retrieval
- [45:41](https://www.youtube.com/watch?v=vl7HiMdGfjo&t=2741s) — Why durable categories, adaptability, and experimentation matter during rapid platform shifts

## Overview

AI-assisted development expands software creation from professional engineers to anyone who understands a problem well enough to describe and refine a solution. The conversation illustrates this shift with personal finance and health tools, a locally focused taxi application, and agent-managed knowledge systems that might previously have required a company or engineering team.

This matters to product teams, infrastructure providers, founders, and independent builders. The emerging design target is not simply a friendly interface for humans: it is an environment where agents can select tools, operate them through code, recover from errors, access user-owned context, and improve against explicit evaluations.

## Key Concepts

- **Builder**: A builder is anyone who can turn domain knowledge into working software with AI assistance, whether or not that person is a professional developer. The source argues that identifying the right problem is becoming a greater constraint than producing an initial implementation.
- **Personal software**: AI lowers the cost of creating applications that serve one person rather than a mass market. Such software can combine private context across finances, health, calendars, files, and relationships without needing to accommodate every user's preferences.
- **Personal database**: A personal database is a user-controlled system of record beneath applications and agents. It makes accumulated context portable and allows different interfaces or agents to operate on the same data instead of locking it inside one assistant.
- **Agent-first interface**: Agents generally work more effectively through machine-operable surfaces such as APIs, CLIs, code, and declarative configuration. Supabase describes evolving from a dashboard company to an API company and then to a code-first company as automated builders became more important.
- **Self-remediating errors**: An error should tell an agent what failed, why it failed, and how to correct it or locate the relevant documentation. This turns failure handling into part of the product interface and reduces the chance that an agent switches to another tool when it gets stuck.
- **Evaluation loop**: An evaluation loop converts representative tasks or production traces into repeatable tests of correctness, quality, cost, and latency. The Gbrain example describes agents repeatedly attempting improvements, retaining changes that improve scores, and documenting unsuccessful experiments.
- **Workload-tiered infrastructure**: Personal prototypes and large production systems do not require identical infrastructure. Copplestone describes a strategy spanning lightweight SQLite-compatible workloads through Postgres-compatible systems intended to scale toward very large data volumes, though these are company plans rather than independently established outcomes.
- **Adaptive product strategy**: Rapid platform shifts make fixed assumptions about interfaces and customers fragile. The proposed response is continual dogfooding, partnerships with ecosystem participants, spare capacity for experiments, and acceptance that many bets will fail.

## How It Works

1. Start with a concrete problem and the user's domain knowledge rather than a predetermined application category.
2. Give an agent access to machine-operable tools: code, APIs, CLIs, schemas, configuration, and isolated execution environments.
3. Store durable user context in a database or file store independent of any single agent.
4. Let the agent build a narrow workflow and observe where selection, execution, or recovery fails.
5. Rewrite errors so they include a diagnosis, a corrective action, and a documentation path.
6. Capture representative tasks or real traces as an evaluation set, including correctness, latency, retrieval quality, and cost.
7. Run improvement loops against those evaluations; keep measurable gains and record failed approaches.
8. Dogfood the experience conversationally, minimizing manual code intervention to reveal what a less technical builder would encounter.

## Training Exercise

Build and evaluate a tiny agent-first personal application.

1. Choose one narrow workflow, such as categorizing receipts, tracking workouts, or organizing reading notes.
2. Define a portable data model with three to five fields and store it independently from the chat or agent interface.
3. Ask an AI coding agent to create the workflow using only code, an API, or a CLI; avoid manually repairing its implementation during the first attempt.
4. Record every point where the agent gets stuck, including ambiguous commands, missing context, and unhelpful errors.
5. Rewrite one failure message so it states the cause, recommended fix, and verification step.
6. Create five representative evaluation cases, including one malformed input and one edge case. Score task correctness, latency, and any monetary or token cost.
7. Run a second implementation attempt with the improved interface, compare the scores, and document both successful and unsuccessful changes.
8. Finally, connect a second agent or interface to the same data store to verify that the user's data is portable rather than bound to the original agent.

## Test Yourself

<details><summary>Why does broader access to code generation increase the importance of domain expertise?</summary>

The mechanical ability to build is becoming easier to access, but selecting a valuable problem still requires knowledge of a particular workflow or industry. The discussion argues that domain experts can now implement ideas that previously failed because they could not recruit an engineer.

</details>

<details><summary>What makes an infrastructure product agent-first rather than merely usable by an agent?</summary>

An agent-first product exposes its capabilities through code, APIs, CLIs, and reproducible configuration. It also provides actionable errors and tests complete agent workflows so models can diagnose failures and continue without human dashboard intervention.

</details>

<details><summary>Why separate personal data from the agent currently using it?</summary>

A separate database preserves a durable store of record that can support several agents and applications. This reduces vendor lock-in and prevents relationships, files, health information, and routines from becoming inaccessible when the user changes agents.

</details>

## Further Reading

- [Apply to Y Combinator](https://www.ycombinator.com/apply)
- [Work at a startup](https://www.ycombinator.com/jobs)
