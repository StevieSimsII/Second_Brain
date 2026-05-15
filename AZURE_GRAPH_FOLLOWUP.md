# Sync Second Brain Follow-Up

## What failed

The scheduled GitHub Actions run on May 14, 2026 failed in the `Process new emails` step.

The failing request was:

- `GET https://graph.microsoft.com/v1.0/users/{GRAPH_USER_EMAIL}/mailFolders`

The error was:

- `403 Forbidden`

This means the cron trigger is working, but the Azure/Microsoft Graph app does not currently have the mailbox access the workflow needs.

## What was already fixed locally

- Added `.processed.json` so the workflow will not later fail on `git add .processed.json`
- Improved Graph error reporting in `ingest/outlook.py` so the next failure log is more actionable

## What to check in Azure

1. Open **Microsoft Entra admin center**.
2. Go to **App registrations**.
3. Open the app used by this repo.
4. Go to **API permissions**.
5. Confirm **Microsoft Graph** includes **Application** permission `Mail.Read`.
6. Click **Grant admin consent** if it is not already granted.

## What to check in GitHub Secrets

Open this repo in GitHub and verify these Actions secrets:

- `GRAPH_CLIENT_ID`
- `GRAPH_TENANT_ID`
- `GRAPH_CLIENT_SECRET`
- `GRAPH_USER_EMAIL`

Checks:

- `GRAPH_USER_EMAIL` must be the exact Exchange Online mailbox address to read
- The client ID, tenant ID, and secret must belong to the same Azure app
- The mailbox must be in that tenant

## If it still returns 403

Check whether Exchange Online is restricting the app with either of these:

- App RBAC for Exchange applications
- Legacy Application Access Policies

## After Azure is fixed

1. Re-run the `Sync Second Brain` workflow manually.
2. Confirm `Process new emails` succeeds.
3. Confirm the workflow reaches `Rebuild site`.
4. Confirm the workflow reaches `Commit and push changes`.
5. Confirm GitHub Pages updates as expected.

## Useful links

- Failed run: https://github.com/StevieSimsII/Second_Brain/actions/runs/25862863832
- Graph permissions reference: https://learn.microsoft.com/en-us/graph/permissions-reference
- List mailFolders: https://learn.microsoft.com/en-us/graph/api/user-list-mailfolders?view=graph-rest-1.0
- Exchange app mailbox scoping: https://learn.microsoft.com/en-us/graph/auth-limit-mailbox-access
- Legacy application access policies: https://learn.microsoft.com/en-us/exchange/permissions-exo/application-access-policies
