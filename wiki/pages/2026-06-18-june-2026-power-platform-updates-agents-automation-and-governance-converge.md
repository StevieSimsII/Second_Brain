# June 2026 Power Platform Updates: Agents, Automation, and Governance Converge

Date: 2026-06-18
Source: https://www.linkedin.com/posts/tiffany-treacy_powerplatform-powerapps-powerautomate-share-7473373166552240128-ZxE5/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via
Tags: powerplatform, powerapps, powerautomate, governance, aiagents, dataverse

## Overview

This update highlights a clear shift in Microsoft Power Platform: AI agents, low-code automation, and governance are no longer separate concerns. New features across Power Apps, Power Automate Desktop, and platform governance show how organizations can build agents that improve from user feedback, orchestrate richer app-driven automation, and control connector usage with more precision.

Working engineers, platform admins, and solution architects should care because these features reduce custom integration work while increasing operational control. The common theme is production-grade low-code systems: agents that learn in-place, desktop flows that interact more directly with apps, and governance tooling that reflects actual usage instead of static assumptions.

## Key Concepts

- **Closed-loop learning**: Closed-loop learning means an AI agent captures user corrections during normal operation and uses them to improve future behavior. In this update, the Power Apps MCP server turns corrections into structured memory, allowing knowledge to accumulate without building separate ML pipelines.
- **Structured memory for agents**: Structured memory is a persistent representation of user feedback, corrections, or learned patterns that an agent can reuse later. The important idea is that learning is operationalized directly in the platform, so improvements can emerge from repeated enterprise use rather than manual retraining cycles.
- **Attended automation with app-flow handoff**: Power Automate Desktop can now launch a Power App, pass inputs into it, receive outputs back, and react to app events. This creates a tighter loop between user-facing app experiences and desktop automation, reducing fragile UI workarounds.
- **Version comparison for desktop flows**: Version comparison makes change review practical by showing differences between two desktop flow versions, including subflows, actions, variables, and UI elements. Retaining versions in Dataverse for up to 12 months also supports troubleshooting, auditability, and change management.
- **Advanced connector policies**: Connector governance is evolving from simple allow/deny lists toward finer-grained control over actions and MCP server access. This matters in AI-heavy environments where an agent's effective capability is defined not just by the connector it can reach, but by which operations it is permitted to invoke.
- **Usage-based governance inventory**: Inventory visibility shows which connectors apps, flows, and agents actually use in practice. That helps administrators ground governance decisions in real dependency data before tightening policies, reducing the risk of breaking business-critical solutions.

## How It Works

The source describes several related platform capabilities rather than a single implementation, but they fit into a coherent architecture for enterprise low-code systems.

At the center is a feedback-driven AI model for business applications. The Power Apps MCP server acts as the execution and tool-access layer for agents. When a user corrects an agent, that correction is not treated as a one-off exception; instead, it is converted into structured memory. On future runs, the agent can consult that memory and adjust behavior. Over time, repeated corrections can consolidate into organization-level patterns, which is significant because it moves agent improvement from a lab exercise into daily production use.

A simplified flow looks like this:

1. A user interacts with an agent exposed through Power Platform.
2. The agent makes a decision or takes an action through MCP-backed tools.
3. The user corrects or refines the result.
4. The platform records that correction as structured memory.
5. On the next similar execution, the agent applies the learned pattern.

This creates a production feedback loop:

```text
User request -> Agent action -> User correction -> Structured memory -> Improved next run
```

The second major capability is richer coordination between Power Apps and Power Automate Desktop. Historically, attended desktop automation often depended on brittle UI navigation or indirect triggers. The new "Run Power App action" preview changes that by allowing desktop flows to launch an app directly, send input parameters, capture returned values, and trigger subflows from app events. Architecturally, this means:

- Power Apps can serve as the user interaction layer.
- Desktop flows can handle local-system or legacy-app automation.
- Inputs and outputs can move explicitly between them.
- Event-driven subflows reduce manual glue code.

That is especially useful in hybrid scenarios, such as a user selecting a record in a Power App and then invoking a desktop flow to interact with an on-premises application, generate a document, or update a system that has no modern API.

Another operational improvement is version comparison for desktop flows. Change management in low-code tools often becomes difficult when teams cannot easily inspect what changed between versions. Side-by-side comparison across subflows, actions, variables, and UI elements provides the equivalent of a visual diff for automation assets. Storing versions in Dataverse for up to 12 months also supports rollback analysis, release validation, and audit needs.

Governance is the final pillar. Advanced connector policies being generally available signals that policy enforcement is moving closer to the real execution surface of AI-enabled tools. In a conventional setup, admins might only classify connectors as business or non-business. In an AI-first environment, that is too coarse. A connector may be allowed, but only for certain actions; similarly, an MCP server may expose capabilities that need selective restriction. ACP addresses that more granular control model.

The inventory feature complements ACP by providing actual dependency visibility. Instead of guessing which connectors are safe to restrict, admins can inspect which apps, flows, and agents currently depend on them. In practice, the workflow becomes:

- Inspect inventory to understand connector usage.
- Identify high-risk or low-value connector actions.
- Apply advanced connector policies.
- Monitor impact and refine policy boundaries.

The broader lesson is that Power Platform is converging around three loops:

- **Build loop**: create apps, agents, and automations quickly.
- **Operate loop**: let systems improve through feedback and versioned change control.
- **Govern loop**: enforce connector and tool policies based on observed usage.

For engineers, this convergence reduces the amount of custom integration code needed to deliver adaptive enterprise workflows while increasing the importance of platform architecture, policy design, and lifecycle management.

## Training Exercise

Build a simple architecture plan for an enterprise workflow that uses all three themes from the update: learning agents, app-to-desktop automation, and governance.

### Goal
Design a low-code solution for a support team that:
- Uses an agent to answer or classify requests.
- Lets a human correct the result.
- Launches a desktop automation from a Power App when needed.
- Applies connector governance based on real dependencies.

### Steps
1. **Pick a business scenario**
   Choose one concrete use case, such as:
   - Employee onboarding
   - Invoice processing
   - Help desk ticket triage
   - Customer data correction

2. **Map the components**
   Write down four components:
   - A Power App for user interaction
   - An AI agent using Power Platform tools/MCP access
   - A Power Automate Desktop flow for a legacy or local-system action
   - A governance layer controlling connector and action access

3. **Draw the data flow**
   Sketch the request path in plain text or a diagram:

   ```text
   User opens Power App
     -> submits request
     -> AI agent evaluates and proposes action
     -> user confirms or corrects result
     -> correction stored as reusable memory
     -> desktop flow launched for legacy-system step
     -> output returned to app
   ```

4. **Define one correction loop**
   Describe one example where the user corrects the agent. For example:
   - The agent assigns the wrong category to a support ticket.
   - The user changes it from "hardware" to "identity access."
   - On future similar tickets, the agent should prefer the corrected category.

5. **Define app/desktop inputs and outputs**
   Create a small contract for the handoff:

   ```json
   {
     "input": {
       "ticketId": "HD-1042",
       "action": "reset-password",
       "userPrincipalName": "alex@example.com"
     },
     "output": {
       "status": "completed",
       "executionId": "run-8891",
       "notes": "Password reset in legacy admin tool"
     }
   }
   ```

6. **Plan a versioning review**
   Pretend your desktop flow changed. List what you would compare between two versions:
   - Changed subflows
   - Updated variables
   - Modified UI selectors/elements
   - Added or removed actions

7. **Create a governance checklist**
   Make a short table with these columns:
   - Connector or MCP server
   - Why it is needed
   - Which actions should be allowed
   - Which actions should be blocked
   - Which apps/flows/agents depend on it

8. **Review failure modes**
   Identify at least three risks, such as:
   - Agent learns a bad correction pattern
   - Desktop flow breaks because a UI element changed
   - Connector policy blocks a business-critical action

### Deliverable
Produce a one-page solution brief containing:
- The scenario
- The component diagram or text flow
- One structured-memory correction example
- The app/desktop input-output contract
- A governance checklist
- A short note on how version comparison would support maintenance

### Stretch task
If you already work in Power Platform, take an existing flow or app in your environment and perform a mini audit:
- List every external connector it uses.
- Identify one connector that would benefit from stricter action-level governance.
- Identify one user-correction point that could become part of a feedback loop for an agent.

## Further Reading

- [Microsoft Power Platform documentation](https://learn.microsoft.com/power-platform/)
- [Power Automate Desktop documentation](https://learn.microsoft.com/power-automate/desktop-flows/)
- [Microsoft Dataverse documentation](https://learn.microsoft.com/power-apps/maker/data-platform/data-platform-intro)
- [Power Apps documentation](https://learn.microsoft.com/power-apps/)
- [Power Platform Well-Architected](https://learn.microsoft.com/power-platform/well-architected/)
