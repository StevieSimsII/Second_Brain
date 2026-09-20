---
title: "Designing Fast Decision Layers for Agentic Coding with Jev"
source: "https://www.youtube.com/watch?v=ScvXFi4MUSc"
date: "2026-09-20"
tags: [agentic-coding, model-routing, code-review, software-testing, ai-workflows]
source_type: "youtube"
source_fingerprint: "b14c599573"
source_characters: 34228
---

## Overview

Jev is presented as a fast decision model: instead of generating prose token by token, it evaluates user-defined answers and returns probabilities or a rubric-based score. This makes it suitable for frequent, narrowly scoped decisions such as routing work, screening code changes, classifying logs, or checking user flows. The lesson’s central pattern is to pair this inexpensive “System 1” decision layer with a slower, deliberative “System 2” coding model. Jev screens many candidates; thresholds and application logic automate clear cases, while uncertain or high-risk cases are escalated for deeper reasoning. Performance, accuracy, cost, and scale figures in the source are demonstrations or reported claims rather than independently verified benchmarks.

## Key Concepts

- **Structured decisions instead of generated text**: Jev receives text and predefined possible answers, then returns probabilities rather than an open-ended response. Application code can translate those probabilities into actions, making the model function like a semantic switch statement.
- **Three decision primitives**: Use bool for a yes-or-no proposition, score when an item belongs on an ordered rubric, and choice for mutually exclusive categories. The source reports up to 11 score levels, producing values from 0 to 10, and up to 255 choice options.
- **Criteria define operational meaning**: A label such as “risky” or “good” is underspecified until accompanied by criteria, descriptions, or examples. The invoice demonstration showed that adding explicit fraud signals changed the returned probability. Treat criteria as versioned decision policy rather than casual prompt text.
- **System 1 and System 2 collaboration**: The video uses “System 1” as an analogy for rapid, repeated classification and “System 2” for slower planning and investigation. A fast model handles local decisions; a deliberative model sets objectives, reviews outcomes, revises criteria, and resolves escalated cases.
- **Thresholded escalation**: Probabilities are not actions by themselves. Define confidence and risk thresholds: automate high-confidence, low-impact cases; request human or stronger-model review for ambiguity; and immediately escalate high-severity findings. Thresholds should be calibrated from observed outcomes rather than copied from a demonstration.
- **Qualitative software checks**: Potential checks include whether comments add useful information, names capture side effects, logs expose sensitive values, or diffs exhibit code smells. These are semantic checks that conventional syntax-oriented linters may not express well, but they should supplement—not automatically replace—static analysis, tests, and specialist review.
- **Broad screening, narrow deep review**: A decision model can cheaply ask many questions about a codebase or diff, shortlist the strongest findings, and send only those findings and relevant context to a larger coding model. The source proposes this for code review, security pipelines, skill selection, and adversarial browser testing, though several examples remain exploratory.

## How It Works

Start by selecting a bounded artifact such as a pull-request diff, log entry, code comment, or browser observation. Define one or more questions and choose the matching primitive. For bool, state exactly what qualifies as true. For score, write an ordered rubric whose levels have distinct meanings. For choice, provide exhaustive-enough categories, including an explicit review or uncertain category when appropriate.

Send the artifact and questions to the decision model. Store the returned probabilities or scores together with the input, policy version, selected action, and eventual outcome. Apply explicit routing logic—for example, accept a low-risk result, escalate a high-risk result, or route uncertain cases to a deliberative coding model or human reviewer.

The slower reviewer examines the shortlisted evidence, decides whether a change is needed, and can revise the criteria, examples, available choices, or thresholds. Re-run a representative sample after every policy change. This creates a feedback loop in which the fast layer performs repeated screening while the slower layer improves the decision policy.

For agentic coding, a practical pipeline is: use deterministic tests and static analysis first; run semantic screening on the remaining diff; rank findings by confidence and severity; escalate the most consequential findings; implement fixes with the coding agent; then verify again. Measure false positives, false negatives, latency, cost, and downstream defects before expanding coverage. Claims in the source about sub-second responses, fractional-cent jobs, large-scale browser testing, or major token savings should be validated in the intended environment.

## Training Exercise

Build a small qualitative review gate for one repository without changing production code. First, select 20–50 comments from recent diffs. Define three questions: (1) bool—“Does this comment merely restate the visible code?”; (2) score from 0 to 3—0 means misleading or obsolete, 1 means accurate but redundant, 2 means useful context, and 3 means essential rationale or constraint; (3) choice—keep, rewrite, remove, or human review. Write criteria and examples before evaluating anything.

Have a person independently label the sample, then run the decision layer and record every output, probability, latency, and disagreement. Choose thresholds only after inspecting the results—for example, automatically shortlist “remove” only when confidence is high, while routing borderline cases to review. Ask a deliberative model or reviewer to analyze false positives and false negatives and propose one criteria revision. Re-run the same frozen sample, compare the confusion matrix and review workload, and document whether the revision improved results. Do not automatically edit comments until the gate demonstrates acceptable behavior on a separate validation sample.

## Further Reading

- [Source video: Jev and System 1 decision models for agentic coding](https://www.youtube.com/watch?v=ScvXFi4MUSc)
