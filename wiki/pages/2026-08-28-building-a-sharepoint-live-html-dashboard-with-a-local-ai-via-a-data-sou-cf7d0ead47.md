---
title: "Building a SharePoint Live HTML Dashboard with a Local AI via a Data Source Contract"
source: "https://lnkd.in/p/gFQgcTuM"
date: "2026-08-28"
tags: [sharepoint, html-dashboards, ai-workflows, data-contracts]
source_type: "web"
source_fingerprint: "cf7d0ead47"
source_characters: 2557
---

## Overview

This lesson describes a proof-of-concept pattern for generating a SharePoint HTML dashboard with a local AI model that has no direct SharePoint access. The core idea is to separate schema understanding from code generation: SharePoint-side tooling produces a structured description of a list or library, and a local model uses that description plus SharePoint HTML and LiveData rules to generate the dashboard. The evidence is limited to a short LinkedIn post, so treat this as an observed architecture and workflow, not a validated production blueprint.

## Key Concepts

- **LiveData in SharePoint**: The post says SharePoint's LiveData capability lets JavaScript-based HTML pages connect to lists and document libraries while staying inside the SharePoint sandbox.
- **Data Source Contract**: A SharePoint skill analyzes a list or library and creates a contract describing fields, data types, choices, relationships, views, and useful KPI or filter information. This contract is the main input to the local model.
- **No direct model access to SharePoint**: The local AI does not query SharePoint directly. Instead, it receives the Data Source Contract and a reusable system prompt containing the relevant SharePoint and sandbox rules.
- **Reusable system prompt**: The system prompt is described as containing the SharePoint `/_html` specification, LiveData structure, sandbox restrictions, and design guidelines. This gives the model the constraints needed to generate compatible code.
- **Local code generation**: The dashboard HTML and JavaScript are generated locally in LM Studio from the contract plus a short task prompt. The post specifically reports success with `Qwen3-Coder-30B-A3B-Instruct` on a Mac mini M4 with 32 GB RAM.
- **Runtime data binding in SharePoint**: After upload, SharePoint provides current list data when the generated page opens. In this pattern, SharePoint is responsible for live data delivery at runtime, not the local model.

## How It Works

A practical way to understand this pattern is as a four-stage pipeline. First, inspect the target SharePoint list or library and extract a schema-level description rather than exporting records. Second, package that description as a Data Source Contract containing structure, field semantics, and view or KPI hints. Third, give a local model two inputs: the contract and a reusable prompt that explains SharePoint `/_html`, LiveData, sandbox limits, and dashboard design rules. Fourth, upload the generated HTML file to SharePoint, where the page receives live data at runtime through LiveData. The architectural benefit is that business data does not need to be sent to the local model. The main uncertainty is operational breadth: the author says it is a small proof of concept and only hopes it works across all sites in the tenant.

## Training Exercise

Write a mini lesson plan for yourself using this pattern. Define a fictional SharePoint list with 5 fields, 1 relationship, and 2 useful filters. Then draft a compact Data Source Contract for it, including field names, types, allowed values, and one KPI. Next, write a short system prompt section that lists the constraints your HTML generator must follow: sandbox-safe JavaScript, no direct SharePoint access, and runtime binding through LiveData. Finally, outline the HTML dashboard you want the model to generate: one summary KPI card, one filter control, and one table. As a reflection step, note which parts are supported directly by the source and which parts you are inferring for your exercise.

## Further Reading

- [LinkedIn source post](https://lnkd.in/p/gFQgcTuM)
