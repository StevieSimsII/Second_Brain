---
title: "Building a SharePoint Asset Dashboard with Copilot and Two Lists"
source: "https://lnkd.in/p/gwki7iwD"
date: "2026-08-26"
tags: [sharepoint, copilot, dashboard, knowledge-management, low-code]
source_type: "web"
source_fingerprint: "3ec5d1ae9d"
source_characters: 5854
---

## Overview

This lesson shows a practical pattern for turning fragmented SharePoint list data into a single HTML-based view with Microsoft Copilot. In the source, one list stores asset inventory and another stores asset allocations or ownership history. The core idea is not that Copilot magically understands an entire system, but that it can generate an initial interface from a plain-language prompt and then refine it through repeated conversation. The evidence is strong for the workflow and UI features described in the transcript, but thin on implementation details such as hosting, data bindings, schema resilience, and long-term maintenance.

## Key Concepts

- **Split-source inventory data**: The source describes a common setup where inventory data lives in one SharePoint list and allocation data lives in another, making simple questions hard to answer without manually combining records.
- **Single-view dashboard**: The generated HTML dashboard is valuable because it presents asset status, images, allocation, and ownership details in one place instead of forcing users to switch between lists.
- **Prompt-driven UI generation**: Copilot is used to create the first version of the application from a natural-language prompt specifying controls, layout, and displayed fields.
- **Conversational refinement**: A major lesson from the source is that refinement happens iteratively: the author asks for changes such as smaller images, an ownership-history table, conditional formatting, and layout adjustments, and Copilot updates the page.
- **Cross-list enrichment**: The dashboard becomes more useful when data from the ownership or allocation list is filtered to match the selected asset, adding context that was not visible in the inventory list alone.
- **Visible business rules**: The example adds conditional formatting for overdue maintenance dates, showing how lightweight apps can surface operational rules directly in the interface.
- **Governance and ownership risk**: A comment on the post highlights an important limitation: quickly generated tools can become important before anyone defines who owns them, where they run, or how they fail when list schemas change.

## How It Works

Observed workflow from the source: start with two SharePoint lists, one for asset inventory and one for asset allocations or ownership. Ask Copilot to create an HTML file with two filters, one for status and one for asset, plus an enlarged asset image and detail fields from the list. Review the generated page, then iteratively refine it by describing changes in plain language. In the transcript, those changes include reducing the image size, adding a history-of-ownership table under the image using data from the second list, applying red/green conditional formatting to maintenance dates, swapping panel positions, increasing text size, and tightening spacing. The lesson is that Copilot can accelerate the first usable version of an internal app, but the source does not provide code, deployment details, or safeguards for schema changes, so those aspects should be treated as unresolved.

## Training Exercise

Create a small practice scenario with two mock SharePoint lists: `Asset Inventory` and `Asset Ownership`. Write a prompt for an HTML dashboard that includes a status filter, an asset selector, an image area, and a details panel. Then write three follow-up prompts to refine the page: add an ownership-history table filtered to the selected asset, highlight overdue maintenance dates, and improve layout readability. After the UI exercise, document two operational decisions before sharing the tool: who maintains it and how users will know when list-schema changes break it.

## Further Reading

- [LinkedIn post: How many SharePoint lists does it take to answer a simple question?](https://lnkd.in/p/gwki7iwD)
