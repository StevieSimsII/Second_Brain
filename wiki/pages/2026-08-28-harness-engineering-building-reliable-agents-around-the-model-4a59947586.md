---
title: "Harness Engineering: Building Reliable Agents Around the Model"
source: "https://x.com/choopyplug1/status/2093037238850617742?s=12"
date: "2026-08-28"
tags: [ai-agents, software-engineering, automation, testing, observability]
source_type: "web"
source_fingerprint: "4a59947586"
source_characters: 2016
---

## Overview

This lesson is based on a social post summarizing a reported Google-team PDF on "harness engineering." The underlying PDF and article are not included here, so the evidence is thin: we can confidently teach the six-part framework described in the post, but not verify the benchmark details or broader claims. The core idea is practical: agent quality depends not just on the model, but on the surrounding system that guides, checks, remembers, constrains, and monitors it.

## Key Concepts

- **Agent = Model + Harness**: The post argues that the useful unit is not the model alone. An agent becomes reliable when the model is paired with supporting infrastructure.
- **Guides**: Files such as `AGENTS.md`, rule files, and constraint docs encode lessons from past failures so the system improves over time instead of repeating mistakes.
- **Sensors**: Linters, tests, and validation scripts act as automatic checks on the agent's output before a human reviews it.
- **Agentic Loop**: A practical loop is `plan -> execute -> verify -> fix`, with bounded retries, budget limits, and escalation when the agent gets stuck.
- **Externalized Memory**: Because the model does not retain durable memory across sessions, the harness must store state, decisions, and artifacts outside the model.
- **Permissions**: Safety and control come from the harness defining which tools may be used, how many writes are allowed, and what actions require approval.
- **Observability**: Tracking tool calls, retries, and cost helps detect drift and turns failures into debuggable system behavior rather than opaque model mistakes.

## How It Works

Treat the model as one component inside a controlled workflow. First, give it explicit written guidance drawn from real past errors. Next, require it to run checks on its own output with tests or validators. Then wrap its work in a loop that plans, performs the task, verifies results, and retries only within fixed limits. Store important state and artifacts outside the model so work can continue across sessions. Put a permission layer around tool use and risky actions. Finally, log what happened so failures can be inspected and converted into better rules or checks. The post's main lesson is that reliability comes from this surrounding harness, not from prompt wording alone.

## Training Exercise

Pick one small agent task, such as editing a file or drafting SQL. Write a short guide file with 5 rules, add 2 automatic checks, and define a loop with at most 2 retries plus an escalation condition. Store one artifact from each run, such as the plan or final diff, in a persistent location. After three runs, review failures and update the guide or checks. The goal is to observe whether system changes improve outcomes more than prompt changes alone.

## Further Reading

- [chuplung on X: Google's team just dropped a 9-page PDF on Harness Engineering](https://x.com/choopyplug1/status/2093037238850617742?s=12)
