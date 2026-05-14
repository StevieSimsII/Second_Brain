# 🧠 Stevie's Second Brain

A fully automated personal knowledge base that reads emails you send yourself, processes them with an LLM, and publishes them as a searchable wiki — hosted on GitHub Pages.

**Live site:** [steviesimsii.github.io/Second_Brain](https://steviesimsii.github.io/Second_Brain)

---

## How It Works

1. **You send an email to yourself** with a link or notes and drop it in an Outlook folder called `Learnings`
2. **GitHub Actions runs daily** (8am CT) and reads any new emails via the Microsoft Graph API
3. **OpenAI processes each email** — either fetching the linked article and generating a structured wiki page, or converting your raw notes directly into a wiki entry
4. **A static HTML site is rebuilt** and pushed back to the repo, updating your GitHub Pages site automatically
5. **Optionally**, a Notion page is created in parallel for each entry

This follows the [LLM-wiki pattern](https://karpathy.ai) — a persistent, compounding knowledge base maintained incrementally by LLMs.

```
You → Email (Outlook Learnings folder)
         ↓
    GitHub Actions (daily cron)
         ↓
    Microsoft Graph API (reads emails)
         ↓
    OpenAI gpt-4o (generates wiki pages)
         ↓
    wiki/pages/*.md  +  Notion pages
         ↓
    build_site.py → index.html
         ↓
    GitHub Pages (public site)
```

---

## Prerequisites

- A **GitHub account** with a public (or private + Pages-enabled) repository
- A **Microsoft 365 account** with Outlook (personal or work)
- An **OpenAI API key** (gpt-4o)
- An **Azure account** (free tier works) for Microsoft Graph API access
- Python 3.11+
- (Optional) A **Notion account** and integration token

---

## Setup Guide

### Step 1 — Fork or Clone This Repo

```bash
git clone https://github.com/StevieSimsII/Second_Brain.git
cd Second_Brain
```

Or click **Fork** at the top of this page to create your own copy under your GitHub account.

---

### Step 2 — Create Your Outlook Folder

In Outlook, create a folder called **`Learnings`** (or any name you prefer — you'll configure it later).

Whenever you find something worth saving, forward it or email yourself a link and move it to this folder.

---

### Step 3 — Register an Azure App (Microsoft Graph API)

This is how the pipeline reads your Outlook emails without storing your password.

1. Go to [portal.azure.com](https://portal.azure.com) → **Azure Active Directory** → **App registrations**
2. Click **New registration**
   - Name: `Second Brain` (or anything you like)
   - Supported account types: **Accounts in this organizational directory only** (or Multitenant if personal)
   - Redirect URI: leave blank
3. Click **Register** — copy the **Application (client) ID** and **Directory (tenant) ID**

#### 3a — Add Permissions for Local Dev (Delegated)

1. In your app → **API permissions** → **Add a permission** → **Microsoft Graph** → **Delegated permissions**
2. Search for and add: `Mail.Read`
3. Click **Grant admin consent**

#### 3b — Add Permissions for CI/GitHub Actions (Application)

1. **API permissions** → **Add a permission** → **Microsoft Graph** → **Application permissions**
2. Search for and add: `Mail.Read`
3. Click **Grant admin consent for [your tenant]** — you must see a green checkmark

#### 3c — Enable Public Client (for local device code flow)

1. In your app → **Authentication** → scroll to **Advanced settings**
2. Set **Allow public client flows** → **Yes**
3. Click **Save**

#### 3d — Create a Client Secret (for GitHub Actions)

1. In your app → **Certificates & secrets** → **Client secrets** → **New client secret**
2. Description: `second-brain-ci`, Expiry: 24 months → **Add**
3. **Copy the Value immediately** — it disappears after you navigate away

---

### Step 4 — Get an OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new secret key and copy it

---

### Step 5 — (Optional) Set Up Notion

If you want Notion pages created alongside wiki pages:

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) → **New integration**
2. Give it a name, select your workspace → **Submit** → copy the **Internal Integration Token**
3. In Notion, open the parent page where new entries should be created
4. Click **...** (top right) → **Add connections** → select your integration
5. Copy the page ID from the URL: `notion.so/Your-Page-Title-`**`abc123def456`** (the last 32 characters)

---

### Step 6 — Configure Local Environment

Create a `.env.local` file in the project root (this file is gitignored — never commit it):

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Microsoft Graph
GRAPH_CLIENT_ID=your-azure-app-client-id
GRAPH_TENANT_ID=your-azure-tenant-id

# Outlook folder to watch
OUTLOOK_FOLDER=Learnings

# Notion (optional)
NOTION_API_KEY=secret_...
NOTION_PARENT_PAGE_ID=abc123...

# GitHub token (optional, for richer GitHub repo pages)
GITHUB_TOKEN=ghp_...
```

---

### Step 7 — Install Dependencies and Run Locally

```bash
pip install -r requirements.txt
```

**First run — authenticate with Microsoft (device code flow):**

```bash
python process.py --dry-run
```

A URL and code will be printed. Open the URL in your browser, enter the code, and sign in with your Microsoft account. A token cache is saved locally so you won't need to do this again for ~90 days.

**Process all emails (backlog — body only):**

```bash
python process.py --body-only
```

Use `--body-only` when your emails contain your own notes. Use the default mode (no flag) when emails contain URLs you want the LLM to fetch and summarize.

**Process new emails (URL fetch mode — ideal for going forward):**

```bash
python process.py
```

**Rebuild the site:**

```bash
python build_site.py
```

This regenerates `index.html` from all `wiki/pages/*.md` files.

**Other useful flags:**

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview what would be processed without writing files or calling APIs |
| `--reprocess` | Re-run all emails, ignoring the `.processed.json` history |
| `--body-only` | Use email body as wiki content, skip URL fetching |

---

### Step 8 — Add GitHub Repository Secrets

For the GitHub Action to run, add these secrets to your repo:

**Repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|-------------|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `GRAPH_CLIENT_ID` | Azure app client ID |
| `GRAPH_TENANT_ID` | Azure tenant ID |
| `GRAPH_CLIENT_SECRET` | Azure client secret value (from Step 3d) |
| `GRAPH_USER_EMAIL` | Your Microsoft 365 email address |
| `NOTION_API_KEY` | Your Notion integration token (optional) |
| `NOTION_PARENT_PAGE_ID` | Your Notion parent page ID (optional) |

---

### Step 9 — Enable GitHub Pages

1. Go to your repo on GitHub → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, Folder: `/ (root)`
4. Click **Save**

Your site will be live at `https://yourusername.github.io/Second_Brain` within a minute.

---

### Step 10 — Push Your Repo

```bash
git add .
git commit -m "init: my second brain"
git push
```

The GitHub Action will run daily at 8am CT, or you can trigger it manually any time:

**Repo → Actions → Sync Second Brain → Run workflow**

---

## Project Structure

```
Second_Brain/
├── .github/
│   └── workflows/
│       └── sync.yml          # GitHub Actions workflow (daily cron)
├── wiki/
│   └── pages/                # Generated wiki pages (markdown)
├── ingest/
│   └── outlook.py            # Microsoft Graph API email reader
├── llm/
│   └── gpt.py                # OpenAI page generation
├── fetchers/
│   ├── web.py                # Article fetcher (BeautifulSoup)
│   └── github.py             # GitHub repo fetcher
├── notionapi/
│   └── client.py             # Notion page creator
├── process.py                # Main pipeline entry point
├── build_site.py             # Static site generator
├── wiki_manager.py           # Wiki file writer / index updater
├── config.py                 # Environment config loader
├── requirements.txt
├── .env.example              # Template — copy to .env.local and fill in
├── .processed.json           # Tracks processed email IDs (committed to repo)
└── index.html                # Generated site (committed, served by GitHub Pages)
```

---

## Customization

**Change the Outlook folder name:**
Set `OUTLOOK_FOLDER=YourFolderName` in `.env.local` and in the GitHub secret.

**Change the cron schedule:**
Edit `.github/workflows/sync.yml` — the `cron` line uses UTC. `0 13 * * *` = 8am CT.

**Change the OpenAI model:**
Set `OPENAI_MODEL=gpt-4-turbo` (or any chat model) in `.env.local`.

**Run on a private repo:**
GitHub Pages is available on private repos with a GitHub Pro/Teams plan. Everything else works the same.

---

## License

MIT — fork it, customize it, make it yours.
