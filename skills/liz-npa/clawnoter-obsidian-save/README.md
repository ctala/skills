# Clawnoter Obsidian

Save web articles and links into a local Obsidian Vault with images, basic Markdown conversion, and optional user notes.

## What It Does

- Saves a webpage into your Obsidian Vault
- Downloads article images into an `images/` folder
- Stores article metadata in YAML frontmatter
- Supports quick notes appended by the user
- Includes first-run vault path configuration

## First Run

On first use, configure:

1. Your Obsidian Vault root path
2. An optional subfolder for saved articles

The configuration is stored in:

```text
~/.obsidian-save-article-config.json
```

## Typical Intents

- `查看保存路径`
- `重新配置`
- `保存到 Obsidian：https://example.com/article`
- `保存到 Obsidian：https://example.com/article 这是我的笔记`

## Runtime Requirements

- `python3`
- Network access to the target webpage
- A local writable Obsidian Vault

## Notes

- Primary fetch path uses `https://r.jina.ai/<URL>`
- If Jina fails, the skill falls back to raw HTML fetch plus local conversion
- Login-required or heavily JavaScript-rendered pages may not extract cleanly
