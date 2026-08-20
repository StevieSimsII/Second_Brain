---
title: "Agent Host in VS Code: Persistent Agent Sessions Across Projects, Web, and Machines"
source: "https://lnkd.in/p/gj_cmNSu"
date: "2026-08-20"
tags: [developer-tools, vscode, agent-systems, session-management, remote-development]
source_type: "web"
source_fingerprint: "a3271cd006"
source_characters: 5915
---

## Overview

This lesson explains the core idea demonstrated in the source: VS Code's Agent Host separates an agent session from the editor window so the session can keep running across project switches, web access, and multiple machines. The practical takeaway is architectural: if agent execution lives in a dedicated host process instead of a single client window, the same live session can be resumed and controlled from different interfaces. Evidence is limited to a product demo transcript and linked resources, so implementation details beyond the demonstrated behavior are not established here.

## Key Concepts

- **Dedicated host process**: The transcript says agent sessions run in their own dedicated process, rather than being tied to a VS Code window, client, or machine session.
- **Session persistence across projects**: A session continues running even after the original folder is closed and another project is opened, which shows that project context and UI context are not the same as process lifetime.
- **Shared live session state**: The demo shows the same session appearing side by side in different clients, with live updates such as approved tool calls, chat input, and queue changes reflected across views.
- **Multiple clients for one session**: The same agent session can be accessed from the VS Code chat view, an Agents window, and the web at `vscode.dev/agents`, implying client attachment to a common backend session.
- **Remote session access**: The source shows enabling remote session access so a browser can connect to an agent-host machine and interact with sessions still running there.
- **Cross-machine agent hosts**: The demo includes reconnecting to a remote host on another machine and viewing or starting sessions against folders on that machine through Agent Host.

## How It Works

Based on the demo, Agent Host changes the execution model from 'session lives inside this editor window' to 'session lives in a host process that clients attach to.' A likely mental model is: 1) start a session from VS Code, 2) the host process owns execution and history, 3) any compatible client such as the chat view, Agents window, or web UI connects to that same running session, and 4) remote hosts expose sessions running on other machines. The source also mentions a 'copilot harness option' powered by the Copilot SDK and running on Agent Host, plus an Agent Host Protocol whose spec is live and under active development. The source does not provide protocol mechanics, storage design, or security details, so those remain unknown from this material alone.

## Training Exercise

Create a short architecture note with three columns: `client`, `host`, and `session state`. Using only the source, map what belongs in each column. Then write a test plan you would run if you had access to the feature: start a session, close the folder, open a different project, reconnect from another client, and verify which actions stay synchronized. Finish by listing two benefits of host-based sessions and two unanswered questions the demo leaves open, such as authentication, failure recovery, or protocol details.

## Further Reading

- [Source post](https://lnkd.in/p/gj_cmNSu)
- [Agent Host in VS Code](https://lnkd.in/g2iwf3j6)
- [Agent Host Protocol](https://lnkd.in/g9VjdPd5)
- [VS Code issue tracker](https://lnkd.in/e_vCWA7p)
