---
title: "After Automation: Why Better AI Increases Demand for Expert Human Work"
source: "https://every.to/p/after-automation?utm_source=onboarding_email_bottom&utm_campaign=onboarding"
date: "2026-07-10"
tags: [ai, automation, knowledge-work, agents, benchmarks, human-in-the-loop]
---

## Overview

This lesson explains a practical paradox emerging in AI-heavy organizations: as automation improves, the amount of human work often increases rather than disappears. The article argues that modern AI makes previously scarce competence cheap, which expands output volume, but also creates more low-differentiation work that must be framed, reviewed, integrated, and improved by human experts.

This matters to engineers, product leaders, operations teams, and founders who are reorganizing work around coding agents and workflow automation. Instead of treating AI as a binary replacement for people, the piece offers a more operational model: AI excels inside frames humans provide, while human value shifts toward setting goals, judging outputs, maintaining systems, and creating the next layer of differentiation.

## Key Concepts

- **Agent employees**: The article distinguishes agents that act like delegated coworkers from humans collaborating live with AI. Agent employees can be invoked asynchronously to draft documents, triage support issues, or summarize discussions without requiring constant supervision. They are most effective on repeatable, well-scoped tasks with stable inputs and clear success criteria.
- **Human-agent collaboration**: A second and more important mode is synchronous collaboration in tools like Codex or Claude Code, where a human and one or more agents share the same workspace. In this mode, the human plans, redirects, reviews, and sequences work while the agent executes subtasks. The article calls this the human 'sandwich': the person frames the work at the beginning and validates it at the end.
- **Cheap competence**: Language models package the visible residue of past human expertise—code, prose, tickets, designs—into a broadly accessible system. That makes previously specialized output much cheaper to produce. As a result, more people can attempt tasks that used to require dedicated experts.
- **Commoditization and slop**: When many users rely on the same models and patterns, output tends to converge toward generic sameness. The article uses 'slop' to describe work that is superficially competent but lacks coherence, specificity, or originality. This makes raw output abundant, but lowers its differentiated value.
- **Frames vs framers**: Benchmarks measure model performance inside a frame: a prompt, task definition, and evaluation setup chosen by humans. A framer is the human who decides what problem matters, what constraints apply, and what counts as success. The core claim is that models can optimize within frames, but that does not eliminate the need for humans to define and revise those frames.
- **Benchmark saturation**: As models improve on a benchmark, they make the measured task cheaper and more widely attempted. But once a benchmark is saturated, humans shift to a harder framing of the same domain, such as moving from 'can the model rewrite code?' to 'when should a rewrite happen, with what scope and migration plan?'. This creates a repeating cycle where automation expands demand for expert judgment.

## How It Works

The article builds its argument from observed workflows inside Every, a company that heavily uses AI across coding, writing, design, support, and email. The central observation is that extensive automation has not removed the need for human workers. Instead, it has changed the shape of work.

The operational model has two layers:

1. **Delegated agents**
   - Slack-style coworker agents handle tasks like proposal drafting, digest creation, metrics analysis, and memo generation.
   - Embedded agents sit inside a workflow like customer support and handle repetitive front-line interactions.
   - These systems reduce toil, but they require setup, monitoring, maintenance, and escalation paths.

2. **Interactive collaboration environments**
   - Tools like Codex and Claude Code act as a shared operating environment for complex work.
   - The human stays in the loop, steering the process, checking quality, and deciding what the next subproblem is.
   - This mode is especially important for open-ended tasks such as coding, writing, and cross-functional decision-making.

A key practical claim is that agents work best when the problem is stable and the frame is already well defined. For example, a support agent can classify and close routine tickets because the workflow, policies, and desired outputs are fairly explicit. But as soon as the task becomes ambiguous or high stakes, human involvement becomes necessary to:

- choose the target problem
- supply context the model does not naturally have
- spot incorrect or low-quality outputs
- turn draft output into a real business decision
- maintain the automation itself

The article then explains **why more automation creates more human work**.

First, AI makes yesterday's expertise cheap. Because models are trained on the recorded outputs of human work, they can reproduce common forms of that work at low cost. That means more employees can now generate code, content, designs, and analyses.

Second, cheap competence gets adopted widely. The volume of output grows because many more people can now perform tasks that used to be bottlenecked on experts.

Third, volume creates sameness. If everyone uses similar models and prompting habits, much of the resulting work becomes generic. This lowers the value of default model output.

Fourth, sameness increases demand for differentiation. Organizations now need experts not only to produce original work, but to review, sharpen, govern, and systematize the flood of AI-generated drafts.

This creates two kinds of new expert work:

- **Quality control and governance**: review queues, evals, CI checks, repo rules, prompt files, permissions, and workflow design.
- **Higher-order application**: using AI to tackle larger or more novel problems than were previously feasible.

The benchmark section reinforces the same idea. The article describes an internal 'Senior Engineer benchmark' where a coding agent is asked to perform a first-principles rewrite of a broken codebase. A model score on that benchmark looks like a measure of raw intelligence, but the author argues it is actually a measure of the model operating within a carefully chosen frame.

That frame includes:

- the exact prompt
- hints embedded in the prompt
- the structure of the codebase
- the stopping conditions
- the grading process
- helper logic, such as automated prodding when the model stalls

This matters because benchmark gains are real but easy to overinterpret. If a model gets dramatically better at one framed task, that lowers the cost of doing that task. Then more people attempt it, which exposes additional decisions that were previously hidden inside expert judgment.

For example, if 'rewrite the app from first principles' becomes cheap, the next hard problems become:

- whether a rewrite should happen at all
- what should be preserved
- how migration works
- how to review the result
- what rollback looks like
- how existing data and users are affected

So the measured task gets cheaper, but the surrounding expert decisions become more visible and more valuable.

The article generalizes this into a repeatable loop:

```text
human expertise -> captured as corpus -> model makes it cheap -> adoption expands -> output becomes abundant
-> generic output loses value -> experts move upstream/downstream
-> humans define new frames and constraints -> models improve inside those frames
-> cycle repeats
```

The final argument is that even in a future with AGI-like systems, this framing problem remains. A highly capable model may choose strategies and optimize over long horizons, but it is still generally pursuing goals supplied by humans or organizations. The system can operate within frames and perhaps move between them, but the human role of deciding what matters now, in this situation, for this business or customer, does not disappear so easily.

For working engineers, the practical takeaway is not 'AI can never replace tasks.' It is: the more your team automates execution, the more valuable become the skills of framing problems, building guardrails, evaluating outputs, and integrating AI work into live systems.

## Training Exercise

Build a small team workflow analysis to identify where AI creates more expert work rather than less.

### Goal
Map one real workflow in your team into:
1. tasks that can be delegated to an agent,
2. tasks that require human-agent collaboration,
3. expert judgments that become *more* important after automation.

### Step 1: Pick a workflow
Choose one concrete process, such as:
- bug triage
- pull request creation and review
- customer support escalation
- incident postmortem drafting
- product spec creation

### Step 2: Break it into stages
List 5-10 steps in the workflow. Example for PR delivery:
- clarify the problem
- inspect the codebase
- implement changes
- run tests
- review architecture impact
- merge and deploy
- monitor regressions

### Step 3: Classify each step
Create a table like this:

```text
| Step | Delegated agent? | Human-AI collaboration? | Human expert judgment needed? | Why? |
|------|-------------------|-------------------------|-------------------------------|------|
| Implement fix | Yes | Yes | Medium | Agent can code, but human validates approach |
| Decide if rewrite is needed | No | Yes | High | Requires tradeoff judgment and system context |
| Run regression tests | Yes | No | Low | Stable and automatable |
```

### Step 4: Identify the frame
For 2-3 steps, write the exact prompt or instruction you would give an agent. Then ask:
- What assumptions are hidden in this prompt?
- What context had to be decided before the prompt was possible?
- What would the model likely miss without a human reviewer?

### Step 5: Find the 'new expert work'
Write down at least 3 tasks that become more important *because* AI is now involved. Examples:
- defining repository rules
- improving test harnesses
- reviewing AI-generated diffs
- setting support escalation thresholds
- refining evaluation criteria

### Step 6: Run one live experiment
Use an AI assistant on a real but low-risk task. For example:

```text
Prompt: Review this module and propose whether we should patch the bug incrementally or do a structural rewrite. List the invariants we must preserve, the migration risks, and the tests required to validate the change.
```

Then compare:
- the raw AI answer
- your own review comments
- what additional context you had to inject

### Deliverable
Produce a 1-page summary with:
- the workflow you analyzed
- 3 tasks to automate now
- 3 places where human review is mandatory
- 2 new expert capabilities your team should build next

If you do this with your actual engineering process, you will directly see the article's thesis: automation removes some execution work, but increases the need for framing, evaluation, and systems design.

## Further Reading

- [OpenAI: GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)
- [Anthropic: Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [Herbert A. Simon - The Sciences of the Artificial](https://mitpress.mit.edu/9780262691918/the-sciences-of-the-artificial/)
- [Andrej Karpathy: Software Is Changing (talks and essays on AI-native development)](https://karpathy.ai/)