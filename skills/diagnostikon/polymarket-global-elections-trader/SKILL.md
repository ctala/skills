---
name: polymarket-global-elections-trader
description: Trades Polymarket prediction markets on elections, referendums, and democratic events worldwide — outside the US (which is heavily covered). Focuses on EU, Latin America, Asia, and Africa.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Global Elections & Democracy Trader
  difficulty: advanced
---

# Global Elections & Democracy Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with probability-extreme detection — remix it with the data sources listed in the Edge Thesis below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polling aggregator divergence from Polymarket: when poll average deviates > 8% from market price, trade the convergence.

## Edge Thesis

Non-US election markets are dramatically less liquid and less followed than US markets. European polling aggregators (Politico Europe, ElectionMapsUK, Wahlrecht.de) update daily but Polymarket prices on the same elections lag by 12–48h. The key signal: when a new poll shows a 3+ point swing vs the previous average, the market takes time to fully absorb it — especially for non-English-language elections where fewer Polymarket traders are monitoring closely.

### Remix Signal Ideas
- **Politico Europe Poll Tracker**: https://www.politico.eu/europe-poll-of-polls/ — Aggregated polling for all major EU elections
- **Wikipedia election polling pages**: https://en.wikipedia.org/ — Manually structured but comprehensive for any election worldwide
- **ElectoralCalendar.com**: https://www.electoralcalendar.com/ — Upcoming election dates globally — for discovery

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | See clawhub.json | Max USDC per trade |
| `SIMMER_MIN_VOLUME` | See clawhub.json | Min market volume filter |
| `SIMMER_MAX_SPREAD` | See clawhub.json | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | See clawhub.json | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | See clawhub.json | Max concurrent open positions |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
