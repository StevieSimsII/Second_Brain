---
title: "Prompt Caching in Copilot-Style LLM Workflows"
source: "https://www.youtube.com/watch?v=TYOhNRp5n7Y"
date: "2026-07-21"
tags: [prompt-caching, llms, github-copilot, tokenization, developer-tools]
source_type: "youtube"
source_fingerprint: "f3dc58c179"
source_characters: 13215
---

## Overview

This lesson explains prompt caching as described in the source: when a chat request shares the same earlier context, the model provider can reuse previously computed work for that unchanged prefix, making later prompts much cheaper than recomputing everything. The speaker focuses on GitHub Copilot using OpenAI models, shows that identical follow-up prompts can reuse many tokens, and highlights practical causes of cache misses such as changing models, reasoning level, skills, MCP servers, or custom agents. Some details are explicitly presented as simplifications, and a few provider-specific claims are anecdotal rather than formally sourced in the transcript.

## Key Concepts

- **Prompt prefix**: The prefix is the unchanged earlier part of a request, including system instructions, tools, MCP definitions, skills, custom agents, and conversation history. Caching works when this earlier portion stays the same.
- **Why caching saves money**: The source says the expensive step is computing attention after tokenization and vectorization. Reusing cached work avoids redoing that full computation for unchanged context, so later requests are much cheaper, though not free.
- **Cache hit, miss, and expiry**: A cache hit reuses prior computation. A miss happens when the relevant prefix changes or the cached entry is no longer available. The speaker stresses that a miss is not always a total loss because caching is chunked, so earlier unchanged chunks may still help.
- **Provider-owned caches**: The cache belongs to the model provider, not the client harness. In the source, switching providers or even switching models is described as causing a miss because caches are not shared across those boundaries.
- **Workflow changes that alter the prefix**: Enabling or disabling skills, MCP servers, custom agents, or similar prompt-building features changes the prefix and can trigger a miss. Returning to a previous configuration may recover the old cache if it is still within the time-to-live window.
- **Session lifecycle matters**: The speaker claims that adding or editing an `agents.md`-style instruction file does not affect the current Copilot session until you start a new session with commands like clear or new. In the demo, the changed instructions were ignored until the session restarted.
- **Time-to-live is operational, not permanent**: For OpenAI models in this workflow, the speaker says the cache lasts about 30 minutes. For Anthropic on the API, the speaker says it is 5 minutes by default and may be configurable to 1 hour depending on the harness; this is presented as workflow guidance, not a formal spec citation.

## How It Works

Treat prompt caching as a prefix-reuse mechanism. Every chat turn is appended onto a growing request, and the expensive model-side work is associated with that accumulated context. If your next request keeps the earlier context identical, the provider can reuse prior computation and only process the new suffix. In practice, that means stable sessions are cheaper than constantly changing configuration. To preserve cache hits, avoid unnecessary model switches, keep reasoning settings stable when possible, and avoid toggling skills, MCP servers, or custom agents mid-session unless you need them. If you do change those settings, remember that returning to a prior configuration may still benefit from cache reuse if the cached variant has not expired. Also distinguish a cache miss from total waste: the source says caching is chunked, so some earlier unchanged segments may still be reusable even when later segments are invalidated. Finally, be cautious with local instruction-file edits in this workflow, because the source demonstrates that they may not take effect until a new session starts.

## Training Exercise

Open a chat workflow similar to the one described in the source and run four trials while recording whether token reuse appears. First, send the same short prompt twice without changing anything and note the second call's reuse. Second, change only the model or reasoning level and observe whether reuse drops, indicating a miss. Third, enable or disable one skill or MCP server, send the same prompt again, and compare behavior. Fourth, return to the original configuration within a short time window and test whether reuse comes back. Afterward, write a short note answering: which changes preserved the prefix, which changed it, and which results are solid observations versus assumptions based on the tool's UI.

## Further Reading

- [Source video](https://www.youtube.com/watch?v=TYOhNRp5n7Y)
