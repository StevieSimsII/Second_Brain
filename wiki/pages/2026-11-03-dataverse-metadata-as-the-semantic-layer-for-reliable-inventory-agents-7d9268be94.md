---
title: "Dataverse Metadata as the Semantic Layer for Reliable Inventory Agents"
source: "https://www.youtube.com/watch?v=GB2lQcK4Uvs"
date: "2026-11-03"
tags: [copilot-studio, dataverse, mcp, ai-agents, data-governance]
source_type: "youtube"
source_fingerprint: "7d9268be94"
source_characters: 20215
channel: "Shane Young"
published: "2026-08-31"
duration_seconds: 971
topics: [ai-agents, power-platform, prompt-engineering, automation-workflows]
kind: "tutorial"
depth: 2
actionability: 3
---

## TL;DR

> Clear Dataverse table and column descriptions let an MCP-powered agent discover and use business data with far less prompt engineering. A one-line instruction can prove the concept, but production agents still need explicit scope, operating rules, and human-reviewed safeguards.

## Key Takeaways

1. Dataverse table descriptions help agents distinguish the intended data even when an environment contains several similarly named tables.
2. Column descriptions explain business meaning—such as what a vendor validity date represents—so agents can select and present fields more accurately.
3. Write semantic context into the data model once instead of making the agent rediscover the schema during every interaction.
4. Document user-facing custom columns first; the presenter limited automated description work to fields the agent would actually use.
5. Dataverse MCP can write as well as read: the demonstration updates a vendor, creates an item, and resolves its vendor lookup relationship.
6. Production instructions should constrain the agent to approved tables and define rules for creation, deletion, statuses, relationships, validation, and recalculation.
7. Keep a human accountable for reviewing generated metadata and instructions; the presenter caught a missing rule requiring order items to be deleted with their parent order.

## Key Moments

- [0:30](https://www.youtube.com/watch?v=GB2lQcK4Uvs&t=30s) — Builds a working demo agent from one instruction and the Dataverse MCP tool
- [1:58](https://www.youtube.com/watch?v=GB2lQcK4Uvs&t=118s) — Shows how table descriptions identify the correct vendor table in a messy environment
- [3:04](https://www.youtube.com/watch?v=GB2lQcK4Uvs&t=184s) — Demonstrates how column descriptions clarify field meaning and improve responses
- [5:05](https://www.youtube.com/watch?v=GB2lQcK4Uvs&t=305s) — Uses GitHub Copilot and an MCP integration to generate metadata descriptions
- [8:41](https://www.youtube.com/watch?v=GB2lQcK4Uvs&t=521s) — Updates records and creates an item with a resolved vendor lookup
- [11:03](https://www.youtube.com/watch?v=GB2lQcK4Uvs&t=663s) — Expands the demo into scoped, prescriptive instructions suitable for testing
- [13:59](https://www.youtube.com/watch?v=GB2lQcK4Uvs&t=839s) — Finds and corrects a missing cascading-delete requirement through human review

## Overview

The lesson treats Dataverse metadata as a semantic interface for AI agents. Table descriptions explain each dataset’s purpose, while column descriptions capture field-level business meaning; the Dataverse MCP server can use that context to locate, read, and modify relevant records.

This matters to Copilot Studio builders, Power Platform administrators, and data owners working in environments with ambiguous names or overlapping schemas. Good metadata can accelerate prototyping, but dependable production behavior also requires narrowly scoped instructions and human review.

## Key Concepts

- **Dataverse MCP server**: The MCP server exposes Dataverse capabilities to the Copilot Studio agent. In the demonstration, the agent uses it to discover schemas, query vendors, update a date, create an item, and populate a lookup relationship.
- **Semantic metadata**: Table and column descriptions explain what data means rather than merely how it is named. This helps the agent distinguish similarly named tables and interpret ambiguous fields in business terms.
- **Metadata-driven self-discovery**: The agent can inspect available schema and descriptions instead of requiring every table, field, and relationship to be explained in the initial prompt. The presenter demonstrates this in an environment containing eight vendor-related tables, including three named Vendor.
- **One-time schema enrichment**: The presenter recommends generating and saving descriptions once rather than paying the reasoning cost of rediscovering meaning on every agent run. Stored descriptions can also be reviewed, corrected, and enriched with user terminology or abbreviations.
- **Read and write operations**: The Dataverse MCP integration is not limited to answering questions. It can update and create records, so accurate metadata and explicit operational rules become especially important.
- **Prescriptive production instructions**: A production-oriented prompt should list approved tables and define expected behavior for common operations. The presenter’s principle is to minimize unnecessary model decision-making by making rules explicit.
- **Human-in-the-loop review**: AI can draft descriptions and instructions after examining the schema, but it cannot own the business consequences. A human must clarify ambiguous fields, verify generated guidance, and identify missing rules.

## How It Works

1. Add meaningful descriptions to each relevant Dataverse table, including its business purpose, project context, and relationships.
2. Describe user-facing custom columns, especially ambiguous dates, choices, identifiers, and lookup fields.
3. Create a Copilot Studio agent and add the Microsoft Dataverse MCP server as a tool.
4. Give the prototype a concise goal and enough project terminology to anchor discovery.
5. Test representative reads and writes, including queries, updates, record creation, choices, and lookups.
6. For production, restrict the agent to named tables and specify rules for creation, deletion, relationship validation, statuses, calculations, and reporting.
7. Review every generated description and instruction with a domain owner, then test unusual user requests before release.

## Training Exercise

1. Choose two related Dataverse tables, such as Vendors and Items, and identify any similarly named tables that could confuse an agent.
2. Write a two-sentence purpose description for each selected table.
3. Add descriptions to five user-facing columns, including at least one date, choice, or lookup field.
4. Connect the Dataverse MCP server to a test Copilot Studio agent and provide one concise instruction describing its role.
5. Ask the agent to list records, explain an ambiguous field, and identify the relationship between the tables.
6. In a safe test environment, create or update one record and verify every written value and relationship directly in Dataverse.
7. Replace the prototype instruction with a production draft that names allowed tables and defines write, deletion, validation, and error-handling rules.
8. Have a domain owner review the draft and record at least one ambiguity or missing safeguard discovered during review.

## Test Yourself

<details><summary>Why are table and column descriptions more valuable than placing every schema explanation in the agent prompt?</summary>

Descriptions keep semantic context beside the data and make it reusable across agent runs. This reduces repeated discovery work while allowing administrators to inspect and refine the meaning centrally.

</details>

<details><summary>Why is the one-sentence agent useful for a demonstration but risky in production?</summary>

It leaves table selection and operational behavior largely to the model. Production instructions should identify allowed tables and explicitly define rules for writes, deletions, relationships, statuses, and validation.

</details>

<details><summary>What role should a human play when AI generates metadata or agent instructions?</summary>

A human should resolve ambiguous business meanings and review generated instructions for missing or unsafe behavior. In the example, human review added the requirement to delete associated order items when deleting an order.

</details>

## Further Reading

- [Power Apps 911 skills training](https://www.powerapps911.com/up-your-power-apps-skills)
- [Shane Young resources](https://www.powerapps911.com/shane)
