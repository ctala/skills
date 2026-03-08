---
name: safe-email
description: Privacy-first email processing workflow for creating calendar events or reminders from forwarded emails via IMAP. Use when a user explicitly asks to process a newly forwarded email in a dedicated mailbox. Requires explicit user trigger, reads only the newest relevant message, and deletes processed email content afterward.
---

# Safe Email (Privacy-First)

Use this skill to process forwarded emails safely and convert actionable items into:
- calendar events, and/or
- reminders/tasks

This skill is intentionally **conservative** and **opt-in only**.

## What users must know first

1. **Use a dedicated email inbox** (recommended: a brand-new Gmail account) for AI processing.
   - Do not connect a personal primary inbox.
   - Keep this mailbox purpose-limited (only forwarded emails for automation).

2. **Forward emails to that dedicated inbox** before asking the assistant to process them.
   - If users do not forward the email, there may be nothing to parse.
   - State this clearly in user-facing instructions.

3. **IMAP access requires a Gmail App Password** (for Gmail with 2FA enabled).

## Security rules (non-negotiable)

1. **Never auto-check email** without explicit user instruction.
   - No background polling.
   - No scheduled inbox scans unless user explicitly sets one up.

2. **Process minimally**.
   - Read only what is needed.
   - Prefer the newest relevant message for the requested action.

3. **Delete processed email content after successful handling**.
   - Move to Trash and permanently expunge when possible.
   - If permanent deletion fails, report status clearly and retry safely.

4. **Ask before destructive or ambiguous actions** (except agreed post-processing deletion rule).

## Setup guide (Gmail + IMAP)

### 1) Create a dedicated Gmail account

Create a separate Gmail mailbox specifically for assistant workflows.

### 2) Enable 2-Step Verification on that account

Gmail App Password requires 2FA.

### 3) Create an App Password

In Google Account security settings:
- Go to **App passwords**
- Create a new app password for Mail/IMAP usage
- Store it in a secure secret manager or OS keychain

### 4) Configure IMAP/SMTP client (example: Himalaya)

Use standard Gmail servers:
- IMAP: `imap.gmail.com:993` (TLS)
- SMTP: `smtp.gmail.com:587` (STARTTLS)

Prefer command/keychain-based secret retrieval instead of plaintext passwords.

Example (conceptual):
```toml
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "your-dedicated-inbox@gmail.com"
backend.auth.type = "password"
backend.auth.cmd = "<secure-command-to-read-app-password>"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "your-dedicated-inbox@gmail.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "<secure-command-to-read-app-password>"
```

## Execution workflow

### Step 0 — Require explicit trigger

Only proceed when user says something like:
- “I just forwarded an email, process it.”
- “Read the latest forwarded email and create calendar/reminder entries.”

If not explicitly asked: stop.

### Step 1 — Read newest relevant email only

- List recent messages in inbox.
- Open only the newest candidate relevant to the user’s request.
- Avoid bulk reading old or unrelated emails.

### Step 2 — Extract structured details

Extract as available:
- title/subject
- date/time window
- location
- links
- notes/details (e.g., confirmation number, participants)
- action type (event vs reminder vs both)

If date/time is missing or ambiguous, ask user before creating entries.

### Step 3 — Create output in user’s preferred systems

This skill is calendar/reminder-system agnostic.
Use whatever tools the user already uses (Apple Calendar, Google Calendar, Notion tasks, Reminders, etc.).

Minimum expected output objects:
- **Calendar event**: title, start, end/duration, timezone, location, notes
- **Reminder/task**: title, due date/time (if known), notes, optional priority/list

### Step 4 — Delete processed email content

After successful creation:
1. Move processed email to Trash
2. Permanently delete/expunge when supported
3. Confirm deletion status to user

### Step 5 — Return concise confirmation

Include:
- what was created (event/reminder)
- key parsed fields (time/location)
- deletion status of processed email
- any unresolved ambiguity

## Failure handling

- If parsing fails: provide extracted partial fields and request confirmation.
- If calendar/reminder creation fails: do **not** delete email until user decides.
- If deletion fails: clearly report “processed but not fully deleted yet,” then retry.

## Default privacy posture

- Explicit user trigger only
- Minimum necessary access
- No automatic surveillance behavior
- Post-processing deletion by default
- Clear user-visible audit summary each run
