---
name: claw-migrate
description: OpenClaw configuration migration tool. Use when users mention pulling configuration from GitHub, migrating OpenClaw configuration, syncing configuration, restoring configuration, or cloning configuration to a new machine. Supports pulling team configuration, skills, memory, etc. from GitHub private repositories, intelligently merging without overwriting local configuration.
homepage: https://github.com/hanxueyuan/claw-migrate
metadata:
  {"openclaw":{"emoji":"🔄","requires":{"bins":["node"],"env":["GITHUB_TOKEN"]},"primaryEnv":"GITHUB_TOKEN"}}
---

# claw-migrate - OpenClaw Configuration Migration Tool

## Features

Pull OpenClaw configuration from GitHub private repository to local, supports intelligent merging, preserves existing local configuration.

## Usage

### 🎯 Automatic Configuration After Installation

When you first install the `claw-migrate` skill, it will automatically trigger the configuration wizard to guide you through setting up your backup strategy.

```bash
# Install skill
openclaw skill install claw-migrate

# Automatically trigger configuration wizard
🎉 claw-migrate installation complete!

📋 Detected this is first-time installation, start configuring backup now?
   1. Yes, configure immediately (Recommended)
   2. No, configure manually later
```

### Manual Configuration

If you skipped automatic configuration, you can manually start anytime:

```bash
# Start configuration wizard
openclaw skill run claw-migrate setup

# View current configuration
openclaw skill run claw-migrate config

# Modify configuration
openclaw skill run claw-migrate config --edit
```

## File Migration Strategy

### Configuration Categories

| Configuration Type | File Examples | Migration Strategy |
|---------|---------|---------|
| **General Configuration** | AGENTS.md, SOUL.md, USER.md | Intelligent merge |
| **Skills** | skills/**/SKILL.md | Incremental sync (add missing only) |
| **Memory/Learning** | MEMORY.md, .learnings/*.md | Merge/Append |
| **Channel Configuration** | feishu/*.json | Preserve local (machine-specific) |
| **Pairing Information** | feishu/pairing/*.json | ❌ Do not migrate (machine-specific) |
| **Sensitive Information** | .env, sessions/*.jsonl | ❌ Do not migrate |

### Detailed Description

| File Type | Strategy | Description |
|---------|------|------|
| AGENTS.md, SOUL.md, IDENTITY.md, USER.md | Intelligent merge | Preserve local customization |
| TOOLS.md, HEARTBEAT.md | Intelligent merge | Preserve local customization |
| skills/ | Incremental sync | Only add skills that exist remotely but not locally |
| MEMORY.md, memory/ | Merge | Preserve local, append remote additions |
| .learnings/ | Append with deduplication | Append remote additions |
| .env | ❌ Do not migrate | Preserve local (API keys, etc.) |
| **feishu/dedup/*.json** | ❌ Do not migrate | Message deduplication IDs (machine-specific) |
| **feishu/pairing/*.json** | ❌ Do not migrate | Pairing information (machine-specific) |
| openclaw.json | Field-level merge | Preserve machine-specific fields like browser.executablePath |

## Command Arguments

```bash
openclaw skill run claw-migrate --repo <owner>/<repo> [options]
```

### Options

| Parameter | Short | Required | Description |
|------|------|------|------|
| `--repo` | `-r` | ✅ | GitHub repository (format: owner/repo) |
| `--branch` | `-b` | ❌ | Branch name (default: main) |
| `--path` | `-p` | ❌ | Path within repository (default: root directory) |
| `--type` | `-t` | ❌ | Migration type: `all` (default) `config` `memory` `learnings` `skills` |
| `--dry-run` | | ❌ | Preview mode, do not actually write files |
| `--no-backup` | | ❌ | Do not create backup (default creates backup) |
| `--verbose` | `-v` | ❌ | Verbose output |

## Usage Examples

### Pull Configuration from GitHub Repository

```bash
# Basic usage
openclaw skill run claw-migrate --repo hanxueyuan/lisa

# Specify branch and path
openclaw skill run claw-migrate \
  --repo hanxueyuan/lisa \
  --branch main \
  --path workspace/projects/workspace

# Pull skills only
openclaw skill run claw-migrate \
  --repo hanxueyuan/lisa \
  --type skills

# Preview mode
openclaw skill run claw-migrate \
  --repo hanxueyuan/lisa \
  --dry-run
```

## Notes

1. **GitHub Token**: Token required to access private repositories
2. **Backup**: Automatically creates backup to `.migrate-backup/<timestamp>/` before migration
3. **Memory Index**: May need to run `openclaw memory rebuild` after migration
4. **Sensitive Information**: .env file preserved if already exists locally

## Troubleshooting

| Error | Cause | Solution |
|------|------|---------|
| 404 Not Found | Repository name incorrect or no permission | Check repository name, confirm token permissions |
| 401 Unauthorized | Invalid token | Regenerate token |
| Rate limit exceeded | API request limit exceeded | Wait and retry, or use authenticated token |

## Related Files

- `src/index.js` - Main entry point
- `src/github.js` - GitHub API access
- `src/merger.js` - Merger engine
- `src/writer.js` - File writing and backup

## License

MIT License
