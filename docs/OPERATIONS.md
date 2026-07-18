# Second Brain Operations

## Permanent Host

Run the Telegram bot only on the Mac mini. The GitHub repository remains the shared source of truth across machines.

Initial setup:

```bash
cd /Users/steviecopilot/Stevie_Code/Second_Brain
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r ingest/requirements.txt
npm install -g @openai/codex
codex login
cp .env.example .env.local
```

When you run `codex login`, choose **Sign in with ChatGPT** so usage bills against your ChatGPT monthly plan. Do not paste an OpenAI Platform API key.

Copy Telegram and GitHub values from the retired `LinkToNotionLessons` `.env.local`. Do **not** copy `OPENAI_API_KEY`, Notion, or Gmail settings; they are unused.

Confirm ChatGPT-managed auth:

```bash
AUTH_FILE="${CODEX_HOME:-$HOME/.codex}/auth.json"
jq '{auth_mode, has_refresh_token: ((.tokens.refresh_token // "") != "")}' "$AUTH_FILE"
```

Expect `auth_mode` of `"chatgpt"` (or equivalent ChatGPT-managed mode) and a refresh token.

## launchd

The checked-in example is `deploy/com.stevie.secondbrain.plist.example`.

Install it:

```bash
cp deploy/com.stevie.secondbrain.plist.example ~/Library/LaunchAgents/com.stevie.secondbrain.plist
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.stevie.linktonotion.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.stevie.secondbrain.plist
```

Do not load the new service before stopping `com.stevie.linktonotion`; two processes cannot poll the same Telegram token.

The launch agent needs `HOME` set (so Codex finds `~/.codex/auth.json`) and a `PATH` that includes the `codex` binary. The example plist sets `HOME` and includes `/opt/homebrew/bin` and `/usr/local/bin`. If you install Codex through nvm, append that node bin directory to the plist `PATH` before bootstrapping.

Check it:

```bash
launchctl list | grep com.stevie.secondbrain
tail -f ~/Library/Logs/SecondBrain.err.log
```

## Updating the Bot

```bash
cd /Users/steviecopilot/Stevie_Code/Second_Brain
git pull --ff-only
source .venv/bin/activate
python -m pip install -r ingest/requirements.txt
launchctl kickstart -k gui/$(id -u)/com.stevie.secondbrain
```

If Codex returns auth errors after a long idle period, run `codex login` again on the Mac mini under the same OS user that owns the launch agent, then restart the service.

## Safe Development

- Use a separate development Telegram bot token.
- Use a fine-grained GitHub token limited to this repository.
- Run tests before restarting the service.
- Keep `.env.local` and `~/.codex/auth.json` only on the host; never commit them.
- Do not share one `auth.json` across concurrent machines or jobs.
- Do not delete the old repository until the new service has processed several real links successfully.

## Recovery

Captures are idempotent after migration. A normalized URL fingerprint is included in every new filename. If a request fails before publishing, send it again. If it already published, the bot returns the existing article instead of paying for another generation.
