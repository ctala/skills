# AI Wallpaper Generator

Generate stunning AI-powered wallpaper images from a text description in seconds. Powered by the Neta talesofai API, this skill returns a direct image URL you can use anywhere.

---

## Install

**Via npx skills:**
```bash
npx skills add BarbaraLedbettergq/wallpaper-claw-skill
```

**Via ClawHub:**
```bash
clawhub install wallpaper-claw-skill
```

---

## Usage

```bash
# Use the default prompt
node wallpaperclaw.js

# Custom prompt
node wallpaperclaw.js "misty mountain range at golden hour"

# Specify size
node wallpaperclaw.js "cyberpunk city at night" --size landscape

# Use a reference image UUID
node wallpaperclaw.js "same style, different scene" --ref <picture_uuid>

# Pass token directly
node wallpaperclaw.js "aurora borealis over a frozen lake" --token YOUR_TOKEN
```

The script prints a single image URL to stdout on success.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `landscape` | Output image dimensions |
| `--style` | `anime`, `cinematic`, `realistic` | `cinematic` | Visual style (passed in prompt) |
| `--ref` | `<picture_uuid>` | — | Reference image UUID for style inheritance |
| `--token` | `<token>` | — | Override token resolution |

### Size reference

| Name | Dimensions |
|------|------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

---

## Token setup

The script resolves your `NETA_TOKEN` in this order:

1. `--token` CLI flag
2. `NETA_TOKEN` environment variable
3. `~/.openclaw/workspace/.env` — line matching `NETA_TOKEN=...`
4. `~/developer/clawhouse/.env` — line matching `NETA_TOKEN=...`

**Recommended:** add your token to `~/.openclaw/workspace/.env`:
```
NETA_TOKEN=your_token_here
```

---

## Example output

```
https://cdn.talesofai.cn/artifacts/abc123.jpg
```

---

Built with Claude Code · Powered by Neta
