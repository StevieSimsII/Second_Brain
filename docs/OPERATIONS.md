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
cp .env.example .env.local
```

Copy the existing Telegram, OpenAI, and GitHub values from the retired repository's `.env.local`. Do not copy Notion or Gmail settings; they are unused.

## launchd

The checked-in example is `deploy/com.stevie.secondbrain.plist.example`.

Install it:

```bash
cp deploy/com.stevie.secondbrain.plist.example ~/Library/LaunchAgents/com.stevie.secondbrain.plist
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.stevie.linktonotion.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.stevie.secondbrain.plist
```

Do not load the new service before stopping `com.stevie.linktonotion`; two processes cannot poll the same Telegram token.

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

## Safe Development

- Use a separate development Telegram bot token.
- Use a fine-grained GitHub token limited to this repository.
- Run tests before restarting the service.
- Keep `.env.local` only on the host.
- Do not delete the old repository until the new service has processed several real links successfully.

## Recovery

Captures are idempotent after migration. A normalized URL fingerprint is included in every new filename. If a request fails before publishing, send it again. If it already published, the bot returns the existing article instead of paying for another generation.

