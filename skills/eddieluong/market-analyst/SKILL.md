---
name: global-market-analyst
description: "Phân tích và tư vấn đầu tư tài sản toàn cầu — cổ phiếu VN & US, forex, vàng, dầu, crypto, ETF, DCA. Kết hợp phân tích kỹ thuật real-time (RSI, MACD, EMA, Bollinger Bands) từ TradingView với phân tích cơ bản (P/E, ROE, Sharpe, CAGR, định giá ngành). Use when: (1) user hỏi về giá cổ phiếu VN hoặc toàn cầu, (2) user muốn biết nên mua tài sản nào, (3) user hỏi về danh mục đầu tư, (4) user muốn tính DCA tích lũy hàng tháng, (5) user hỏi nên đầu tư bao nhiêu/tháng, (6) user muốn estimate lợi nhuận theo thời gian, (7) user muốn so sánh các loại tài sản toàn cầu, (8) user hỏi về vàng, crypto, S&P 500, ETF, (9) user hỏi về lướt sóng, swing trading, scalping, day trading VN, (10) user hỏi về forex EUR/USD, USD/JPY, (11) user hỏi về commodities dầu WTI, bạc, (12) user hỏi về US stocks AAPL, NVDA, TSLA, MSFT."
---

# Global Market Analyst

Phân tích tài sản toàn cầu — VN stocks, US equities, Forex, Commodities, Crypto, ETF — kỹ thuật real-time + cơ bản + định giá + estimate sinh lời.

## ⚠️ Nguyên tắc quan trọng nhất

**CAGR lịch sử ≠ kỳ vọng từ giá hiện tại.**
Luôn hỏi: *"Nếu mua HÔM NAY ở giá này, P/E là bao nhiêu? Còn rẻ không?"*

Ví dụ: MCH CAGR 73%/năm từ đáy 30k → nhưng ở giá 161k hiện tại P/E ~37x là **đắt**.
Sharpe 2.19 là lịch sử từ vùng giá thấp — không apply cho người mua hôm nay.

---

## Step 0: Hiểu rõ yêu cầu & Check Macro

Trước khi phân tích bất kỳ tài sản nào, luôn check:

### 🇻🇳 Macro Việt Nam
**Macro context hiện tại (cập nhật 23/03/2026):**
- **🔴 VN-Index: ~1,604** — giảm 14% trong tháng, khối ngoại bán ròng -27,591 tỷ YTD
- **🟢 FTSE upgrade VN** → hiệu lực 21/09/2026 → catalyst lớn nhất
- SBV rate: Đang giữ, follow FED
- GDP target 2026: 6.5-7%

### 🇺🇸 Macro Mỹ
- **FED rate: 3.5-3.75%** (giữ nguyên 18/3/2026, hawkish — chỉ 1 lần cắt dự kiến 2026)
- **PCE inflation: 2.7%** (nâng từ 2.4%)
- **Unemployment:** ~4.0% (ổn định)
- **S&P 500:** Đang correction ~5-8% từ ATH, tech dẫn dắt
- **US 10Y yield:** ~4.2-4.4%

### 🌍 Macro Toàn cầu
- **🔴 Iran War đang diễn ra** — dầu WTI $95-99, đe dọa Eo Hormuz
- **Vàng XAUUSD:** ~$4,362 (điều chỉnh -15% từ ATH $5,608)
- **DXY (USD Index):** ~103-105
- **BNB:** Áp lực risk-off, ecosystem vẫn mạnh (TVL $6.7B, #3 globally)
- **ECB rate:** ~3.0%, đang cắt dần
- **BOJ rate:** ~0.5%, vừa tăng từ 0.25%

**Tác động lên danh mục:**
- 🟢 Mua tích lũy: MBB (P/E 6.5x), Vàng, S&P 500 ETF (VOO)
- 🟢 DCA: FPT (P/E 13-14x, rẻ bất thường nhưng dưới EMA200)
- ⏳ Hold: BNB (chờ FED cắt), TCB, AAPL, MSFT
- 🔴 Tránh: VCB (P/E đắt), BĐS (lãi suất tăng), crypto mới, meme coins
- 🟢 Mua mới: GAS/PVS (hưởng lợi dầu cao), Energy ETF (XLE)

Xem chi tiết: `references/macro-update-2026-03.md`, `references/crypto-analysis.md`, `references/gold-analysis.md`.

---

Xác định:
- **Asset class**: Cổ phiếu VN? US stocks? Forex? Vàng? Crypto? ETF?
- **Mục tiêu**: Tìm cơ hội mới? Phân tích mã cụ thể? Estimate lợi nhuận? Scan thị trường?
- **Thời gian nắm giữ**: Ngắn hạn (< 3 tháng), trung hạn (3-12 tháng), dài hạn (> 1 năm)
- **Vốn**: Để estimate portfolio allocation và risk
- **Khẩu vị rủi ro**: Bảo thủ / Cân bằng / Tích cực

---

## Step 1: Real-time Data (TradingView Scanner)

TradingView scanner hoạt động **KHÔNG cần auth**:

### 🇻🇳 VN Stocks
```bash
# Scan toàn HOSE tìm oversold
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 40 --exchange HOSE

# Phân tích kỹ thuật sâu 1 mã VN
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/analyze_stock.py FPT HOSE
```

### 🇺🇸 US Stocks
```bash
# Scan NASDAQ oversold (large-cap > $2B)
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 40 --exchange NASDAQ

# Scan NYSE
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 35 --exchange NYSE
```

### 🌍 Global Markets (Crypto, Forex, Commodities)
```bash
# Scan US equities (large-cap > $10B)
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market us --rsi 40

# Scan crypto
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market crypto --rsi 35

# Scan forex major pairs
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market forex

# Scan commodities (gold, oil, silver)
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market commodities

# Scan tất cả markets
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_global.py --market all --rsi 40
```

**Fetch thủ công nhiều mã (bất kỳ market):**
```python
import urllib.request, json

# VN stocks
payload = {
    "symbols": {"tickers": ["HOSE:MBB","HOSE:TCB","HOSE:FPT"]},
    "columns": ["name","close","change","volume","RSI","EMA20","EMA50","EMA200",
                "MACD.macd","MACD.signal","BB.upper","BB.lower",
                "price_52_week_high","price_52_week_low","Stoch.K","Stoch.D"]
}
req = urllib.request.Request(
    "https://scanner.tradingview.com/vietnam/scan",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    method="POST"
)

# US stocks → "https://scanner.tradingview.com/america/scan"
# Crypto → "https://scanner.tradingview.com/crypto/scan"
# Forex → "https://scanner.tradingview.com/forex/scan"
# Commodities → "https://scanner.tradingview.com/cfd/scan"
```

---

## Step 2: Phân tích Kỹ thuật (Áp dụng cho TẤT CẢ asset classes)

Đọc từng chỉ báo theo thứ tự ưu tiên:

### 1. EMA200 — Kiểm tra TRƯỚC TIÊN
- `close > EMA200` ✅ → Long-term uptrend còn nguyên → **có thể xem xét mua**
- `close < EMA200` ❌ → Downtrend dài hạn → **thận trọng, chỉ mua nếu có catalyst đặc biệt**

**⚠️ Không mua asset RSI oversold nhưng dưới EMA200** (trừ khi có catalyst rõ ràng)

### 2. RSI(14)
| RSI | Tín hiệu | Hành động |
|---|---|---|
| < 30 | 🟢🟢 Oversold cực mạnh | Xem xét mua mạnh nếu trên EMA200 |
| 30–40 | 🟢 Oversold | DCA nếu trên EMA200 |
| 40–60 | 🟡 Neutral | Giữ / chờ |
| 60–70 | 🔴 Cận overbought | Không thêm vị thế |
| > 70 | 🔴🔴 Overbought | Cân nhắc chốt lời |

### 3. MACD
- `macd > signal` → 🟢 Bullish momentum
- `macd < signal` → 🔴 Bearish momentum
- MACD vừa cắt lên signal ở vùng âm → **tín hiệu mua mạnh**

### 4. Bollinger Bands
- `close ≤ BB.lower` → Gần đáy dải → tiềm năng bounce
- BB co lại (squeeze) → sắp biến động mạnh, chờ breakout

### 5. Stochastic K/D
- K < 20: Oversold | K > 80: Overbought
- K cắt lên D ở vùng < 20 → mua signal

### 6. 52W Position
```
pos52 = (close - low52w) / (high52w - low52w) × 100
```
- < 20%: Gần đáy 52W — vùng value tốt
- > 80%: Gần đỉnh 52W — momentum cao nhưng rủi ro

### 🎯 Buy Zone Score (tổng hợp)
```python
score = 0
if rsi < 30: score += 3
elif rsi < 40: score += 2
if close > ema200: score += 2
if pe_discount > 20%: score += 3  # P/E < Fair P/E - 20%
elif pe_discount > 0: score += 2
if pos52 < 20: score += 2
elif pos52 < 40: score += 1
if close <= bb_lower * 1.02: score += 2
if macd > macd_signal: score += 1
# Max: 15 điểm
# ≥ 10: Mua mạnh | 7-9: DCA | 4-6: Theo dõi | < 4: Bỏ qua
```

---

## Step 3: Phân tích Định giá — BẮT BUỘC (Stocks & ETF)

**Không đưa ra khuyến nghị MUA nếu chưa check định giá.**

### P/E Analysis
```
Upside = (Fair P/E - Current P/E) / Fair P/E × 100%
```

| Upside | Đánh giá |
|---|---|
| > 25% | 🟢 Rất rẻ — mua |
| 10–25% | 🟡 Hơi rẻ — tích lũy |
| 0–10% | 🟡 Hợp lý — OK |
| < 0% | 🔴 Đắt — chờ điều chỉnh |
| < -15% | 🔴🔴 Đắt nhiều — tránh |

**Fair P/E theo ngành VN:**
- Ngân hàng: 10–12x | Công nghệ: 20–25x | Thép: 8–12x
- Tiêu dùng: 15–22x | BĐS: 12–18x | Dầu khí: 10–14x

**Fair P/E theo ngành US:** (Xem chi tiết `references/us-equities.md`)
- Tech (mega): 25–30x | Tech (growth): 30–45x | Healthcare: 16–20x
- Financials (banks): 10–13x | Energy: 10–14x | Consumer Disc.: 22–28x
- **US dùng Forward P/E** nhiều hơn Trailing P/E
- **PEG Ratio** = P/E / EPS Growth Rate → PEG < 1.0 = rẻ tương đối

Xem chi tiết trong `references/sector-fundamentals.md` (VN) và `references/us-equities.md` (US)

### Các chỉ số cơ bản khác
- **ROE > 15%**: tốt | **> 20%**: xuất sắc
- **D/E < 1.0**: ít nợ (ngân hàng ngoại lệ)
- **FCF dương**: công ty sinh tiền thực
- **EPS CAGR**: driver chính của giá dài hạn

Xem framework đầy đủ trong `references/financial-analysis-knowledge.md`

---

## Step 4: Phân tích Ngành & Catalyst

### 🇻🇳 VN Sectors
Reference `references/sector-fundamentals.md` và `references/sector-update-2026.md`.

**Catalyst VN 2026-2028:**
- Nâng hạng thị trường FTSE/MSCI → vốn ngoại đổ vào
- Lãi suất giảm → P/E hợp lý cao hơn, BĐS phục hồi
- Đầu tư công tăng → thép, vật liệu xây dựng
- GDP 6-7%/năm → ngân hàng, tiêu dùng

### 🇺🇸 US Sectors
Reference `references/us-equities.md`.

**Catalyst US 2026-2028:**
- AI revolution → NVDA, MSFT, GOOG, META, AMZN
- FED rate cuts → growth stocks rally, REITs phục hồi
- Infrastructure spending → industrials, materials
- GLP-1 drugs → LLY, NVO, healthcare sector

Luôn trả lời:
1. **Ngành đang ở đâu trong chu kỳ?** (tăng trưởng / đỉnh / suy thoái / đáy)
2. **Catalyst 1-3 năm tới là gì?**
3. **Rủi ro chính là gì?**

---

## Step 5: US Equities Analysis

Khi user hỏi về cổ phiếu Mỹ (AAPL, NVDA, TSLA, MSFT, GOOG, META, AMZN, v.v.):

### Workflow:
1. **Scan data:** `scan_global.py --market us` hoặc fetch trực tiếp
2. **Technical:** Áp dụng Step 2 (EMA200, RSI, MACD, BB)
3. **Valuation:** Forward P/E vs sector average, PEG ratio
4. **Earnings:** Check earnings calendar — KHÔNG mua ngay trước earnings
5. **Macro:** FED rate path, US 10Y yield, DXY ảnh hưởng

### Key Metrics cho US Stocks:
- **Forward P/E** (quan trọng hơn trailing)
- **PEG Ratio** (< 1.0 = rẻ, 1.0-2.0 = hợp lý, > 2.0 = đắt)
- **FCF Yield** (FCF / Market Cap — > 5% = tốt)
- **Revenue Growth** (YoY — quan trọng cho tech)
- **Gross Margin** (>60% cho software, >40% cho hardware)

### Đặc thù US vs VN:
- US trade pre/after-market → gap risk cao hơn
- Earnings season 4 lần/năm → stock có thể ±20% trong 1 ngày
- Options market rất active → đọc implied volatility
- Buyback programs → hỗ trợ giá (AAPL buyback $100B+/năm)
- US dùng **fractional shares** → mua $10 NVDA được

Xem chi tiết: `references/us-equities.md`

---

## Step 6: Forex Analysis

Khi user hỏi về forex (EUR/USD, USD/JPY, GBP/USD, v.v.):

### Workflow:
1. **Scan:** `scan_global.py --market forex`
2. **Macro check:** Interest rate differential giữa 2 đồng tiền
3. **Technical:** EMA, RSI, Fibonacci, pivot points
4. **Session timing:** Asian/European/US session
5. **Risk:** Swap rates, leverage management

### Key Pairs & Factors:
| Cặp | Nhân tố chính |
|-----|--------------|
| EUR/USD | FED vs ECB rates, trade balance EU-US |
| USD/JPY | FED vs BOJ, risk sentiment, carry trade |
| GBP/USD | BOE rate, Brexit effects, UK economy |
| AUD/USD | RBA rate, commodities (iron ore), China demand |
| USD/VND | SBV policy, trade balance VN, FDI flows |

### Session Times (giờ VN):
- **London-NY overlap (19:30-23:00 VN)** = best time to trade
- **Asian session (06:00-14:00)** = range-bound, phù hợp range trading
- **London open (14:00-17:00)** = breakout Asian range

### Risk Management Forex:
- **2% rule:** Max risk 2% account per trade
- **Leverage max 1:30** cho beginner
- **ATR-based stop loss:** SL = 1.5-2x ATR(14)

Xem chi tiết: `references/forex-guide.md`

---

## Step 7: Commodities Analysis (Vàng, Dầu, Bạc)

Khi user hỏi về vàng (XAUUSD), dầu (WTI/Brent), bạc (XAGUSD):

### Workflow:
1. **Scan:** `scan_global.py --market commodities`
2. **Macro:** Real rates (US 10Y - CPI), DXY, geopolitics
3. **Technical:** EMA200, RSI, Fibonacci retracement
4. **Specific factors:** (xem bên dưới)

### 🥇 Vàng (XAUUSD):
- **Bullish khi:** Real rates giảm, DXY yếu, risk-off, NHTW mua vàng
- **Bearish khi:** Real rates tăng, DXY mạnh, risk-on
- **Key levels:** Round numbers ($4000, $4500, $5000)
- **Seasonal:** Thường mạnh Q1 và Q4
- Xem chi tiết: `references/gold-analysis.md`

### 🛢️ Dầu (WTI / Brent):
- **Bullish khi:** OPEC+ cắt sản lượng, geopolitics (Iran/ME), demand tăng
- **Bearish khi:** Recession fears, OPEC+ tăng sản lượng, US shale tăng
- **Key data:** EIA Weekly Inventory, Baker Hughes Rig Count
- **Correlation:** USD/CAD (inverse), energy stocks (positive)

### 🥈 Bạc (XAGUSD):
- **Dual nature:** Industrial metal + precious metal
- **Gold/Silver Ratio:** > 80 = bạc rẻ tương đối, < 60 = bạc đắt
- **Volatile hơn vàng:** Beta ~1.5-2x so với gold

---

## Step 8: Global ETF Analysis

Khi user hỏi về ETF (VOO, QQQ, VNM, v.v.):

### Workflow:
1. **Identify need:** Core portfolio? Sector bet? Country exposure?
2. **Compare:** Expense ratio, tracking error, AUM, liquidity
3. **Technical:** Áp dụng EMA200, RSI cho ETF chart
4. **DCA plan:** Phân bổ theo risk profile

### Quick ETF Recommendations:
| Mục đích | ETF | Expense | Ghi chú |
|----------|-----|---------|---------|
| Core US | VOO / IVV | 0.03% | S&P 500, nền tảng portfolio |
| Tech/Growth | QQQ / QQQM | 0.15-0.20% | NASDAQ 100, AI exposure |
| VN Exposure | VNM | 0.66% | VanEck Vietnam ETF |
| Emerging Markets | VWO / IEMG | 0.08-0.09% | Broad EM |
| Bonds | BND / AGG | 0.03% | US total bond |
| Gold | GLD / IAU | 0.25-0.40% | Physical gold ETF |
| All-World | VT | 0.07% | Toàn cầu, lazy portfolio |

### DCA Portfolios:

**Conservative:** VOO 40% + BND 30% + VWO 15% + GLD 15%
**Balanced:** VOO 45% + QQQ 20% + VWO 15% + BND 10% + GLD 10%
**Aggressive:** QQQ 35% + VOO 25% + VWO/VNM 20% + ARKK/SOXX 10% + GLD 10%

Xem chi tiết: `references/global-etf.md`

---

## Step 9: Estimate Sinh lời

```bash
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/estimate_returns.py [TICKER] [--capital X] [--years N]
```

Script tính từ historical data:
- **CAGR** 3Y/5Y (tỷ lệ tăng trưởng kép)
- **Volatility** hàng năm (độ biến động)
- **Max Drawdown** (mức giảm tối đa từ đỉnh)
- **Sharpe Ratio** (return/risk)
- **3 kịch bản** Bear/Base/Bull × 6M/1Y/3Y/5Y

**⚠️ Luôn nhắc user:**
- CAGR lịch sử là từ giá VÀO của quá khứ, không phải từ giá hiện tại
- Nếu P/E hiện tại đã cao → estimate thực tế thấp hơn CAGR lịch sử
- So sánh với: gửi ngân hàng 5.5%/năm (VN), US Treasury 4.5%/năm, VN-Index ~11%/năm, S&P 500 ~12%/năm

Xem phương pháp đầy đủ trong `references/return-estimation.md`

---

## Step 10: Portfolio Allocation (Global)

Khi user hỏi nên phân bổ vốn như thế nào:

### Sizing theo Sharpe
| Sharpe | Tỷ trọng tối đa |
|---|---|
| > 1.5 | 35% |
| 1.0–1.5 | 25% |
| 0.5–1.0 | 15% |
| < 0.5 | 10% |

### Sizing theo Max Drawdown
| Max DD | Tỷ trọng tối đa |
|---|---|
| < 30% | 30% |
| 30–50% | 20% |
| 50–70% | 10% |
| > 70% | 5% |

### Global Portfolio Framework:
| Asset Class | Conservative | Balanced | Aggressive |
|-------------|-------------|----------|------------|
| VN Stocks | 20% | 25% | 30% |
| US Stocks/ETF | 30% | 35% | 35% |
| Bonds/Cash | 25% | 10% | 5% |
| Gold | 15% | 15% | 10% |
| Crypto | 0% | 5% | 10% |
| Forex/Commodities | 0% | 5% | 10% |
| EM ETF | 10% | 5% | 0% |

### DCA Strategy
- Không all-in một lúc
- Chia 3–5 lần mua trong 4–8 tuần
- Mua thêm khi RSI giảm về vùng oversold
- **ETF DCA:** Cùng ngày mỗi tháng, không time the market

---

## Step 11: Output Formats

### 📊 VN Stock Output
```
## 📊 [TICKER] — [Tên công ty]
Giá: X,XXX VND | Hôm nay: +/-X.XX% | Volume: XM

### Kỹ thuật
- RSI: XX.X [tín hiệu]
- EMA200: X,XXX [▲ Trên / ▼ Dưới] — [Uptrend / Downtrend]
- MACD: [🟢 Bullish / 🔴 Bearish]
- Bollinger: [vị trí]
- 52W: High X,XXX | Low X,XXX | Vị trí: XX%
- Score: X/15

### Định giá
- P/E hiện tại: XX.Xx (Fair: XX-XXx)
- Upside định giá: +/-XX%
- ROE: XX% | D/E: XX

### Kết luận
[🟢 MUA / 🟡 THEO DÕI / ⏳ CHỜ / 🔴 TRÁNH]
Lý do: [1-2 câu]
Vùng mua lý tưởng: [X,XXX – X,XXX VND]
```

### 🇺🇸 US Stock Output
```
## 🇺🇸 [TICKER] — [Company Name]
Price: $XXX.XX | Today: +/-X.XX% | Volume: XM | Market Cap: $X.XB

### Technical
- RSI: XX.X [signal]
- EMA200: $XXX [▲ Above / ▼ Below]
- MACD: [🟢 Bullish / 🔴 Bearish]
- 52W: High $XXX | Low $XXX | Position: XX%

### Valuation
- Forward P/E: XX.Xx (Sector avg: XX-XXx)
- PEG Ratio: X.XX
- FCF Yield: X.X%
- Next Earnings: [Date]

### Kết luận
[🟢 MUA / 🟡 THEO DÕI / ⏳ CHỜ / 🔴 TRÁNH]
Lý do: [1-2 câu]
Entry zone: $XXX – $XXX
```

### 💱 Forex Output
```
## 💱 [PAIR] — Forex Analysis
Price: X.XXXX | Today: +/-X.XX% | Session: [Asian/European/US]

### Technical
- RSI: XX.X | EMA200: X.XXXX [▲/▼]
- MACD: [🟢/🔴] | Fibonacci: [key level]
- Support: X.XXXX | Resistance: X.XXXX

### Macro
- Rate differential: [FED X.XX% vs ECB/BOJ X.XX%]
- DXY: XXX.X [trend]
- Key data upcoming: [event + date]

### Trade Setup
Direction: [🟢 LONG / 🔴 SHORT / 🟡 NEUTRAL]
Entry: X.XXXX | SL: X.XXXX (-XX pips) | TP: X.XXXX (+XX pips)
R:R: 1:X | Lot size (2% risk, $5K account): X.XX lots
```

### 🏆 Commodity Output
```
## 🏆 [COMMODITY] — Analysis
Price: $X,XXX | Today: +/-X.XX%

### Technical
- RSI: XX.X | EMA200: $X,XXX [▲/▼]
- Key S/R: $X,XXX / $X,XXX

### Drivers
- [Factor 1: impact]
- [Factor 2: impact]

### Kết luận
[🟢 MUA / 🟡 TRUNG LẬP / 🔴 TRÁNH]
Vùng mua: $X,XXX – $X,XXX
```

### 📈 ETF Output
```
## 📈 [ETF] — [Name]
Price: $XXX.XX | YTD: +/-X.XX% | Expense: X.XX% | Yield: X.X%

### Technical
- RSI: XX.X | EMA200: $XXX [▲/▼]
- Drawdown từ ATH: -X.X%

### So sánh
- vs S&P 500: [outperform/underperform] XX%
- vs category: [ranking]

### DCA Estimate ($XXX/tháng)
- 5 năm: ~$XX,XXX (gốc $XX,XXX, lãi ~$XX,XXX)
- 10 năm: ~$XX,XXX

### Kết luận
[🟢 DCA / 🟡 CHỜ / 🔴 TRÁNH]
```

---

## Step 12: Swing Trading & Lướt Sóng (VN)

Khi user hỏi về **lướt sóng, swing trading, scalping, day trading**, hoặc muốn trade ngắn hạn (2-10 ngày):

Reference đầy đủ: `references/swing-trading-vn.md`

### Quick Workflow

1. **Screening:** Chạy swing screener tìm mã phù hợp
   ```bash
   python3 ~/.openclaw/workspace/skills/market-analyst/scripts/scan_market.py --rsi 45 --exchange HOSE
   ```

2. **Technical check (swing-specific):**
   - RSI divergence (bullish/bearish) trên D1
   - MACD crossover position (vùng âm = mua mạnh)
   - Bollinger squeeze → chờ breakout
   - ADX > 25 → trend đủ mạnh để swing

3. **Entry criteria:**
   - R:R tối thiểu 1:2 (KHÔNG trade nếu < 1:2)
   - Volume xác nhận (> 1.5x avg 20 phiên)
   - Stop loss xác định TRƯỚC khi vào lệnh

4. **Position sizing:**
   - 2% rule: Max risk 2% vốn per trade
   - Max 3-5 vị thế swing cùng lúc

### Output Format (Swing)
```
## 🏄 [TICKER] — Swing Analysis
Setup: [RSI Divergence / BB Squeeze / MACD Cross / ...]
Entry: X,XXX VND | Stop Loss: X,XXX (-X%) | Target: X,XXX (+X%)
R:R: 1:X | Position Size: X% vốn (XX CP)
Timeframe: X-X ngày
⚡ Confidence: [Cao/Trung bình/Thấp]
```

---

## References

### VN Market
- `references/sector-fundamentals.md` — P/E chuẩn, catalyst, risk từng ngành VN
- `references/sector-update-2026.md` — Cập nhật sector Q1/2026
- `references/swing-trading-vn.md` — Swing trading, scalping, lướt sóng VN

### US & Global
- `references/us-equities.md` — Top 20 S&P 500, sector breakdown US, P/E benchmarks, ADR/OTC
- `references/forex-guide.md` — Major/cross pairs, factors, sessions, swap rates
- `references/global-etf.md` — VOO/QQQ/SPY so sánh, VNM ETF, EM ETFs, Bond ETFs, DCA strategy

### Macro & Asset-specific
- `references/macro-update-2026-03.md` — Macro context 03/2026: FED, VN-Index, Iran War
- `references/crypto-analysis.md` — Framework phân tích crypto/BNB
- `references/gold-analysis.md` — Framework phân tích vàng XAUUSD

### Knowledge Base
- `references/financial-analysis-knowledge.md` — RSI, MACD, P/E, Sharpe, DCA, Global portfolio
- `references/advanced-ta.md` — Fibonacci, Elliott Wave, Volume Profile
- `references/return-estimation.md` — Methodology estimate sinh lời

## Scripts

- `scripts/scan_market.py` — Scan VN + US exchanges (HOSE, HNX, NASDAQ, NYSE)
- `scripts/scan_global.py` — Scan global markets (US, crypto, forex, commodities)
- `scripts/analyze_stock.py` — Phân tích kỹ thuật sâu 1 mã
- `scripts/estimate_returns.py` — Estimate lợi nhuận theo lịch sử
- `scripts/dca_calculator.py` — Tính DCA tích lũy hàng tháng

**DCA Calculator:**
```bash
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/dca_calculator.py [monthly_vnd] [years]
# Ví dụ: 2 triệu/tháng, 10 năm
python3 ~/.openclaw/workspace/skills/market-analyst/scripts/dca_calculator.py 2000000 10
```

---

*⚠️ Phân tích mang tính tham khảo, không phải khuyến nghị đầu tư. DYOR.*
