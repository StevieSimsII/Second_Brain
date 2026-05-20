# Google I/O 2026: Gemini 3.5, Agentic Search, XR, and Google's Expanding AI Platform

Date: 2026-05-20
Source: https://www.zdnet.com/article/google-io-05-19-2026-live-blog/
Tags: google, gemini, ai-agents, search, android-xr, developer-tools

## Overview

This lesson distills the major technical themes from Google's I/O 2026 keynote coverage: a new Gemini 3.5 model family, increasingly agentic product behavior across Search and Gemini, multimodal creation tools, developer-facing web agent tooling, and Android XR hardware expansion. Rather than treating the event as a list of announcements, the goal is to help an engineer understand the platform direction Google is signaling and how the pieces fit together.

If you build consumer apps, developer tools, enterprise workflows, or multimodal experiences, these announcements matter because Google is turning AI from a chat surface into an execution layer embedded across products. The conference suggests a stack composed of fast multimodal foundation models, personalization and context from Google's ecosystem, UI generated on demand, and agents that can act across apps, documents, shopping, and the web.

## Key Concepts

- **Gemini 3.5 Flash**: Gemini 3.5 Flash is presented as the first publicly available model in the Gemini 3.5 family, optimized for speed, lower cost, and lightweight deployment while still supporting longer-horizon agentic tasks. Google positions it as a practical model for product integration, coding workflows, Search, and API usage rather than only a flagship benchmark model.
- **Agentic AI**: Agentic AI refers to systems that do more than answer prompts: they plan, track goals, use tools, and carry out multi-step tasks on a user's behalf. In this coverage, agentic behavior shows up in Spark, Search agents, shopping workflows, and developer tools that help agents understand and manipulate web applications.
- **Generative UI**: Generative UI is the idea that the system does not just produce text; it dynamically constructs the interface best suited for the task. Google's examples include Search responses assembled as personalized interactive layouts and Gemini responses broken into structured, visual chunks instead of a single text block.
- **Multimodal world models**: Google's Omni model is described as a multimodal system that accepts combinations of text, image, audio, and video to generate or edit video outputs. The important concept is not only multiple input types, but the claim that a single model can reason across them and produce more coherent creative results.
- **Personal context integration**: Several product demos depend on access to user context such as calendars, files, notes, emails, preferences, and activity across Google services. This context layer is what enables personalized itineraries, document generation from scattered materials, and persistent shopping or task agents.
- **AI content provenance**: Google highlighted content provenance through both SynthID watermarking and C2PA content credentials. For engineers, this points to a future where generative pipelines increasingly need metadata, attribution, and standards-based authenticity signals instead of relying on brittle AI-detection claims.

## How It Works

Google's I/O 2026 messaging describes an AI stack with four layers: models, context, orchestration, and experience.

At the bottom is the **model layer**. Gemini 3.5 Flash is the new default workhorse for several surfaces, including the Gemini app, AI Mode in Search, Antigravity, and the Gemini API. The significance is architectural: Google appears to be standardizing many end-user and developer experiences on a fast model that is cheap enough to run broadly, but capable enough to support coding, multimodal understanding, and multi-step actions.

Above that is the **context layer**. Many announcements rely on Google's advantage of already hosting user state across products. Search can use preferences and calendar information to assemble a custom itinerary. Docs Live can pull from notes, email, and documents to draft content. Universal Cart can persist product intent across Search, YouTube, Gemini, and Gmail. The lesson for engineers is that the value of an AI assistant increasingly comes from connected data and permissions, not just raw model quality.

The third layer is **orchestration**, which is where Google is pushing hard on agents. Spark is positioned as an always-on personal agent that takes verbal instructions and proactively handles multi-step logistics. Search agents can research, and future ones will help book tickets or events. Developer-facing tooling such as WebMCP and Chrome DevTools for agents suggests Google expects agents to operate against websites and web apps as tools, not only against Google-owned products.

The top layer is the **experience layer**, where AI becomes visible to users. Instead of returning plain text, products generate structured interfaces. Search's updated multimodal box accepts richer inputs and returns interactive results. Gemini's redesign adds more visual response composition and smoother switching between voice and text. Flow and Pics use model outputs to support creative workflows rather than isolated one-shot generation.

Step by step, the product strategy looks like this:

1. **Deploy a fast default model everywhere**
   - Gemini 3.5 Flash becomes the baseline engine.
   - It powers consumer products and developer APIs.
   - This reduces fragmentation between product capabilities.

2. **Use Google account context as retrieval and memory**
   - Calendar, email, notes, files, and shopping behavior become task inputs.
   - Responses become personalized and actionable rather than generic.

3. **Wrap model calls in planner/executor flows**
   - Spark, Search agents, and shopping agents imply decomposition into subtasks.
   - The system must decide what information to gather, which tools to call, and how to present the result.

4. **Generate task-specific interfaces instead of generic chat**
   - Itineraries become visual plans.
   - Search becomes a multimodal workspace.
   - Gemini responses become segmented, graphic-rich outputs.

5. **Extend the same pattern into new domains**
   - Creative media: Omni, Flow, Pics.
   - Productivity: Docs Live.
   - Web development: Modern Web Guidance, DevTools for agents, WebMCP.
   - Hardware: Android XR glasses as a new interaction endpoint.

The **developer implications** are especially important. Google's web tooling announcements imply that future applications may need to be consumable by both humans and software agents. If agents are expected to navigate a site, diagnose failures, or use a page as a toolkit, then developers need clearer page semantics, stable action surfaces, and machine-readable affordances. This is similar in spirit to API design, but applied to interactive web UX.

The **creative stack** follows the same architecture. Omni is the multimodal generation/editing engine; Omni Flash is the lighter deployable variant; Flow is the filmmaking-oriented workspace with agent support; Pics is the image editing/generation front end. The system is moving from a model demo to a workflow platform where the model collaborates across multiple steps of the creative process.

The **XR story** is comparatively early but strategically consistent. Android XR glasses are another place where multimodal AI and persistent personal context make sense: voice prompting, visual capture, navigation, and ambient assistance. Google's likely platform play is to seed an ecosystem through hardware partners, then make Gemini the common intelligence layer across devices.

Finally, Google emphasized **trust and provenance** through SynthID and C2PA credentials. This matters because as generative output spreads into Search, video, images, and docs, downstream systems will need ways to preserve origin metadata. For engineers building media pipelines, this is a sign that provenance standards are becoming part of the product surface, not just a compliance add-on.

## Training Exercise

Build a small design proposal for an **agentic web application** inspired by the I/O 2026 announcements.

### Objective
Design a product that uses:
- a fast multimodal model,
- user context from multiple sources,
- an agent that performs a multi-step task,
- and a generated UI for results.

### Scenario
Assume you're building a `Trip Planner + Booking Assistant` for a company that already has access to:
- user calendar data,
- saved preferences,
- email confirmations,
- and a travel vendor API.

### Step 1: Define the workflow
Write down a user request such as:

```text
Plan a two-day trip to Seattle next month around my work calendar, keep hotel cost under $250/night, and suggest one dinner with vegan options.
```

Break the task into at least 6 steps, for example:
1. Read calendar availability.
2. Infer destination and constraints.
3. Query hotel and flight providers.
4. Rank options using preferences.
5. Build an itinerary UI.
6. Ask for confirmation before booking.

### Step 2: Specify the architecture
Create a one-page architecture with these components:
- **Model**: a Gemini-3.5-Flash-like fast model for orchestration and summarization.
- **Context service**: calendar, email, preference retrieval.
- **Tool layer**: hotel API, flight API, maps API, booking API.
- **Planner/agent**: decomposes the request and executes tools.
- **UI renderer**: turns the final result into cards, timelines, and action buttons.

### Step 3: Define tool interfaces
Write pseudocode for 3 tool calls:

```javascript
async function getCalendarAvailability(userId, startDate, endDate) {}
async function searchHotels(city, maxPrice, dates, preferences) {}
async function createItinerary(options, userContext) {}
```

Then describe what inputs and outputs each tool should expose so an agent can call them reliably.

### Step 4: Add agent safety checks
Document at least 4 guardrails, such as:
- do not book without explicit confirmation,
- separate inferred preferences from user-stated constraints,
- log which external tools were used,
- show provenance for generated recommendations.

### Step 5: Design a generative UI response
Sketch the output as sections:
- Trip summary
- Flight options
- Hotel cards
- Restaurant suggestion
- Calendar conflict warnings
- `Approve` / `Revise` actions

### Step 6: Reflect on product tradeoffs
Answer these questions in writing:
1. Why use a fast model instead of the largest model everywhere?
2. Which context sources create the most value?
3. What makes this a true agent instead of a chatbot?
4. Where should provenance or content credentials appear?

### Stretch goal
Adapt the same design for an XR interface. Explain what changes when the user interacts through smart glasses instead of a laptop or phone.

## Further Reading

- [Gemini API documentation](https://ai.google.dev/)
- [Google I/O](https://io.google/)
- [Chrome DevTools documentation](https://developer.chrome.com/docs/devtools/)
- [C2PA Specification](https://c2pa.org/specifications/specifications/1.3/index.html)
- [Android XR](https://developer.android.com/xr)
