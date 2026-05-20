# Copilot CLI, Agent UIs, and the Shift from Terminal-First to IDE-Assisted AI Development

Date: 2026-05-20
Source: https://www.linkedin.com/posts/jukkaniiranen_claude-code-inside-microsoft-was-never-going-share-7460787128470265856-7IaX?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY
Tags: copilot, cli, vscode, agents, developer-tools

## Overview

This lesson examines a short but revealing industry discussion about Microsoft discontinuing internal use of Claude Code as a developer harness and consolidating around Copilot CLI and related GitHub/Microsoft agent experiences. The source is not a deep technical specification, but it highlights an important product and workflow transition: AI coding tools are no longer just model choices, but full environments made of interfaces, safety constraints, repository awareness, and integration into real developer workflows.

Engineers, tool builders, and technical leads should care because the competitive edge in AI-assisted development is increasingly in the harness and UX rather than just the underlying model. The post and comments point to a broader trend: terminal-only experiences work well for some users, but agent-first graphical interfaces, sandboxed cloud execution, repo-aware editing, and diff review are becoming essential for wider adoption, especially among low-code makers and less IDE-native users.

## Key Concepts

- **Model versus harness**: The source distinguishes between the underlying model provider, such as Anthropic, and the developer tool wrapped around it. A strong coding assistant is not just an LLM endpoint; it is the surrounding harness that manages repository context, tool access, planning, code edits, review flows, and user interaction.
- **CLI as an agent interface**: Copilot CLI and Claude Code represent terminal-based interfaces for interacting with coding agents. In this mode, the terminal becomes the control plane for prompting, tool execution, and iterative development, which can be efficient for experienced developers but intimidating or opaque for others.
- **Agent-first GUI workflows**: The source highlights the arrival of VS Code's Agents UI and mentions desktop app experiences that resemble agent consoles more than traditional editors. This matters because visual task panes, plan visibility, diff inspection, and multi-step workflow management reduce the cognitive load compared with raw command-line sessions.
- **Repo visibility and trust**: A recurring point is that users want to see the actual repository, files, and edits before trusting an agent's output. IDE integration provides a stronger sense of grounding because generated changes can be reviewed in context rather than accepted as opaque terminal output.
- **Dogfooding and feedback loops**: Several comments frame Microsoft's move as a dogfooding strategy: if internal developers use Copilot CLI and related tools, Microsoft captures telemetry and feedback needed to improve its own harness. This is a common platform strategy when the product's quality depends on real-world usage across diverse software stacks.
- **Broadening the developer audience**: The discussion connects AI coding tools to low-code and Power Platform users who may now need more traditional development workflows. For this audience, the success of agentic tooling depends on reducing reliance on expert-level terminal or IDE knowledge while still exposing enough control to be useful.

## How It Works

The source is a LinkedIn post reacting to a report that Microsoft will stop giving its developers access to Claude Code and instead standardize on Copilot CLI and Microsoft/GitHub-owned tooling. Technically, the important idea is not simply vendor replacement. It is that the competitive layer is moving upward from the model to the workflow surface.

In practice, an AI coding system has several layers:

1. **Foundation model**: the LLM that generates plans, explanations, and code.
2. **Harness**: the orchestration layer that decides what files to read, how to call tools, how to edit code, and how to present actions.
3. **Interface**: CLI, IDE panel, desktop app, or cloud workspace.
4. **Execution environment**: local machine, sandboxed cloud runtime, or integrated dev container.

The post argues that Microsoft may still use Anthropic models, but it wants to own the harness and user experience. That makes sense because the harness is where product differentiation happens:

- repository scanning
- edit application
- diff generation
- command execution
- web search or documentation lookup
- approval and safety prompts
- telemetry collection
- integration with source control and CI/CD

A terminal-first tool like Copilot CLI or Claude Code typically works as follows:

- The user starts in a shell within a project directory.
- The tool infers repo context from the current working tree and version control metadata.
- The user submits a task in natural language.
- The harness may read files, inspect git status, run tests, and propose edits.
- The user reviews output, often as text plus patch-style changes.
- The tool may iterate by executing more commands or revising code.

This interaction model is powerful because it is close to the operating system and easy to script, but it has weaknesses. For users who are not fluent in terminal workflows, it can obscure what the agent is doing. Planning, specification review, file navigation, and side-by-side diff inspection are all possible, but usually less discoverable than in a GUI.

The post's core insight is that this changes once the same capabilities are embedded into an agent-oriented GUI such as VS Code's Agents view or a desktop app. In that design, the rough architecture looks more like this:

- **Conversation pane** for requests and agent reasoning summaries
- **File tree/editor** for grounded repo context
- **Diff viewer** for reviewing generated changes before applying them
- **Task or plan pane** for multi-step execution visibility
- **Integrated terminal** for commands that still need shell access
- **Source control integration** for staging, committing, and rollback

This matters because it combines two kinds of trust:

- **Behavioral trust**: the user can see what the agent plans to do.
- **Artifact trust**: the user can inspect the exact files and changes in context.

The comments expand the picture in a few useful ways. One commenter notes that GitHub Copilot experiences can run agents in the cloud, sandboxed by default. That implies an execution architecture where tool use may happen in an isolated environment instead of directly on the local workstation. For enterprise adoption, this can improve safety and make it easier to grant constrained credentials. Another commenter values native web search, showing that coding assistants are now expected to do retrieval and research as part of the workflow rather than just code generation.

For low-code and Power Platform developers, the source suggests a transition from visual-first app building toward more code- and agent-assisted workflows. The technical challenge is not whether these users can use LLMs; it is whether the tool surface supports them. A raw terminal assumes comfort with paths, shells, processes, and text-only state. An agent-first GUI can preserve the same underlying orchestration while exposing it through reviewable plans, clickable files, and visible execution traces.

From an engineering management perspective, the move also fits a classic platform control pattern. If Microsoft standardizes internal use on Copilot CLI and adjacent experiences, it can:

- collect product feedback from many engineering teams
- improve repos, prompts, and safety harnesses for its own stack
- reduce dependence on a competitor's end-user product surface
- unify documentation and support around one workflow
- accelerate features for specific ecosystems such as Power Platform and GitHub

So the central technical lesson from the article is this: the future of AI developer tooling is not just `best model wins`. It is `best integrated system wins`.

A practical mental model is:

```text
User request
  -> agent UI or CLI
  -> harness/orchestrator
  -> model + retrieval + tool calls
  -> local/cloud execution environment
  -> code changes, plans, test results, diffs
  -> human review and iteration
```

When evaluating tools like Copilot CLI, Claude Code, or agentic IDE features, engineers should compare each layer of that pipeline rather than focusing only on model quality.

## Training Exercise

Compare a terminal-first and IDE-assisted AI workflow in a small repository.

### Goal
Understand how interface choice changes trust, reviewability, and usability when working with an AI coding agent.

### Prerequisites
- Git installed
- VS Code installed
- Access to GitHub Copilot or another AI coding assistant with both chat/editor and terminal-style workflows
- A small sample repository

### Step 1: Create a sample repo
Use any small project, or create one quickly:

```bash
mkdir agent-ui-vs-cli-demo
cd agent-ui-vs-cli-demo
git init
printf "def add(a, b):\n    return a + b\n" > math_utils.py
printf "from math_utils import add\nprint(add(2, 3))\n" > app.py
git add .
git commit -m "Initial demo"
```

### Step 2: Define one realistic task
Use the same prompt in both interfaces:

- Add input validation to `add`
- Create a `subtract` function
- Add a simple test file
- Update `app.py` to demonstrate both functions

Example task text:

```text
Refactor this small Python repo. Add input validation so math functions only accept ints or floats, add a subtract function, create tests, and update the demo app. Show me the plan before applying changes.
```

### Step 3: Run the task in a terminal-oriented workflow
Use your CLI assistant or the integrated terminal with an AI coding tool.

Observe and write down:
- How the tool discovers files
- Whether it shows a plan before editing
- How diffs are presented
- Whether commands/tests are run automatically
- How easy it is to understand what changed

### Step 4: Run the same task in VS Code's agent/chat/editor workflow
Open the same repo in VS Code and use the agent or chat interface.

Observe:
- Whether the file tree and open editors help you understand the repo faster
- How proposed edits appear in the editor or diff view
- Whether reviewing changes feels safer or more transparent
- Whether it is easier to iterate on one file at a time

### Step 5: Compare outcomes
Create a short comparison table with these columns:

- Interface
- Planning visibility
- Repo awareness
- Diff review quality
- Ease of use
- Confidence before accepting changes

### Step 6: Reflect like a tool evaluator
Answer these questions:

1. Which workflow was faster for a simple task?
2. Which workflow made it easier to trust the output?
3. If you were onboarding a low-code maker or non-terminal-heavy engineer, which interface would you choose?
4. What capabilities came from the model, and what clearly came from the harness/UI?

### Optional extension
If your tool supports cloud or sandboxed agent execution, repeat the exercise there. Compare:

- local versus sandboxed command execution
- credential management
- safety boundaries
- reproducibility

The point of the exercise is not to prove that GUI beats CLI or vice versa. It is to separate model quality from harness quality and to evaluate the developer experience as a full system.

## Further Reading

- [Visual Studio Code Release Notes](https://code.visualstudio.com/updates/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GitHub CLI](https://cli.github.com/)
- [The Verge - Microsoft is discontinuing Claude Code internally](https://www.theverge.com/)
- [Anthropic Documentation](https://docs.anthropic.com/)
