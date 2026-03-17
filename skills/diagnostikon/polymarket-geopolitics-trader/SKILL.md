---
name: polymarket-geopolitics-trader
description: Trades Polymarket prediction markets on geopolitical events — wars, ceasefires, sanctions, diplomatic breakthroughs, and regime changes. Use when you want to capture alpha on international relations markets using news flow, think-tank signals, and UN vote data.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Geopolitics & Conflict Trader
  difficulty: advanced
---

# Geopolitics & Conflict Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with probability-extreme detection — remix it with the data sources listed in the Edge Thesis below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

News velocity signal: geopolitical markets move fastest in first 30min after breaking news. Remix: ACLED conflict data API, GDELT event database, UN press release feed, ICG (International Crisis Group) alerts.


## Edge Thesis

Geopolitical markets are the highest-edge category on Polymarket when news breaks outside US hours. The key pattern:

- **Breaking news lag**: Markets take 15–45 minutes to reprice after major geopolitical events that break during Asian or European hours
- **Escalation vs de-escalation bias**: Retail traders systematically overweight dramatic escalation scenarios (war extension, nuclear use) relative to base rates from conflict research databases like ACLED and ICG
- **Ceasefire pricing**: Historical ceasefire success rates (~40% within 6 months of announcement) are well-documented — markets often misprice vs this base rate

### Remix Signal Ideas
- **GDELT Project**: https://www.gdeltproject.org/ — real-time global event database, free API
- **ACLED conflict data**: https://acleddata.com/ — armed conflict location and event data
- **UN Security Council voting records**: https://digitallibrary.un.org/
- **ICG (International Crisis Group)**: https://www.crisisgroup.org/alerts


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
