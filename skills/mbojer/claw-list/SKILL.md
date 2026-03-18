---
name: todo
description: |
  Manage todo lists in PostgreSQL. Per-agent lists, optional categories, priorities, due dates.
  Triggers: "todo", "add task", "mark done", "what's due", "my tasks", "due soon", "overdue"
---

# ClawList — Todo Skill

Todo lists in PostgreSQL with per-agent ownership, categories, priorities, and due dates.

## Prerequisites

- Python 3.7+
- `psycopg2-binary` (`pip install psycopg2-binary`)
- PostgreSQL database (accessible from the agent host)

## First-Time Setup

1. Copy `.env.example` to `.env` and fill in your PostgreSQL credentials
2. Run `setup` command to create tables
3. Done — start adding todos

## Quick Reference

All operations via `scripts/todo_cli.py <command> [options]`.

| Command | Purpose |
|---|---|
| `setup` | Create DB tables (run once) |
| `add` | Add a todo (`--title`, `--list`, `--category`, `--priority`, `--due`) |
| `list` | List todos (`--agent`, `--list`, `--category`, `--priority`, `--completed`, `--all`, `--all-agents`) |
| `complete` / `uncomplete` | Toggle completion (`<id> --agent`) |
| `edit` | Update a todo (`<id> --title/--due/--priority/--category --agent`) |
| `transfer` | Move a todo to another agent (`<id> --from-agent X --to-agent Y --to-list Z`) |
| `delete` | Delete a todo (`<id> --agent`) |
| `archive` | Archive completed todos (`--agent`, optional `--list`) |
| `due-soon` | Todos due within N days (`--agent --days 7`) |
| `overdue` | Overdue todos (`--agent`) |
| `lists` | Show all lists for agent |
| `create-list` / `delete-list` | Manage lists |
| `categories` / `create-category` | Manage categories within a list |
| `migrate-check` | Scan workspace for existing task files (THELIST.md etc.) |
| `migrate` | Import from a task file (`--file --list --agent --action import-keep\|import-delete`) |

## Output Modes

- **Default**: Human-readable with status icons, priorities, due date indicators
- `--compact`: Single-line per todo, minimal tokens (e.g., `3 | Buy milk | high | due: 2026-03-20`)
- `--json`: JSON array for programmatic use

## Cross-Agent Access

Use `--request-from <agent>` to query another agent's list. All cross-agent access is logged.

## Detailed Reference

For full command syntax, examples, and schema: see [references/cli.md](references/cli.md)

## How to Use This Skill

### Agent Identity

The `--agent` flag identifies who owns the todos. Use your agent's identity name
(check your agent config or the `identity.name` field). Examples: `researcher`,
`jobhunter`, `assistant`. When unsure, ask the user which agent they want to use.

### Natural Language → Command Mapping

Parse user intent and map to commands:

| User says | Command |
|---|---|
| "Add todo: X" / "Remind me to X" | `add --title "X" --agent <name>` |
| "Add X to my Y list" | `add --title "X" --list "Y" --agent <name>` |
| "Show my todos" / "What's on my list?" | `list --agent <name>` |
| "Show all todos across agents" | `list --all-agents` |
| "Show my high priority tasks" | `list --agent <name> --priority high` |
| "What's due this week?" | `due-soon --agent <name> --days 7` |
| "Anything overdue?" | `overdue --agent <name>` |
| "Mark X as done" / "Complete X" | `complete <id> --agent <name>` |
| "Transfer X to agent Y" | `transfer <id> --from-agent <name> --to-agent Y` |
| "Delete X" / "Remove X" | `delete <id> --agent <name>` |
| "Change due date on X to Y" | `edit <id> --due "Y" --agent <name>` |
| "Archive completed items" | `archive --agent <name>` |

### Finding Todo IDs

Most commands need a todo ID. When the user refers to a todo by title (e.g., "mark
'buy milk' as done"), run `list` first to find the matching ID, then run the action.

### Responding to the User

- After `add`: confirm with the ID and any parsed details (priority, due date, list)
- After `list`: present the formatted output; for compact/json, summarize key items
- After `complete`/`delete`: confirm what was done
- For `overdue`/`due-soon`: highlight urgent items proactively

### First-Time Setup Flow

1. Run `setup` to create tables
2. Run `migrate-check` to scan for existing task files (THELIST.md, todo.txt, etc.)
3. If files found, ask the user what to do: import, keep, or both
4. Start normal operations

### Choosing Output Mode

- **Default** (no flags): for direct user display
- `--compact`: when listing many items or in token-constrained contexts
- `--json`: when another agent/script needs to parse results
