---
name: miniqmt
description: miniQMT lightweight quantitative trading terminal — supports external Python via xtquant SDK for data and trading.
version: 1.0.0
homepage: http://dict.thinktrader.net/nativeApi/start_now.html
metadata: {"clawdbot":{"emoji":"🚀","requires":{"bins":["python3"]}}}
---

# miniQMT (迅投极简量化终端)

miniQMT is a lightweight quantitative trading terminal by 迅投科技, designed for external Python integration. It runs as a local Windows service that provides market data and trading capabilities via the [XtQuant](http://dict.thinktrader.net/nativeApi/start_now.html) Python SDK (`xtdata` + `xttrade`).

> ⚠️ **Requires broker account with miniQMT access**. Contact your securities broker to enable miniQMT. Many Chinese brokers (国金、华鑫、中泰、东方财富、国信、方正等) support it.

## What miniQMT is

- A **lightweight QMT client** that runs locally on Windows as a background service
- Provides **market data server** + **trading server** for external Python programs
- Your Python scripts connect via `xtquant` SDK (xtdata for data, xttrade for trading) over localhost TCP
- Supports: A-shares, ETFs, convertible bonds, futures, options, margin trading
- Some brokers provide **Level2 data** for free with miniQMT access

## Architecture

```
Python Script (any IDE: VS Code, PyCharm, Jupyter, etc.)
    ↓ xtquant SDK (pip install xtquant)
    ├── xtdata  ──TCP──→ miniQMT (market data server)
    └── xttrade ──TCP──→ miniQMT (trading server)
                              ↓
                    Broker Trading System (券商柜台)
```

## How to get miniQMT

1. Open a securities account with a broker that supports QMT
2. Apply for miniQMT access (some brokers require minimum assets, e.g. 50k-100k RMB)
3. Download and install the QMT client from your broker
4. Launch in miniQMT mode (极简模式) and log in

## Setup workflow

### 1. Start miniQMT

Launch the QMT client in miniQMT/极简模式 and log in. The miniQMT window is minimal — just a login screen.

### 2. Install xtquant

```bash
pip install xtquant
```

### 3. Connect from Python — Market data

```python
from xtquant import xtdata

# Connect to local miniQMT
xtdata.connect()

# Download historical data (must download before first access)
xtdata.download_history_data('000001.SZ', '1d', start_time='20240101', end_time='20240630')

# Get data (returns dict of DataFrames)
data = xtdata.get_market_data_ex(
    [], ['000001.SZ'], period='1d',
    start_time='20240101', end_time='20240630',
    dividend_type='front'  # 前复权
)
print(data['000001.SZ'].tail())
```

### 4. Connect from Python — Trading

```python
from xtquant import xtconstant
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount

# path must point to the userdata_mini folder inside QMT installation
path = r'D:\券商QMT\userdata_mini'
# session_id must be unique per strategy/script
session_id = 123456
xt_trader = XtQuantTrader(path, session_id)

# Register callback for real-time push notifications
class MyCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        print('Connection lost - need to reconnect')
    def on_stock_order(self, order):
        print(f'Order: {order.stock_code} status={order.order_status} msg={order.status_msg}')
    def on_stock_trade(self, trade):
        print(f'Trade: {trade.stock_code} {trade.traded_volume}@{trade.traded_price}')
    def on_order_error(self, order_error):
        print(f'Error: {order_error.error_msg}')

xt_trader.register_callback(MyCallback())
xt_trader.start()
connect_result = xt_trader.connect()  # 0 = success, non-0 = failure

account = StockAccount('your_account')
xt_trader.subscribe(account)  # Subscribe to receive push notifications

# Place order
order_id = xt_trader.order_stock(
    account, '000001.SZ', xtconstant.STOCK_BUY, 100,
    xtconstant.FIX_PRICE, 11.50, 'my_strategy', 'test_order'
)
# order_id > 0 = success, -1 = failure
```

---

## miniQMT vs full QMT

| Feature | miniQMT | QMT (full) |
|---|---|---|
| **Python** | External Python (any version) | Built-in Python (restricted version) |
| **IDE** | Any (VS Code, PyCharm, Jupyter, etc.) | Built-in editor only |
| **Libraries** | All pip packages (pandas, numpy, etc.) | Limited built-in libs |
| **UI** | Minimal (login only) | Full trading UI + charts |
| **Data** | Via xtdata API | Built-in + xtdata API |
| **Trading** | Via xttrade API | Built-in + xttrade API |
| **Resources** | Lightweight (~50MB memory) | Heavy (full GUI, ~500MB+) |
| **Debugging** | Full IDE debugging support | Limited |
| **Best for** | Automated strategies, external integration | Visual analysis + manual trading |
| **Connection** | One-time connect, no auto-reconnect | Persistent |

---

## Data capabilities (via xtdata)

| Category | Details |
|---|---|
| **K-line** | tick, 1m, 5m, 15m, 30m, 1h, 1d, 1w, 1mon — with dividend adjustment (前复权/后复权/等比) |
| **Tick** | Real-time tick data with 5-level bid/ask, volume, amount, transaction count |
| **Level2** | l2quote (实时快照), l2order (逐笔委托), l2transaction (逐笔成交), l2quoteaux (总买总卖), l2orderqueue (委托队列), l2thousand (千档盘口), fullspeedorderbook (全速20档) |
| **Financial** | Balance sheet, Income statement, Cash flow, Per-share indicators, Capital structure, Top 10 shareholders/float holders, Shareholder count |
| **Reference** | Trading calendar, holidays, sector/block lists, index constituents & weights, ex-rights data, contract info |
| **Real-time** | Single-stock subscription (`subscribe_quote`), full-market push (`subscribe_whole_quote`) |
| **Special** | Convertible bond info, IPO data, ETF creation/redemption lists, announcement/news, limit-up performance (涨停连板), snapshot indicators (量比/涨速), high-frequency IOPV |

### Data access pattern

```
download_history_data() → get_market_data_ex()  # Historical: download first, then get from cache
subscribe_quote()       → callback               # Real-time: subscribe, receive via callback
get_full_tick()                                   # Snapshot: get latest tick for all stocks
```

## Trading capabilities (via xttrade)

| Category | Operations |
|---|---|
| **Stock** | Buy/Sell (sync & async), limit/market/best price orders |
| **ETF** | Buy/Sell, creation/redemption |
| **Convertible bond** | Buy/Sell |
| **Futures** | Open/Close Long/Short (多开/多平/空开/空平) |
| **Options** | Buy/Sell Open/Close, covered open/close, exercise, lock/unlock |
| **Margin (融资融券)** | 融资买入, 融券卖出, 买券还券, 直接还券, 卖券还款, 直接还款, 专项融资/融券 |
| **IPO** | New share/bond subscription, query purchase limits |
| **Cancel** | Cancel by order_id or by broker sysid (sync & async) |
| **Query** | Asset, orders, trades, positions, futures position statistics |
| **Credit query** | Credit detail, liabilities, margin subjects, available short-sell, collateral |
| **Bank transfer** | Bank→Securities, Securities→Bank (sync & async) |
| **Smart algo** | VWAP and other algorithmic execution |
| **Securities lending** | Query sources, apply, manage contracts |

### Account types

```python
StockAccount('id')            # 普通股票
StockAccount('id', 'CREDIT')  # 信用/融资融券
StockAccount('id', 'FUTURE')  # 期货
```

### Key trading callbacks

| Callback | When triggered |
|---|---|
| `on_stock_order(order)` | Order status changes (submitted, partially filled, filled, cancelled, rejected) |
| `on_stock_trade(trade)` | Trade executed |
| `on_stock_position(position)` | Position changes |
| `on_stock_asset(asset)` | Asset/cash changes |
| `on_order_error(error)` | Order placement failed |
| `on_cancel_error(error)` | Order cancellation failed |
| `on_disconnected()` | Connection to miniQMT lost |

### Order status codes

| Value | Status |
|---|---|
| 48 | 未报 (Not submitted) |
| 50 | 已报 (Submitted) |
| 54 | 已撤 (Cancelled) |
| 55 | 部成 (Partially filled) |
| 56 | 已成 (Filled) |
| 57 | 废单 (Rejected) |

---

## Common broker paths

```python
# 国金证券
path = r'D:\国金证券QMT交易端\userdata_mini'
# 华鑫证券
path = r'D:\华鑫证券\userdata_mini'
# 中泰证券
path = r'D:\中泰证券\userdata_mini'
# 东方财富
path = r'D:\东方财富证券QMT交易端\userdata_mini'
```

## Stock code format

| Market | Example |
|---|---|
| Shanghai A-shares | `600000.SH` |
| Shenzhen A-shares | `000001.SZ` |
| Beijing (BSE) | `430047.BJ` |
| Index | `000001.SH` (上证指数), `399001.SZ` (深证成指) |
| CFFEX Futures | `IF2401.IF` |
| SHFE Futures | `ag2407.SF` |
| Options | `10004358.SHO` |
| ETF | `510300.SH` |
| Convertible Bond | `113050.SH` |

---

## Complete example: Data + trading strategy

```python
from xtquant import xtdata, xtconstant
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount

# === Callback ===
class MyCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        print('Disconnected')
    def on_stock_trade(self, trade):
        print(f'成交: {trade.stock_code} {trade.traded_volume}@{trade.traded_price}')
    def on_order_error(self, order_error):
        print(f'错误: {order_error.error_msg}')

# === 1. Connect data ===
xtdata.connect()

# === 2. Download and get data ===
stock = '000001.SZ'
xtdata.download_history_data(stock, '1d', start_time='20240101', end_time='20240630')
data = xtdata.get_market_data_ex(
    [], [stock], period='1d',
    start_time='20240101', end_time='20240630',
    dividend_type='front'
)
df = data[stock]

# === 3. Simple MA crossover signal ===
df['ma5'] = df['close'].rolling(5).mean()
df['ma20'] = df['close'].rolling(20).mean()
latest = df.iloc[-1]
prev = df.iloc[-2]

# === 4. Connect trader ===
path = r'D:\券商QMT\userdata_mini'
xt_trader = XtQuantTrader(path, 123456)
xt_trader.register_callback(MyCallback())
xt_trader.start()
if xt_trader.connect() != 0:
    print('Connection failed!')
    exit()

account = StockAccount('your_account')
xt_trader.subscribe(account)

# === 5. Execute signal ===
if prev['ma5'] <= prev['ma20'] and latest['ma5'] > latest['ma20']:
    order_id = xt_trader.order_stock(
        account, stock, xtconstant.STOCK_BUY, 100,
        xtconstant.LATEST_PRICE, 0, 'ma_cross', 'golden_cross'
    )
    print(f'Golden cross — buy {stock}, order_id={order_id}')
elif prev['ma5'] >= prev['ma20'] and latest['ma5'] < latest['ma20']:
    order_id = xt_trader.order_stock(
        account, stock, xtconstant.STOCK_SELL, 100,
        xtconstant.LATEST_PRICE, 0, 'ma_cross', 'death_cross'
    )
    print(f'Death cross — sell {stock}, order_id={order_id}')

# === 6. Check results ===
asset = xt_trader.query_stock_asset(account)
print(f'Cash: {asset.cash}, Total: {asset.total_asset}')

positions = xt_trader.query_stock_positions(account)
for pos in positions:
    print(f'{pos.stock_code}: {pos.volume} shares, available={pos.can_use_volume}, cost={pos.open_price}')
```

## Complete example: Real-time monitoring with subscription

```python
from xtquant import xtdata
import threading

def on_tick(datas):
    for code, tick in datas.items():
        print(f'{code}: price={tick["lastPrice"]}, vol={tick["volume"]}')

# Connect and subscribe
xtdata.connect()

# Run subscription in a separate thread (xtdata.run() blocks)
def run_data():
    xtdata.subscribe_quote('000001.SZ', period='tick', callback=on_tick)
    xtdata.subscribe_quote('600000.SH', period='tick', callback=on_tick)
    xtdata.run()

t = threading.Thread(target=run_data, daemon=True)
t.start()

# Main thread can do trading or other work
# ...
```

## Tips

- miniQMT runs on **Windows only** — Python scripts can run on same or different machine if TCP is accessible.
- Keep miniQMT **logged in** while your Python script is running.
- `connect()` is a **one-time connection** — no auto-reconnect on disconnect; implement reconnection logic.
- `session_id` must be **unique per strategy** — different Python scripts need different session IDs.
- Use `xtdata.run()` in a **separate thread** for real-time subscriptions while doing trading in main thread.
- Data is **cached locally** after download — subsequent reads are instant.
- In push callbacks (`on_stock_order`, etc.), prefer **async query methods** (e.g. `query_stock_orders_async`) to avoid deadlocks. Or enable `set_relaxed_response_order_enabled(True)`.
- Some brokers offer miniQMT with **free Level2 data** — check with your broker.
- Docs: http://dict.thinktrader.net/nativeApi/start_now.html
