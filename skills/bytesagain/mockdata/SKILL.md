---
name: MockData
description: "Generate realistic fake data — names, emails, addresses — for testing and dev. Use when seeding databases, mocking API responses, creating sample records."
version: "2.0.0"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["mock","fake","data","generator","testing","development","faker","sample"]
categories: ["Developer Tools", "Utility"]
---

# MockData

Data operations toolkit for ingesting, transforming, querying, filtering, and managing data entries. Each command category maintains its own log, and the tool provides full export, search, profiling, and pipeline capabilities — all stored locally as timestamped log files.

## Commands

All commands are invoked via `mockdata <command> [args]`.

### Core Data Commands

Each of these commands works the same way: called without arguments it shows the 20 most recent entries from that category; called with arguments it saves a new timestamped entry.

| Command | Description |
|---------|-------------|
| `ingest <input>` | Log a data ingestion event (source, format, row count, etc.) |
| `transform <input>` | Log a data transformation step (normalization, type conversion, etc.) |
| `query <input>` | Log a query execution (SQL, API call, search parameters) |
| `filter <input>` | Log a filter operation (criteria applied, rows matched) |
| `aggregate <input>` | Log an aggregation result (sum, count, average, group-by) |
| `visualize <input>` | Log a visualization task (chart type, dimensions, output format) |
| `export <input>` | Log an export operation (destination, format, record count) |
| `sample <input>` | Log a sampling operation (sample size, method, seed) |
| `schema <input>` | Log a schema definition or change (fields, types, constraints) |
| `validate <input>` | Log a validation result (rules checked, pass/fail, errors found) |
| `pipeline <input>` | Log a pipeline execution (steps, duration, status) |
| `profile <input>` | Log a data profiling result (distributions, nulls, cardinality) |

### Utility Commands

| Command | Description |
|---------|-------------|
| `stats` | Summary statistics — entry counts per category, total entries, data size, earliest record |
| `export <fmt>` | Export all data in `json`, `csv`, or `txt` format (note: this is the utility export, separate from the logging `export` command) |
| `search <term>` | Search across all log files for a keyword (case-insensitive) |
| `recent` | Show the 20 most recent entries from the activity history |
| `status` | Health check — version, data directory, total entries, disk usage, last activity |
| `help` | Show the built-in help message |
| `version` | Print version string (`mockdata v2.0.0`) |

## Data Storage

- **Location:** `~/.local/share/mockdata/`
- **Format:** Each command category has its own `.log` file (e.g. `ingest.log`, `transform.log`, `pipeline.log`)
- **History:** All activity is also appended to `history.log` with timestamps
- **Exports:** Generated export files are saved to the same data directory as `export.json`, `export.csv`, or `export.txt`
- **Entry format:** Each log line is `YYYY-MM-DD HH:MM|<value>`

## Requirements

- Bash 4+
- Standard Unix utilities (`date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cat`)
- No external dependencies, no API keys, no network access needed

## When to Use

1. **Data pipeline documentation** — Log each step of a data pipeline (ingest → transform → validate → export) to maintain an audit trail of what was processed and when
2. **Schema tracking** — Record schema definitions and changes over time, making it easy to trace when fields were added, renamed, or removed
3. **ETL monitoring** — Use `ingest`, `transform`, `filter`, and `aggregate` to log ETL job details, then `search` or `export` to review execution history
4. **Data quality assurance** — Log validation results and profiling outputs to track data quality metrics across runs, and quickly find issues with `search`
5. **Experiment tracking** — Record query parameters, sampling methods, and aggregation results to document data experiments and reproduce analyses later

## Examples

```bash
# Log a data ingestion event
mockdata ingest "Loaded 50,000 rows from users.csv into staging table"

# View recent ingestion entries (no args = show last 20)
mockdata ingest

# Log a transformation step
mockdata transform "Normalized email addresses to lowercase, 12 duplicates removed"

# Log a validation result
mockdata validate "Schema check passed: all 15 required fields present, 0 nulls in PK"

# Log a pipeline run
mockdata pipeline "Daily ETL completed: ingest→transform→validate→load in 4m32s"

# Log a data profile
mockdata profile "users table: 125K rows, 3.2% null emails, age range 18-99"

# Search across all logs for a keyword
mockdata search "duplicates"

# Show summary statistics
mockdata stats

# Export everything to JSON
mockdata export json

# Export to CSV for spreadsheet analysis
mockdata export csv

# Check overall health status
mockdata status

# View 20 most recent activities
mockdata recent
```

## Output

All command output goes to stdout. Redirect to save:

```bash
mockdata stats > report.txt
mockdata export json   # saves to ~/.local/share/mockdata/export.json
```

## Configuration

No configuration file needed. Data directory is fixed at `~/.local/share/mockdata/`.

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
