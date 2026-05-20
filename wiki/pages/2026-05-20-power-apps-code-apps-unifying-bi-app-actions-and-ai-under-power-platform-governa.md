# Power Apps Code Apps: Unifying BI, App Actions, and AI Under Power Platform Governance

Date: 2026-05-20
Source: https://www.linkedin.com/posts/nicolassprotti_microsoft-powerbi-fabric-share-7462519822556520448-oBNV?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY&utm_campaign=share_via
Tags: powerapps, powerbi, fabric, powerplatform, enterprise-security, ai-agents

## Overview

This lesson explains the shift described in the source: from a traditional split where Power BI is used to analyze and Power Apps is used to take action, toward a single experience built as a Power Apps code app. The central claim is that dashboards are not becoming less relevant in the AI era; they are becoming the operational control surface for humans supervising automated systems, workflows, and AI agents.

For engineers and technical leads working in Microsoft-heavy enterprises, this matters because Power Apps code apps promise a hybrid model: pro-code development with familiar tools like React, TypeScript, Git, and CI/CD, while still running inside the Power Platform governance boundary. That means teams can build richer, more integrated applications without giving up enterprise controls such as identity, DLP, Conditional Access, sharing rules, and ALM.

## Key Concepts

- **From dashboard to control surface**: The source argues that AI does not replace dashboards; it increases their importance. When systems and agents can act autonomously, teams need visual operational context such as KPIs, trends, and variance charts to understand what is happening and whether automation is behaving correctly.
- **Power BI to see, Power Apps to act**: Historically, many organizations used Power BI for reporting and Power Apps for task execution or workflow interaction. This separation worked, but it also created a handoff between insight and action that could fragment the user experience.
- **Code apps in Power Apps**: Power Apps code apps are positioned as a pro-developer way to build applications using standard engineering tools rather than only low-code designers. The source highlights React, TypeScript, VS Code, Git, and CI/CD as the primary development experience.
- **Governed pro-code development**: A key value proposition is that code apps run inside the managed Power Platform environment instead of as an entirely independent SPA hosted elsewhere. That preserves enterprise controls such as Entra ID authentication, DLP policies, Conditional Access, application lifecycle management, and platform-based sharing.
- **Embedded AI agents**: The source emphasizes that agents are embedded natively into the application surface, grounded in the same data the user is reviewing. Instead of adding a generic chatbot, the application can support domain-specific actions like explaining a KPI variance, drafting communication, or triggering workflows.
- **Single-surface workflow**: The practical pattern is to combine report, app, and agent in one place. Users can inspect a metric, understand why it changed, and immediately take corrective action without leaving the current screen or switching tools.

## How It Works

The source presents a conceptual architecture rather than implementation details, but the mechanics are clear enough to derive a practical mental model.

At the highest level, the application surface combines three layers:

1. **Analytical context** from Power BI/Fabric-style reporting
2. **Operational interaction** through a Power Apps code app UI
3. **Assistance and automation** through embedded AI agents and workflow triggers

In the older model, these layers often lived in separate products or browser tabs. A user would inspect a dashboard, identify an issue, and then switch to a form or app to do something about it. The source argues that code apps collapse those steps into a single governed experience.

A typical data and interaction flow looks like this:

- Business data lands in the organization's governed data layer, often associated with Microsoft Fabric, Dataverse, or other enterprise sources.
- The app presents analytical artifacts such as KPIs, variances, and charts, giving the user a shared operational picture.
- The user interacts with the same screen to take action, for example reassigning ownership, flagging a supplier, or initiating a workflow.
- An embedded AI agent can use the current context to answer targeted questions or automate follow-up steps.
- All of this happens under the same identity, policy, and environment controls enforced by Power Platform and Microsoft identity/security tooling.

The important architectural point is not just UI consolidation. It is **governance consolidation**. In many organizations, a standalone React SPA can certainly be built and hosted cheaply, but engineering teams then need to assemble and maintain their own identity integration, authorization model, data access boundaries, deployment controls, compliance posture, and lifecycle processes. The source positions Power Apps code apps as a way to keep a modern front-end stack while inheriting platform-level controls.

A practical way to think about the code app structure is:

- **Frontend layer**: React + TypeScript application code authored in VS Code
- **Platform runtime**: the Power Apps code app host inside Power Platform
- **Security boundary**: Entra ID, Conditional Access, DLP, and environment policies
- **Data and business services**: Power Platform connectors, Dataverse, Fabric/Power BI-related data sources, or enterprise APIs
- **Automation layer**: embedded agents and workflow orchestration
- **Delivery pipeline**: Git-based source control and CI/CD, tied to Power Platform ALM practices

The source's supply-chain planning example shows why this architecture is attractive. A planner compares forecast versus actuals. The KPI summarizes impact. A waterfall chart explains variance drivers. That is classical BI. But then, because the experience is a code app rather than only a report, the same planner can take immediate actions like:

- reassigning coverage,
- flagging a supplier issue,
- asking an agent about next-quarter exposure,
- triggering an operational process.

That turns a passive report into an active decision surface.

From an engineering perspective, the tradeoff is straightforward:

- **Standalone app approach**: maximum hosting/runtime freedom, but more responsibility for security, governance, and integration consistency.
- **Code app approach**: some platform constraints, but faster alignment with enterprise requirements and lower friction for regulated production use.

The source strongly favors the second model for enterprises that care about production AI, auditable data access, and controlled rollout. Its thesis is that the real advantage is not merely development speed; it is being able to ship modern app experiences quickly **with guardrails already in place**.

## Training Exercise

Build a design proposal for a unified "report + action + agent" application in your own organization.

### Goal
Take an existing Power BI reporting use case and redesign it as a Power Apps code app concept that keeps analytics, user actions, and AI assistance in one governed experience.

### Step 1: Pick a current dashboard
Choose a real or hypothetical dashboard such as:

- sales pipeline review
- supply chain forecast vs actuals
- ticket backlog and SLA compliance
- finance budget vs spend

Write down:

- the primary KPI users look at,
- the supporting charts they use to diagnose issues,
- the actions they take after seeing a problem.

### Step 2: Map the old workflow
Document the current split between tools.

Use this template:

```text
Observe: User checks KPI in Power BI
Diagnose: User opens chart/filter/drillthrough
Act: User switches to another app / sends email / opens ticket / updates record
Follow-up: User asks someone else for context or manually triggers a workflow
```

### Step 3: Redesign as a code app
Create a one-page architecture note with these sections:

- **UI surface**: What appears on the main screen?
- **Data sources**: Where do KPI and detail data come from?
- **Actions**: What can users do without leaving the screen?
- **Agent prompts**: What context-aware questions should an embedded agent answer?
- **Governance**: Which controls matter most: identity, DLP, sharing, audit, ALM?

### Step 4: Define the component layout
Sketch a simple React-style component tree for the app.

Example:

```text
<App>
  <Header />
  <KpiSummary />
  <VarianceWaterfall />
  <ActionPanel />
  <AgentPanel />
  <AuditTrail />
</App>
```

For each component, note:

- displayed data,
- user interactions,
- required permissions.

### Step 5: Write 3 embedded-agent use cases
Examples:

- "Explain the top 3 drivers of this month's variance."
- "Draft a supplier escalation email using the selected account context."
- "If this trend continues, what is our projected exposure next quarter?"

For each one, specify:

- required input data,
- expected output,
- whether the result is advisory or triggers an action.

### Step 6: Evaluate fit
End by answering these engineering questions:

1. Why would this be better as a governed code app rather than a standalone SPA?
2. What platform constraints would your team need to accept?
3. What security and compliance benefits justify those constraints?
4. What would your CI/CD and ALM process need to look like?

### Optional stretch task
If you have access to Microsoft Learn content and a Power Platform environment, review the Power Apps code apps documentation and compare your proposed design against the documented development model. Update your architecture note with anything you missed around tooling, deployment, or environment strategy.

## Further Reading

- [Power Apps code apps overview](https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview)
- [Microsoft Power Platform architecture](https://learn.microsoft.com/en-us/power-platform/architecture/)
- [Power Platform Well-Architected](https://learn.microsoft.com/en-us/power-platform/well-architected/)
- [Microsoft Fabric documentation](https://learn.microsoft.com/en-us/fabric/)
- [Power BI documentation](https://learn.microsoft.com/en-us/power-bi/)
