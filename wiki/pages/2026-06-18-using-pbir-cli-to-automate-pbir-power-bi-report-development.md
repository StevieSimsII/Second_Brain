# Using pbir-cli to Automate PBIR Power BI Report Development

Date: 2026-06-18
Source: https://www.linkedin.com/posts/kurtbuhler_microsoftfabric-powerbi-reports-share-7473456154094809088-VKHN/?utm_source=share&utm_medium=member_ios&rcm=ACoAADqTv_wBXXGPo353jX-XXfFlsn3ZQBpJzsY
Tags: powerbi, pbir, microsoftfabric, cli, reporting, tmdl

## Overview

This matters to engineers building Power BI and Microsoft Fabric solutions as code rather than exclusively through the GUI. PBIR and related tooling make reports diffable, scriptable, and suitable for CI/CD workflows. If you maintain many reports, need repeatable refactoring, or want to inspect report internals such as visual queries and page metadata, pbir-cli provides a path toward treating BI assets like software assets.

## Key Concepts

- **PBIR as report source format**: PBIR is a file-based representation of Power BI reports intended to make report definitions easier to inspect, version, and automate. Instead of treating a report as a monolithic binary artifact, PBIR exposes report structure such as pages, visuals, and settings in a form that CLI tools can manipulate.
- **CLI-driven report engineering**: pbir-cli enables common report maintenance tasks from the shell instead of through Power BI Desktop. This is useful for bulk updates, reproducibility, scripting, and integration with source control and deployment pipelines.
- **TMDL hot reload**: TMDL is a model definition format used to represent semantic model metadata. Hot reloading TMDL into Power BI Desktop shortens the edit-test cycle by pushing model changes into an open report environment without fully rebuilding work manually.
- **Validation granularity**: Validation checks help detect malformed report definitions, unsupported properties, or inconsistent visual configurations. Granular control over validation lets engineers choose strict checks for CI environments or relaxed checks while experimenting with transformations.
- **Bulk styling operations**: Font and color changes are common but tedious when applied manually across many pages and visuals. CLI-based bulk operations allow consistent branding or remediation work to be applied programmatically to many report artifacts at once.
- **Visual query extraction**: A visual in a PBIR report often contains enough metadata for tooling to reconstruct the DAX query behind it. Extracting that query from a visual.json file helps debugging, performance analysis, and learning how a visual is resolved without opening the Performance Analyzer UI.
- **Legacy-to-PBIR conversion**: Older Power BI report formats are harder to automate because they are less transparent and less source-control friendly. Experimental conversion to PBIR aims to bring existing reports into a modern workflow where they can be inspected and modified by code.

## How It Works

The source describes pbir-cli as an automation layer over Power BI report artifacts, especially reports stored in PBIR format. The core idea is that a report is no longer treated as an opaque document; instead, the CLI reads and updates file-based definitions for report pages, visuals, styling, and metadata. Once report internals are accessible as files, tasks that are painful in the UI become straightforward shell commands.

A typical workflow starts with a local PBIR report project. The tool can inspect report content, validate structure, and modify properties in bulk. For example, engineers can apply shared font or color changes across many visuals, or run validation before committing report changes. This is especially valuable when a report repository contains dozens of pages or repeated design patterns.

Another important capability is **hot reloading TMDL to Power BI Desktop**. In practical terms, this shortens the loop between semantic model edits and report testing. Rather than repeatedly performing manual import or refresh steps, the CLI can push model-definition changes into the Desktop environment, making iterative development faster.

The update also highlights **screenshot automation**. Instead of manually navigating each page and exporting images one by one, the CLI can capture all report pages at once. This is useful for documentation, design review, regression testing, and pull request previews.

Validation has become more flexible. The tool now provides better discovery of visual type properties and more control over how strict validation should be. This implies a workflow like:

- strict validation in CI to catch invalid or unsupported report definitions
- lighter validation during local experiments
- optional disabling when testing transformations against edge-case reports

The post also mentions several **experimental commands**. These are noteworthy because they move the tool from convenience automation toward migration and observability:

- **Convert legacy reports to PBIR**: helps modernize existing assets.
- **Migrate thin report measures to the model**: useful when report-level measures should become centralized semantic-model measures.
- **Get report views**: retrieves workspace-, report-, and page-level usage metrics. For local reports, the report must first be linked to a published report through Fabric CLI so the local artifact has a service-side identity.

One especially practical feature is **DAX extraction from a visual**. If you point pbir-cli at a `visual.json` file, it can reconstruct the query and optionally save it as a `.dax` file. That means a report engineer can inspect how a visual is querying the model without launching Performance Analyzer. The caveats matter: not all visuals are supported, some queries are simplified, and visual calculations have limited support.

Conceptually, the data flow looks like this:

1. A report exists locally in PBIR form.
2. pbir-cli reads report files such as page and visual JSON definitions.
3. Commands either:
   - validate those files,
   - transform them,
   - extract derived information like DAX or usage metadata,
   - or synchronize model/report state with Power BI Desktop or Fabric.
4. The modified files can then be committed to source control or re-opened in Power BI tooling.

This makes pbir-cli part of a broader engineering pattern: **BI development as code**. Instead of relying only on manual authoring, the report definition becomes a programmable asset that can be tested, refactored, reviewed, and migrated systematically.

## Training Exercise

Build a small PBIR-oriented automation workflow and practice inspecting a visual.

1. **Install or upgrade the tool**
   ```bash
   uv tool install --upgrade pbir-cli
   ```

2. **Prepare a report project**
   - Use an existing PBIR-based Power BI report if you have one.
   - If you only have a legacy report, note that conversion is experimental; if available in your environment, try converting a copy rather than your primary file.

3. **Locate a visual definition**
   - In the report folder, find a visual JSON file, typically under a page/visual hierarchy.
   - Copy one visual file to a scratch area if you want to experiment safely.

4. **Extract the DAX query from the visual**
   - Run the relevant pbir-cli query-extraction command against the `visual.json` file.
   - Save the output as a `.dax` file if the command supports it.
   - Inspect the generated query and compare it with what you expected the visual to request.

5. **Run validation with different strictness**
   - Run validation normally.
   - Then rerun it with reduced granularity or disabled checks if supported.
   - Observe which warnings are useful for CI versus which are only noise during local editing.

6. **Perform a bulk style edit**
   - Choose one cosmetic property, such as a font family or color.
   - Use the appropriate pbir-cli bulk operation to update that property across multiple visuals or pages.
   - Review the changed files in git diff to see how the tool edits PBIR artifacts.

7. **Generate screenshots for review**
   - Run the screenshot-all-pages command.
   - Store the images in a folder such as `artifacts/screenshots/`.
   - Consider how these could be attached to pull requests for design review.

8. **Optional advanced step: hot reload TMDL**
   - If you also work with a semantic model in TMDL and have Power BI Desktop open, test the hot reload workflow.
   - Make a small model change, push it, and confirm the report reflects the updated model behavior.

Example shell workflow:
```bash
uv tool install --upgrade pbir-cli
# inspect your repo structure
find . -name "visual.json"
# then run the appropriate pbir-cli commands for:
# - validation
# - query extraction
# - bulk style updates
# - screenshot generation
```

What to learn from the exercise:
- how PBIR exposes report internals as editable files
- how CLI automation reduces repetitive UI work
- where extracted DAX is accurate versus simplified
- how validation and bulk edits fit into a source-controlled BI workflow

## Further Reading

- [Power BI Project (PBIP) and source control documentation](https://learn.microsoft.com/power-bi/developer/projects/projects-overview)
- [Tabular Model Definition Language (TMDL) overview](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview)
- [Microsoft Fabric documentation](https://learn.microsoft.com/fabric/)
- [DAX overview](https://learn.microsoft.com/dax/dax-overview)
