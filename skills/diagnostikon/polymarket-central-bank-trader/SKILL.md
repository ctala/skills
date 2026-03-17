---
name: polymarket-central-bank-trader
description: Trades Polymarket prediction markets on central bank decisions, interest rates, inflation prints, and Fed/ECB/Riksbank policy moves.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Central Bank & Monetary Policy Trader
  difficulty: advanced
---

# Central Bank & Monetary Policy Trader

Central bank decisions move prediction markets faster than almost any other category — but Polymarket consistently lags interest rate futures by 15–45 minutes after FOMC statements. This skill exploits that lag.

Out of the box it scans for monetary policy markets and trades probability extremes. The real edge comes from wiring in the CME FedWatch API: when futures odds diverge >10% from the Polymarket YES price, the futures market has an essentially perfect track record of being right. The skill is structured so you can drop that signal into `compute_signal()` in about 20 lines.

## Strategy Overview

Yield curve inversion depth + CME FedWatch futures divergence from market probability.

## Edge Thesis

Prediction markets are slower than interest rate futures to reprice after FOMC statements. The CME FedWatch tool shows real-money futures probabilities that systematically lead Polymarket by 15–45 minutes after Fed speak. Key edge pattern: compare FedWatch probability for next meeting vs Polymarket YES price — when divergence > 10%, the futures market is almost always right.

### Remix Signal Ideas
- **CME FedWatch Tool API**: https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html — Real-money futures odds for each FOMC meeting outcome
- **FRED API (St. Louis Fed)**: https://fred.stlouisfed.org/docs/api/fred/ — CPI, PCE, unemployment, yield spreads — all free
- **BLS CPI release calendar**: https://www.bls.gov/schedule/news_release/cpi.htm — Trade the 15-minute window before/after CPI prints

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
