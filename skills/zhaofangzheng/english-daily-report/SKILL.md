---
name: english-daily-report
description: Generate daily English learning reports with news summaries. Use when user wants to: (1) Receive daily English news summaries for learning, (2) Get Chinese translations and vocabulary notes, (3) Generate PDF and audio versions for offline study, (4) Set up automated daily English learning schedules via cron
homepage: https://github.com/openclaw/openclaw
metadata: { "openclaw": { "emoji": "📰", "requires": { "bins": ["node"] } } }
---

# English Daily Report Skill

Generate daily English learning reports with news summaries, Chinese translations, vocabulary notes, PDF and audio versions.

## Quick Start

```bash
# Generate report manually
~/.openclaw/workspace/skills/english-daily-report/scripts/generate-pdf-html.sh \
  "2026-03-21" \
  "News Title" \
  "English content (~100 words)" \
  "中文翻译" \
  "word1:释义 1" \
  "word2:释义 2"

# Or set up automated daily reports via cron
openclaw cron add --name "英语学习计划" --cron "0 30 9 * * *" --session isolated --message "..."
```

## Workflow

### 1. Fetch News

Use `web_search` or `web_fetch` to get today's English news:

```
- Use web_search with freshness="pd" for today's news
- Or web_fetch specific news URLs (Reuters, BBC, NPR, etc.)
- Select 1-2 relevant stories
```

### 2. Create Summary

Create a ~100 word English summary with:

- **Title**: Clear, descriptive headline
- **Content**: ~100 words covering key facts
- **Chinese translation**: Complete translation (全文释义)
- **Vocabulary**: 5-8 uncommon words with Chinese meanings

### 3. Generate PDF

Use the bundled script:

```bash
scripts/generate-pdf-html.sh "DATE" "TITLE" "CONTENT" "TRANSLATION" "word1:meaning1" ...
```

The script:
- Creates HTML with beautiful gradient header
- Uses system default fonts (auto-detects Chinese fonts)
- Converts to PDF via Chrome headless
- Saves to `uploads/english-daily-DATE.pdf`

### 4. Generate Audio

Use TTS tool to convert English summary to speech:

```
tts text="<English news summary>"
```

Save to `uploads/english-daily-DATE.mp3`

### 5. Send to User

Send three messages via Feishu (or other channel):

1. **Text version**: Formatted summary with vocabulary notes
2. **Audio version**: TTS-generated MP3 for listening practice
3. **PDF version**: Printable PDF with beautiful layout

## Cron Setup

For automated daily reports at 9:30 AM:

```bash
openclaw cron add \
  --name "英语学习计划" \
  --description "每天 9:30 发送英文时报" \
  --cron "0 30 9 * * *" \
  --tz "Asia/Shanghai" \
  --session "isolated" \
  --message "Generate English Daily Report for user <USER_ID>:

1. Fetch today's English news
2. Create ~100 word summary with title, content, Chinese translation, 5-8 vocabulary words
3. Generate PDF: scripts/generate-pdf-html.sh \"DATE\" \"TITLE\" \"CONTENT\" \"TRANSLATION\" \"word1:meaning1\" ...
4. Generate audio: Use TTS tool for English summary
5. Send text + audio + PDF to user

Save files to uploads/english-daily-DATE.pdf and uploads/english-daily-DATE.mp3"
```

## File Structure

```
english-daily-report/
├── SKILL.md (this file)
├── scripts/
│   └── generate-pdf-html.sh  # PDF generation script
└── references/
    └── example-report.md     # Example report format
```

## Output Format

### Text Version

```
📰 English Daily Report - YYYY-MM-DD

**News Title**

English content (~100 words)...

---

📖 全文释义

中文完整翻译...

---

📝 Vocabulary & Grammar Notes:

- **word1** (pos.): 中文释义
- **word2** (pos.): 中文释义
...
```

### PDF Version

- Gradient header with title and date
- English summary section
- Chinese translation section
- Vocabulary section with highlighted words
- Footer with learning plan branding

### Audio Version

- TTS-generated English narration
- Clear pronunciation for learning
- Saved as MP3 for offline listening

## Tips

- **News sources**: Reuters, BBC, NPR, AP News for quality English
- **Word selection**: Choose 5-8 uncommon but useful words
- **Audio length**: Keep under 1 minute for better engagement
- **PDF design**: System fonts auto-detect Chinese characters
- **Consistency**: Send at same time daily for habit formation

## Troubleshooting

### PDF Chinese characters show as squares

This should not happen on macOS (auto-detects Chinese fonts). If you see squares:
- Check Chrome is installed: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Ensure system has Chinese font support

### TTS audio not saving

TTS tool delivers audio automatically. Use `message` tool to send the audio file path.

### Cron job not running

Check cron status:
```bash
openclaw cron list
openclaw cron status
```
