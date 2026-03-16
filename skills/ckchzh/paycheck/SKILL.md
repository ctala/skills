---
name: paycheck
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [paycheck, tool, utility]
---

# Paycheck

Paycheck calculator — salary breakdown, tax estimates, deductions, and net pay.

## Commands

| Command | Description |
|---------|-------------|
| `paycheck help` | Show usage info |
| `paycheck run` | Run main task |
| `paycheck status` | Check state |
| `paycheck list` | List items |
| `paycheck add <item>` | Add item |
| `paycheck export <fmt>` | Export data |

## Usage

```bash
paycheck help
paycheck run
paycheck status
```

## Examples

```bash
paycheck help
paycheck run
paycheck export json
```

## Output

Results go to stdout. Save with `paycheck run > output.txt`.

## Configuration

Set `PAYCHECK_DIR` to change data directory. Default: `~/.local/share/paycheck/`

---
*Powered by BytesAgain | bytesagain.com*
*Feedback & Feature Requests: https://bytesagain.com/feedback*
