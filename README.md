# 🧠 Stevie's Second Brain

A fully automated personal knowledge base that reads emails you send yourself, processes them with an LLM, and publishes them as a searchable wiki — hosted on GitHub Pages.

**Live site:** [steviesimsii.github.io/Second_Brain](https://steviesimsii.github.io/Second_Brain)

---

## How It Works

There are two ways to feed your Second Brain. Both end up as wiki pages on your site.

### Path 1 — Direct Email (Core Pipeline)

1. **Email yourself** a link or notes and drop it in your Outlook `Learnings` folder
2. **GitHub Actions runs daily** (8am CT) and reads any new emails via the Microsoft Graph API
3. **OpenAI processes each email** — fetching the linked article and generating a structured wiki page, or converting your raw notes directly into a wiki entry
4. **A static HTML site is rebuilt** and pushed back to the repo, updating your GitHub Pages site automatically
5. **Optionally**, a Notion page is created in parallel for each entry

### Path 2 — Telegram Bot (Fast Capture, anywhere)

1. **Send a URL to your private Telegram bot** from your phone or desktop — takes 5 seconds
2. **The bot fetches the article**, calls OpenAI to generate a structured lesson, and creates a Notion page
3. **An email is sent to your Outlook address** with the full lesson summary + a markdown attachment
4. **Move that email into your Learnings folder** (or set up an Outlook rule to do it automatically)
5. **GitHub Actions picks it up** in the next daily run and adds it to your wiki

This follows the [LLM-wiki pattern](https://karpathy.github.io) — a persistent, compounding knowledge base maintained incrementally by LLMs.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PATH 1: Direct Email          PATH 2: Telegram Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Email yourself a link    OR   Send URL to Telegram bot
         ↓                              ↓
  Move to Learnings folder       Fetch + OpenAI lesson
                                        ↓
                               Notion page created
                                        ↓
                               Gmail → your Outlook
                                        ↓
                               Move to Learnings folder
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    Both paths converge here:

              GitHub Actions (daily 8am CT)
                         ↓
          Microsoft Graph API (reads Learnings folder)
                         ↓
            OpenAI gpt-4o (generates wiki pages)
                         ↓
          wiki/pages/*.md  +  Notion pages (optional)
                         ↓
           build_site.py → index.html committed
                         ↓
             GitHub Pages (your live public site)
```

---

## Prerequisites

**Core pipeline (required):**
- A **GitHub account** with a public (or private + Pages-enabled) repository
- A **Microsoft 365 account** with Outlook (personal or work)
- An **OpenAI API key** (gpt-4o)
- An **Azure account** (free tier) for Microsoft Graph API access
- Python 3.11+

**Telegram fast-capture (optional but recommended):**
- A **Telegram account** and the Telegram app on your phone
- A **Gmail account** with an App Password enabled (used to send lesson emails)

**Notion integration (optional):**
- A **Notion account** and integration token

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

---

## Bonus: Telegram Bot for On-the-Go Capture

The Telegram bot lives in a companion repo — [LinkToNotion](https://github.com/StevieSimsII/LinkToNotion) — and runs as a separate long-polling process on your machine (or a cheap VPS). Once it's running, you send it a URL from anywhere and it handles the rest.

### How the Email Loop Closes

The bot sends a formatted email (HTML + markdown attachment) to your configured `EMAIL_TO` address — your Outlook inbox. The email subject is `[Lesson] Your Article Title`. From there you have two options:

- **Manual:** Move the email into your `Learnings` folder whenever you want it in the wiki
- **Automatic (recommended):** Create an Outlook rule that moves any email with subject containing `[Lesson]` directly into `Learnings` — fully hands-off

### Telegram Bot Setup

#### Step T1 — Clone the LinkToNotion Repo

```bash
git clone https://github.com/StevieSimsII/LinkToNotion.git
cd LinkToNotion
pip install -r requirements.txt
```

#### Step T2 — Create a Telegram Bot via BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Give your bot a name (e.g., `My Second Brain`) and a username (e.g., `my_secondbrain_bot`)
4. BotFather will reply with your **bot token** — looks like `123456789:ABCdef...`
5. Copy it — you'll need it in your `.env.local`

#### Step T3 — Get Your Telegram User ID

You need your personal user ID so the bot only responds to you (not anyone who finds it).

1. In Telegram, search for **@userinfobot**
2. Send `/start`
3. It replies with your numeric user ID — e.g., `123456789`
4. Copy it

#### Step T4 — Create a Gmail App Password

The bot sends emails via Gmail SMTP. You need an App Password (not your regular Gmail password).

1. Go to your **Google Account** → [myaccount.google.com/security](https://myaccount.google.com/security)
2. Make sure **2-Step Verification** is turned on (required for App Passwords)
3. Search for **App passwords** (or go directly to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords))
4. Select app: **Mail**, Select device: **Other** → type `Second Brain Bot` → **Generate**
5. Copy the 16-character password shown — it won't be shown again

#### Step T5 — Configure LinkToNotion .env.local

Create `LinkToNotion/.env.local`:

```env
# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
ALLOWED_TELEGRAM_USER_ID=123456789

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Notion
NOTION_API_KEY=secret_...
NOTION_PARENT_PAGE_ID=abc123...

# Gmail (sends lesson emails to your Outlook)
GMAIL_USER=yourname@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
EMAIL_TO=you@youroutlook.com

# GitHub token (optional — for richer GitHub repo summaries)
GITHUB_TOKEN=ghp_...
```

> **Important:** `EMAIL_TO` should be your Outlook/Microsoft 365 address — this is where the lesson email lands so the Second Brain pipeline can pick it up.

#### Step T6 — Start the Bot

```bash
cd LinkToNotion
python main.py
```

You should see:
```
Starting LinkToNotion bot...
Bot ready. Press Ctrl+C to stop.
```

Now open Telegram, find your bot by the username you created, and send `/start` to verify it responds.

#### Step T7 — Send Your First Link

Send any URL to your bot:

```
https://some-article.com/interesting-thing
```

The bot will reply:
```
Processing: https://some-article.com/interesting-thing
This can take a minute...
```

Then within ~30 seconds:
```
Done.

*Your Article Title*
Notion: https://notion.so/...
Email sent to you@youroutlook.com
Wiki note: wiki/pages/2026-05-14-your-article-title.md
```

Check your Outlook inbox — you'll have a formatted email with the full lesson.

#### Step T8 — (Recommended) Set Up an Outlook Rule

To fully automate the loop so every bot-processed article lands in your Second Brain without any manual steps:

1. In Outlook, go to **Settings** → **Rules** → **Add new rule**
2. **Condition:** Subject contains `[Lesson]`
3. **Action:** Move to folder → `Learnings`
4. Save the rule

Now the complete flow is touchless: send URL on phone → wiki page appears on your site the next morning.

#### Running the Bot Persistently

For the bot to work when your computer is off, run it on a lightweight server:

- **Windows Task Scheduler** — trigger at startup, run `python main.py` in the LinkToNotion directory
- **A cheap VPS** (e.g., DigitalOcean $4/mo droplet) running `python main.py` in a `tmux` or `screen` session, or as a `systemd` service
- **Railway / Render** — free tier is enough; point it at the `main.py` entry point

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
