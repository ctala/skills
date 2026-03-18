---
name: weread-import
description: Export WeRead highlights and notes into Markdown files, usually into an Obsidian Reading folder. Use when the user asks to import or sync WeRead books, re-render exported notes after template or merge changes, verify deleted/archive behavior, update frontmatter tags, or run WeRead export with browser cookie extraction or manual cookie input.
---

# weread-import

This skill now carries its own CLI entrypoint in `scripts/weread-import.mjs` and runs through `scripts/run.sh`.

## First run

Install the bundled runtime dependency once inside `scripts/`:

```bash
cd scripts
npm install
```

Then run the skill via `./scripts/run.sh`.

## Default path

1. Prefer `--mode api`.
2. Prefer `--cookie-from browser` when a Chrome remote debugging session is available.
3. Prefer validating in a temporary output directory first when changing template / merge / frontmatter behavior.
4. After validation, re-run against the real output directory.
5. Use `--force` when the goal is re-render / verification instead of incremental skip.

For concrete command templates, read `references/workflows.md`.

## Recommended command shapes

```bash
# Single book
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading"

# All books
bash ./scripts/run.sh --all --mode api --cookie-from browser --output "/path/to/Reading"

# Re-render existing file
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading" --force

# Override frontmatter tags
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading" --tags "reading/weread,book"
```

## Parameters worth exposing

- `--all`
- `--book <title>`
- `--book-id <id>`
- `--output <dir>`
- `--mode <auto|api|dom>`
- `--cookie <cookie>`
- `--cookie-from <manual|browser>`
- `--force`
- `--tags <a,b,c>`

## Operational notes

- Browser-cookie flow depends on a live Chrome remote debugging session, usually `http://127.0.0.1:9222`.
- Merge stats support added / updated / retained / deleted.
- Deleted items are archived under `## 已删除` instead of being dropped.
- Frontmatter is enabled;正文不再重复 `## 元信息`.
- If the WeRead API returns a business error such as login timeout, the CLI now fails loudly instead of silently exporting empty results.
- The skill is self-contained at the script level, but still expects the runtime environment to provide Node.js and the required Playwright dependency.

## Resources

### scripts/
- `scripts/run.sh`: main execution entrypoint for the skill
- `scripts/weread-import.mjs`: bundled CLI implementation
- `scripts/open-chrome-debug.sh`: helper for launching Chrome with remote debugging
- `scripts/package.json`: local runtime dependency definition for the skill

### references/
- `references/workflows.md`: recommended command patterns, validation flow, and common failure handling.
