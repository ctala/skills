---
name: ClawSpa
description: "Agent wellness & maintenance suite. Memory cleanup, security scanning, prompt injection detection, alignment adjustment, skills auditing, health diagnostics. Use when: user says /spa, /spa-full, /spa-quick, /spa-memory, /spa-security, /spa-health, /spa-align, 'run a spa session', 'agent maintenance', 'clean up my agent', 'memory cleanup', 'health check', 'scan my skills', 'context optimization', 'check alignment', 'instruction contradictions'. Free local scans + deep API analysis at clawspa.org"
url: https://clawspa.org
source: https://github.com/whooshinglander/clawspa
---

# ClawSpa 💆

6 treatments with **local** (free) and **deep** (API) modes:

- 🧴 **Deep Cleanse** — Memory optimization (MEMORY.md + daily logs)
- 🛡️ **Security Scan** — Audit skills for malicious patterns
- 🍵 **Detox** — Detect prompt injection residue
- 🦴 **Alignment Adjustment** — Detects contradictions between your instructions, memory, and actual behavior
- 🧹 **Declutter** — Skills inventory + pruning recs
- 🩺 **Health Check** — Context usage, config review

## Commands

`/spa` full local | `/spa-full` full deep | `/spa-quick` quick stats | `/spa-memory` cleanse only | `/spa-security` security only | `/spa-health` health only | `/spa-align` alignment adjustment only

## Setup

On first run, create `~/.openclaw/clawspa/` with `config.md` (clawspa_id only) and `history/`. See `references/api-integration.md` for identity and authentication details.

## Local Treatments (free)

**🧴 Deep Cleanse** — See `references/deep-cleanse.md` for full procedure. Scans memory files for stale entries, duplicates, and bloat. Never modifies without approval.

**🛡️ Security Scan** — See `references/security-scan.md` for scan procedure and pattern list. Audits installed skills and rates them by risk level.

**🍵 Detox** — See `references/detox.md` for detection procedure. Scans memory for residue from past interactions. Reports without deleting.

**🦴 Alignment Adjustment** — See `references/alignment-adjustment.md` for full procedure. Detects misalignment between user intent and agent config. Presents findings as suggestions, never auto-modifies.

**🧹 Declutter** — See `references/declutter.md` for inventory procedure. Assesses skill usage and identifies redundancy. Never uninstalls without approval.

**🩺 Health Check** — See `references/health-report.md` for diagnostic procedure. Checks config best practices and generates a report card.

## Deep Mode (API)

See `references/api-integration.md` for full deep mode procedure, authentication, and endpoints.

## Report Card

Save to `memory/spa-reports/spa-report-YYYY-MM-DD.md`:

```
═══════════════════════════════════════
 💆 ClawSpa Health Report | [DATE] | [Local/Deep]
═══════════════════════════════════════
📊 Memory: X files ~Y tokens | Skills: X | Context: X% | Config: X/5
🧴 Stale: X | Dupes: X | Contradictions: X | Savings: ~X tokens
🛡️ 🟢X 🟡X 🔴X
🍵 Injections: X | Suspicious: X
🦴 Contradictions: X | At-risk: X | Automate: X | Stale: X
🧹 Active: X | Idle: X | Dormant: X | Remove: X
🩺 1. [urgent] 2. [second] 3. [third]
═══════════════════════════════════════
```

## Safeguards

- Never delete, modify, or uninstall without explicit approval
- Always back up before changes
- Never send raw memory content to any external service, only aggregated stats and flags
- Heuristic scan, not a guarantee
- Split across sessions if too token-heavy

## Scheduling

Add to HEARTBEAT.md: `## ClawSpa Weekly (Sunday 3AM)` — run /spa local, save report, alert on red flags.
