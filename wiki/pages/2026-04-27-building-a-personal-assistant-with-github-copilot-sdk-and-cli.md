---
title: "Building a Personal Assistant with GitHub Copilot SDK and CLI"
source: "personal notes"
date: "2026-04-27"
tags: [github-copilot, cli, sdk, ai-agents, developer-tools]
---

## Overview

These notes describe how to build a practical personal engineering assistant using GitHub Copilot CLI and the Copilot SDK. The emphasis is on moving from passive AI assistance toward an orchestrated workflow where a user states intent, the assistant gathers context, optionally uses tools, and returns a reviewable result such as a command suggestion, summary, or next action.

This approach matters because many software and DevOps workflows already happen in the terminal and around repositories, logs, and build systems. A useful assistant is therefore not just a chatbot; it is a system shaped by prompts, context injection, tool access, and safety guardrails. Understanding that structure helps when designing automations that are more reliable, transparent, and controllable than ad hoc scripts or unconstrained chat interactions.

## Key Concepts

- **Copilot CLI**: Brings AI-assisted interactions into the terminal.
- **Copilot CLI**: Useful for generating commands, explaining shell usage, and translating natural-language requests into terminal actions.
- **Copilot CLI**: Fits naturally into workflows like Git operations, diagnostics, test runs, and deployment checks.

- **Copilot SDK**: Provides the programmable layer for custom assistant behavior.
- **Copilot SDK**: Lets you define prompts, pass context, expose tools, and shape responses.
- **Copilot SDK**: Enables building specialized assistants instead of relying on a fixed product interface.

- **Personal assistant workflow**: More than chat; it accepts a goal, collects context, uses tools when needed, and returns an actionable output.
- **Personal assistant workflow**: In engineering, this often combines repository state, docs, logs, shell commands, and user preferences.
- **Personal assistant workflow**: A good workflow is iterative and grounded in the current environment.

- **Tool-augmented AI**: Extends an LLM with external capabilities like shell commands, file access, Git inspection, APIs, or search.
- **Tool-augmented AI**: This is what makes the assistant operational rather than purely conversational.
- **Tool-augmented AI**: Tool access should be constrained and intentionally designed.

- **Context management**: Assistant quality depends heavily on supplied context.
- **Context management**: Relevant context includes current directory, repository contents, task history, logs, conventions, and branch status.
- **Context management**: Better context reduces hallucinations and improves relevance.

- **Human-in-the-loop safety**: Users should remain in control of execution.
- **Human-in-the-loop safety**: Command previews, confirmations, and scoped permissions are key safeguards.
- **Human-in-the-loop safety**: Especially important when an assistant suggests shell commands or file changes.

## How It Works

The lesson frames a personal assistant as a three-layer system:

1. **User interaction layer**: the developer expresses intent in natural language from the editor or terminal.
2. **Assistant orchestration layer**: SDK-backed logic interprets the request, builds prompts, gathers context, and decides whether tools should be used.
3. **Execution/tool layer**: shell commands, filesystem reads, repository inspection, or API calls produce concrete outputs the assistant can summarize or transform.

A useful mental model is an assistant loop:

- accept a request
- collect relevant context
- reason over the request plus context
- optionally propose actions or commands
- return a result for user review or execution

In the Copilot CLI scenario, the terminal is the main control surface. This is powerful because many engineering tasks already live there: Git, builds, tests, setup, diagnostics, and deployment checks. The SDK adds customization so the assistant can be specialized to a repository, workflow, or team convention instead of acting like a generic helper.

A typical request path might look like this:

- user asks: “Create a changelog from commits since the last tag.”
- assistant applies a role instruction such as “You are a release engineering assistant.”
- context providers gather Git history, latest tag, branch, and version files
- tool adapters call Git or read files
- assistant returns a draft changelog and a safe command suggestion

The key implementation lesson is separation of concerns. Even a small prototype benefits from splitting responsibilities into modules such as:

- **command interface** for parsing CLI input
- **assistant service** for prompt building and model interaction
- **context providers** for Git state, logs, config, docs, and shell state
- **tool adapters** for shell, Git, file operations, or APIs
- **output formatter** for plain text, markdown, or command previews

This structure improves testability and safety. For example, tool adapters can be mocked so tests do not run real commands. It also makes guardrails easier to enforce, such as explicit approval before execution.

The prototype exercise in the notes follows that philosophy. It asks for a terminal-based assistant that:

- accepts a natural-language task
- collects local Git context
- sends the request plus context to an assistant layer
- prints a command suggestion and explanation
- requires manual approval before execution

The example implementation uses:
- an `assistant_spec.md` file to define system behavior
- a `context.sh` script to collect working directory, Git status, and recent commits
- a Python driver script to assemble the prompt and display the next step
- a manual approval step before any command is executed

The main design takeaway is that usefulness comes from the surrounding system, not from the model alone. Prompt design, context quality, available tools, and safety boundaries determine whether the assistant is genuinely helpful in day-to-day engineering work.

## Personal Notes

Building a Personal Assistant with GitHub Copilot SDK and Copilot CLI

Source: https://youtu.be/5TN6l7JGWvs?si=NjdhRQXb45iSfg2s
Notion page: https://www.notion.so/Building-a-Personal-Assistant-with-GitHub-Copilot-SDK-and-Copilot-CLI-34f01bb0839a8148aadeee7eaff626a5

Tags: github-copilot, cli, sdk, ai-agents, developer-tools

Overview

This lesson explains how a developer can build a personal assistant experience using GitHub Copilot tooling, specifically the Copilot SDK and Copilot CLI. The core idea is to move beyond passive code completion and instead create an assistant that can accept intent, gather context, invoke tools, and help automate engineering workflows from the terminal and development environment.

This matters for engineers who want to operationalize AI inside their daily workflow rather than treat it as a chat-only interface. If you work in software development, DevOps, platform engineering, or internal tooling, understanding how an assistant is structured around prompts, context, commands, and tool execution will help you design practical automation that is safer and more useful than ad hoc shell scripts or generic chatbot usage.

Key Concepts

  *   Copilot CLI: Copilot CLI brings AI-assisted interactions into the terminal, where many engineering tasks already happen. It typically helps users generate commands, explain shell usage, and turn natural-language requests into concrete terminal actions.
  *   Copilot SDK: The SDK provides the programmable layer for building custom assistant behavior instead of relying only on a fixed product interface. With an SDK, you can define prompts, wire in tools, pass context, and shape how the assistant responds to user requests.
  *   Personal assistant workflow: A personal assistant is more than a chat bot: it accepts a goal, determines what context is needed, optionally calls tools, and returns an actionable result. In engineering scenarios, that often means combining repository context, terminal commands, documentation, and user preferences.
  *   Tool-augmented AI: Tool augmentation lets an LLM do useful work by invoking external capabilities such as shell commands, file access, APIs, or search. This is what turns a model from a text generator into a practical workflow assistant.
  *   Context management: The quality of the assistant depends heavily on what context it receives, such as current directory, repository contents, task history, or project conventions. Good context management reduces hallucinations and makes outputs more relevant to the user’s actual environment.
  *   Human-in-the-loop safety: When an assistant can generate or suggest commands, the user should remain in control of execution. Confirmation steps, command previews, and scoped permissions are important guardrails for preventing destructive or misleading actions.

How It Works

At a high level, building a personal assistant with GitHub Copilot tooling involves three layers:

1. **User interaction layer**: the developer expresses intent in natural language, often from the terminal or editor. 2. **Assistant orchestration layer**: the SDK-backed logic interprets the request, composes a prompt, gathers context, and decides whether to call tools. 3. **Execution/tool layer**: CLI commands, filesystem reads, repository inspection, or API calls produce concrete outputs that the assistant can summarize or transform.

A practical mental model is to treat the assistant as a loop:

- Accept a request such as "summarize the last failed build and suggest a fix" - Collect context such as current repository, Git status, logs, or CI output - Ask the model to reason over that context - Optionally generate a command or sequence of actions - Present the result to the user for review or execution

In a Copilot CLI scenario, the terminal is the natural control point. The user may type a natural-language instruction, and the CLI can turn that into a shell command, an explanation, or a scripted action. This is useful because many repetitive engineering tasks already live in the command line: Git operations, project setup, diagnostics, test execution, and deployment checks.

The SDK is where customization happens. Instead of accepting the default behavior of a generic assistant,