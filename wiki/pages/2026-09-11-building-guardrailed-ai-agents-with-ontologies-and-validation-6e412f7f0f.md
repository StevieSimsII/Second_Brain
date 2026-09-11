---
title: "Building Guardrailed AI Agents with Ontologies and Validation"
source: "https://www.youtube.com/watch?v=Sir59K8ZDPU"
date: "2026-09-11"
tags: [ai-agents, ontologies, knowledge-graphs, neuro-symbolic-ai, data-validation]
source_type: "youtube"
source_fingerprint: "6e412f7f0f"
source_characters: 16779
---

## Overview

AI agents combine probabilistic language-model decisions with tools and iterative control loops. This flexibility also creates risks: fabricated values, invalid actions, runaway loops, unintended side effects, and mounting token costs. The source proposes a neuro-symbolic design that places formal domain knowledge around an agent. Typed validation checks the shape of tool inputs and outputs, while an ontology checks whether their meaning and relationships are consistent with the domain. The practical goal is not to eliminate probabilistic behavior, but to constrain consequential actions before they change external state.

## Key Concepts

- **Agent perception–decision–action cycle**: An agent receives context, decides what should happen next, and requests an action. A language model itself only produces output; an application must interpret a tool request, execute the selected tool, return its result, and decide whether the loop should continue.
- **Ontologies and knowledge graphs**: An ontology formally describes a shared domain using entities, properties, relationships, and constraints. A graph representation makes relationships explicit and can be extended by adding nodes, properties, or edges. The source contrasts this flexibility with the more rigid table structure of relational databases, though real relational schemas can also evolve.
- **Top-down and bottom-up modeling**: A top-down ontology begins with domain experts identifying concepts such as customers, orders, representatives, and their relationships. A bottom-up ontology extracts recurring entities and relationships from operational evidence such as customer interactions. A practical ontology can combine both approaches and reuse established vocabularies such as Schema.org, FOAF, and Dublin Core where appropriate.
- **RDFS inference**: RDFS domain and range declarations can derive additional classifications. If the property “teaches” has domain Teacher and range Student, then the statement “Bob teaches Scooter” supports inferring that Bob is a Teacher and Scooter is a Student. If Teacher is a subclass of Person, Bob can also be inferred to be a Person.
- **OWL constraints and reasoning**: OWL can express semantics such as transitive, functional, disjoint, and restricted-value relationships. A transitive ancestor relationship can derive an indirect ancestor. A functional property allows at most one value and may cause two recorded values to be treated as identifiers for the same individual rather than automatically reporting an error. These rules depend on the ontology’s explicit assumptions and should not be mistaken for universal facts.
- **Agent loops and termination controls**: A tool-using loop commonly asks the model for the next step, examines its stop reason, executes a requested tool, validates the result, and either finishes, retries, or escalates to a human. Loops enable iterative work but can become infinite, drift away from the goal, or consume excessive tokens. Systems therefore need explicit iteration, cost, timeout, and escalation limits.
- **Syntactic versus semantic validation**: A schema-validation library such as Pydantic can check whether data has the required fields and acceptable types. An ontology-backed validator checks whether the data makes sense in the domain—for example, whether a status belongs to the permitted vocabulary, a recipient has the right role, or an order already has a refund. Passing type validation does not imply semantic correctness.
- **Side-effect isolation**: The source recommends keeping proposed agent actions free of external side effects until validation succeeds. Treat tool calls that modify databases, send payouts, or contact people as staged commands: construct the request, validate its structure, test it against ontology rules, and only then authorize execution or request human review.

## How It Works

A guarded agent can be organized as a staged loop. First, the model receives the user’s goal, relevant context, and descriptions of available tools. It may return either a final response or a structured tool request. Second, a typed model validates the requested arguments; malformed or missing data is rejected before execution. Third, a preferably read-only tool runs and returns structured evidence. Fourth, an ontology-aware reasoner evaluates the proposed conclusion or next action against domain rules—for example, permitted order statuses, disjoint organizational roles, cardinality constraints, and previously recorded transactions. If the result is valid, the controller may finish or authorize a separate state-changing operation. If it is invalid, the controller sends a precise error back to the model or escalates to a human. The controller must also enforce maximum iterations, token or monetary budgets, timeouts, and an auditable record of every proposal, validation decision, and execution. This separates probabilistic planning from deterministic enforcement: the model suggests; code and domain rules decide what is allowed to happen.

## Training Exercise

Design a guarded refund agent for a small online store. Define a graph with Customer, SupportRepresentative, Order, Payment, and Refund entities. Add relationships such as placedOrder, paidFor, requestsRefund, issuedFor, and refundRecipient. Specify a fixed order-status vocabulary: paid, shipped, or refunded. Add rules stating that Customer and SupportRepresentative are disjoint roles and that an order may have no more than one successful refund. Then define typed request and response models for a refund tool. Walk through four test cases: a valid first refund to the buyer; a second refund for the same order; a payout addressed to a support representative; and an order whose status is “probably shipped.” For each case, record whether structural validation or ontology validation catches the problem. Finally, sketch loop controls with a maximum of three model attempts, a tool timeout, a cost budget, and mandatory human review whenever validation continues to fail. Keep the exercise read-only or use a mock ledger so no real payment can occur.

## Further Reading

- [Source video on YouTube](https://www.youtube.com/watch?v=Sir59K8ZDPU)
- [Code Supreme](https://codesupreme.ai)
