---
name: clawclau
description: 'Async Claude Code task dispatcher via tmux. Use when ACP protocol fails or hangs. Spawns Claude Code in isolated tmux sessions, monitors completion, and retrieves results asynchronously. NOT for: tasks that fit in one exec call, interactive Claude Code sessions, or environments without tmux/claude/jq.'
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["tmux", "jq", "claude"] },
        "install":
          [
            { "id": "tmux", "kind": "brew", "package": "tmux" },
            { "id": "jq", "kind": "brew", "package": "jq" },
            {
              "id": "claude",
              "kind": "npm",
              "package": "@anthropic-ai/claude-code",
              "bins": ["claude"],
            },
          ],
      },
  }
---

# ClawClau — Async Claude Code via tmux

Dispatch Claude Code tasks asynchronously through tmux. Bypasses ACP protocol deadlocks.

## When to Use

Use ClawClau instead of `sessions_spawn` with `runtime: "acp"` when:
- ACP initialization hangs (common with custom API proxies)
- You need non-blocking task dispatch
- You want to check results later without waiting

Do NOT use for:
- Simple one-liner commands (use `exec` directly)
- Tasks requiring real-time streaming output
- Environments without tmux, jq, or Claude Code

## First-Time Setup

```bash
# Set up the working directory
export CLAWCLAU_HOME="$HOME/.clawclau"
mkdir -p "$CLAWCLAU_HOME/logs"
echo '[]' > "$CLAWCLAU_HOME/active-tasks.json"
```

Add to shell profile for persistence:
```bash
echo 'export CLAWCLAU_HOME="$HOME/.clawclau"' >> ~/.zshrc
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAWCLAU_HOME` | `~/.openclaw/workspace/.clawdbot` | Base directory for registry and logs |
| `CLAWCLAU_SHELL` | `bash` | Shell for launching Claude Code in tmux |

## Scripts

All scripts are in `scripts/` relative to this skill directory. Set `CLAWCLAU_HOME` before calling.

### Spawn a task

```bash
CLAWCLAU_HOME="$HOME/.clawclau" ./scripts/claude-spawn.sh <task-id> "<prompt>" [workdir] [timeout-seconds]
```

- `<task-id>`: alphanumeric + dash/underscore only
- `<prompt>`: the task for Claude Code
- `[workdir]`: defaults to current directory
- `[timeout-seconds]`: defaults to 600 (10 min)

Example:
```bash
CLAWCLAU_HOME="$HOME/.clawclau" ./scripts/claude-spawn.sh "refactor-auth" \
  "Refactor src/auth.ts to use JWT tokens instead of sessions" \
  "$HOME/my-project" 300
```

### Check task status

```bash
CLAWCLAU_HOME="$HOME/.clawclau" ./scripts/claude-check.sh [task-id]
```

Without argument: lists all tasks. With argument: shows details + last output.

### Get results

```bash
CLAWCLAU_HOME="$HOME/.clawclau" ./scripts/claude-result.sh <task-id>
```

### Monitor (auto-detect completion)

```bash
CLAWCLAU_HOME="$HOME/.clawclau" ./scripts/claude-monitor.sh
```

Set up cron for automatic monitoring:
```bash
# crontab -e
*/2 * * * * CLAWCLAU_HOME="$HOME/.clawclau" /path/to/skills/clawclau/scripts/claude-monitor.sh
```

### Kill a task

```bash
CLAWCLAU_HOME="$HOME/.clawclau" ./scripts/claude-kill.sh <task-id>
```

### Steer a running task

```bash
CLAWCLAU_HOME="$HOME/.clawclau" ./scripts/claude-steer.sh <task-id> "<message>"
```

Note: steering only works with interactive Claude Code sessions, not `claude -p`.

## Task Lifecycle

```
running → done     (tmux ended, log has content)
running → failed   (tmux ended, log empty)
running → timeout  (exceeded timeout)
running → killed   (manually terminated)
```

## Security

`claude-spawn.sh` uses `--dangerously-skip-permissions`. Only use in trusted environments.
