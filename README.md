# 🧠 Stevie's Second Brain

---

## How It Works

```
You (phone or desktop)
       ↓
  Send URL to your private Telegram bot
       ↓
  LinkToNotion bot fetches the article
       ↓
  OpenAI gpt-4o generates a structured lesson
       ↓
  Notion page created
       ↓
  Gmail sends a lesson email → your Outlook inbox
       ↓
  Outlook rule moves it to your Learnings folder (automatic)
       ↓
  GitHub Actions (daily 8am CT)
       ↓
  Microsoft Graph reads Learnings folder
       ↓
  wiki/pages/*.md rebuilt + Notion page updated
       ↓
  index.html committed → GitHub Pages site updated
```

---

## What You'll Need

**Two repos:**
- **This repo** (`Second_Brain`) — the GitHub Actions pipeline that reads your email and builds the site
- **[LinkToNotion](https://github.com/StevieSimsII/LinkToNotion)** — the Telegram bot that processes URLs and sends the emails

**Accounts and keys:**
- GitHub account
- Microsoft 365 / Outlook account
- Azure account (free tier) — for Microsoft Graph API
- OpenAI API key
- Telegram account
- Gmail account (used only to send lesson emails to yourself)
- Notion account (optional)

---

## Setup Guide

### Part 1 — Telegram Bot (LinkToNotion)

This is the front door. You'll set this up first so you can start capturing articles immediately.

---

#### Step 1 — Clone LinkToNotion

```bash
git clone https://github.com/StevieSimsII/LinkToNotion.git
cd LinkToNotion
pip install -r requirements.txt
```

---

#### Step 2 — Create Your Telegram Bot

1. Open Telegram → search for **@BotFather**
2. Send `/newbot`
3. Enter a display name (e.g. `My Second Brain`)
4. Enter a username ending in `bot` (e.g. `my_secondbrain_bot`)
5. BotFather replies with your **bot token** — looks like `123456789:ABCdef...`
6. Copy it — you'll need it in Step 6

---

#### Step 3 — Get Your Telegram User ID

The bot only responds to you — this is how it knows who you are.

1. In Telegram, search for **@userinfobot**
2. Send `/start`
3. It replies with your numeric user ID — e.g. `123456789`
4. Copy it

---

#### Step 4 — Create a Gmail App Password

The bot sends lesson emails via Gmail SMTP. You need an App Password, not your regular Gmail password.

1. Go to your Google Account → [myaccount.google.com/security](https://myaccount.google.com/security)
2. Make sure **2-Step Verification** is turned on (required)
3. Search for **App passwords** → [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
4. App: **Mail**, Device: **Other** → type `Second Brain Bot` → **Generate**
5. Copy the 16-character password — it won't be shown again

---

#### Step 5 — Get an OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new secret key and copy it

---

#### Step 6 — Configure LinkToNotion

Create `LinkToNotion/.env.local` (never commit this file):

```env
# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
ALLOWED_TELEGRAM_USER_ID=123456789

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Gmail — sends lesson emails to your Outlook
GMAIL_USER=yourname@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
EMAIL_TO=you@outlook.com

# Notion (optional — skip if not using)
NOTION_API_KEY=secret_...
NOTION_PARENT_PAGE_ID=abc123...

# GitHub token (optional — richer summaries for GitHub repo URLs)
GITHUB_TOKEN=ghp_...
```

> **`EMAIL_TO`** must be your Microsoft 365 / Outlook address — this is where lesson emails land so the Second Brain pipeline can pick them up.

---

#### Step 7 — Start the Bot and Test It

```bash
python main.py
```

You should see:
```
Starting LinkToNotion bot...
Bot ready. Press Ctrl+C to stop.
```

Open Telegram, find your bot by its username, send `/start` to confirm it responds, then send any URL:

```
https://some-article.com/interesting-read
```

Within ~30 seconds you'll get back:

```
Done.

*Your Article Title*
Notion: https://notion.so/...
Email sent to you@outlook.com
```

Check your Outlook inbox — a formatted lesson email will be there with a markdown attachment.

---

#### Step 8 — Set Up the Outlook Rule (Closes the Loop)

This rule automatically moves every bot-generated email into your Learnings folder so the pipeline picks it up without any manual steps.

1. In Outlook → **Settings** → **Rules** → **Add new rule**
2. **Condition:** Subject contains `[Lesson]`
3. **Action:** Move to folder → `Learnings` (create this folder if it doesn't exist yet)
4. Save

From now on: send URL on phone → lesson email lands in Learnings → wiki page appears on your site the next morning.

---

#### Keeping the Bot Running

The bot needs to be running to receive messages. Options:

| Option | How |
|--------|-----|
| **Windows Task Scheduler** | Trigger at startup → run `python main.py` in the LinkToNotion directory |
| **Cheap VPS** (e.g. DigitalOcean $4/mo) | `python main.py` in a `tmux` session or as a `systemd` service |
| **Railway / Render** | Free tier works — point the start command at `python main.py` |

---

### Part 2 — Second Brain Pipeline (This Repo)

This is what reads your Learnings folder each morning, generates wiki pages, and updates the site.

---

#### Step 9 — Fork or Clone This Repo

```bash
git clone https://github.com/StevieSimsII/Second_Brain.git
cd Second_Brain
pip install -r requirements.txt
```

Or click **Fork** at the top of this page to create your own copy.

---

#### Step 10 — Register an Azure App (Microsoft Graph API)

This lets the pipeline read your Outlook emails without storing your password.

1. Go to [portal.azure.com](https://portal.azure.com) → **Azure Active Directory** → **App registrations**
2. Click **New registration**
   - Name: `Second Brain`
   - Supported account types: **Accounts in this organizational directory only**
   - Redirect URI: leave blank
3. Click **Register** — copy the **Application (client) ID** and **Directory (tenant) ID**

**Add delegated permission (for local dev):**
1. **API permissions** → **Add a permission** → **Microsoft Graph** → **Delegated permissions**
2. Search for `Mail.Read` → add it → **Grant admin consent**

**Add application permission (for GitHub Actions CI):**
1. **API permissions** → **Add a permission** → **Microsoft Graph** → **Application permissions**
2. Search for `Mail.Read` → add it → **Grant admin consent** — confirm the green checkmark

**Enable public client flow (for local device code auth):**
1. **Authentication** → scroll to **Advanced settings**
2. Set **Allow public client flows** → **Yes** → **Save**

**Create a client secret (for GitHub Actions):**
1. **Certificates & secrets** → **Client secrets** → **New client secret**
2. Description: `second-brain-ci`, Expiry: 24 months → **Add**
3. **Copy the Value immediately** — it disappears after you navigate away

---

#### Step 11 — (Optional) Set Up Notion

If you want Notion pages created in parallel with wiki pages:

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) → **New integration**
2. Name it, select your workspace → **Submit** → copy the **Internal Integration Token**
3. Open the Notion page where new entries should live
4. Click **...** → **Add connections** → select your integration
5. Copy the page ID from the URL — the last 32 characters after the final `-`

---

#### Step 12 — Configure Local Environment

Create `Second_Brain/.env.local`:

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

# GitHub token (optional)
GITHUB_TOKEN=ghp_...
```

---

#### Step 13 — Authenticate with Microsoft (First Time Only)

```bash
python process.py --dry-run
```

A URL and code will be printed in your terminal. Open the URL in your browser, enter the code, and sign in with your Microsoft account. A token cache is saved locally — you won't need to do this again for ~90 days.

---

#### Step 14 — Add GitHub Repository Secrets

**Repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|-------------|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `GRAPH_CLIENT_ID` | Azure app client ID |
| `GRAPH_TENANT_ID` | Azure tenant ID |
| `GRAPH_CLIENT_SECRET` | Azure client secret value (from Step 10) |
| `GRAPH_USER_EMAIL` | Your Microsoft 365 email address |
| `NOTION_API_KEY` | Your Notion integration token (optional) |
| `NOTION_PARENT_PAGE_ID` | Your Notion parent page ID (optional) |

---

#### Step 15 — Enable GitHub Pages

1. Go to your repo on GitHub → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, Folder: `/ (root)`
4. Click **Save**

Your site will be live at `https://yourusername.github.io/Second_Brain` within a minute.

---

#### Step 16 — Push and Trigger Your First Run

```bash
git add .
git commit -m "init: my second brain"
git push
```

Then trigger the pipeline manually to verify everything works:

**Repo → Actions → Sync Second Brain → Run workflow**

After it completes, your site will reflect any emails already in your Learnings folder.

The workflow runs automatically every day at 8am CT. You can also trigger it manually any time from the Actions tab.

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
└── index.html                # Generated site (served by GitHub Pages)
```

---

## Useful CLI Flags

```bash
python process.py               # Normal run — fetch URLs and generate wiki pages
python process.py --dry-run     # Preview without writing files or calling APIs
python process.py --body-only   # Use email body directly, skip URL fetching
python process.py --reprocess   # Re-run all emails, ignore processed history
python build_site.py            # Rebuild index.html from wiki/pages/*.md
```

---

## Customization

**Change the Outlook folder name:** Set `OUTLOOK_FOLDER=YourFolderName` in `.env.local` and as a GitHub secret.

**Change the cron schedule:** Edit `.github/workflows/sync.yml`. The `cron` value uses UTC — `0 13 * * *` = 8am CT.

**Change the OpenAI model:** Set `OPENAI_MODEL=gpt-4-turbo` (or any chat model) in `.env.local`.

---

## License

MIT — fork it, customize it, make it yours.
