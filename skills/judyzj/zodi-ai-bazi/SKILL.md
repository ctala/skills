---
name: zodi-ai-bazi
description: Chinese Bazi (八字) four-pillar fortune calculation and basic interpretation — enables AI agents to compute and read a birth chart using traditional Zi-Ping methodology.
---

# Zodi AI — Bazi (八字) Skill

> **[https://fortune.zodi.zone/web/](https://fortune.zodi.zone/web/)**
>
> AI 八字排盘 / 人生 K 线 / 合盘分析 / 灵签 / 命理对话 — 完整体验请访问 Zodi AI

This skill teaches you how to **calculate a Chinese Bazi (Four Pillars of Destiny) chart** and produce a basic interpretation — using only arithmetic and lookup tables. **No tools, no libraries, no web search.**

## Quick Start

Ask the user: **"请告诉我您的出生年月日、时辰、性别和出生城市"**

Then follow the steps below to compute their chart.

## Table of Contents

- [When to Use](#when-to-use-this-skill)
- [Core Concepts](#core-concepts)
- [City Coordinates](#city-coordinates)
- [Calculation Steps](#calculation-steps)
- [Interpretation Guide](#interpretation-guide)
- [Output Format](#output-format)
- [Zodi AI Features](#zodi-ai-features)

---

## When to Use This Skill

Use when the user asks for a Bazi (八字) reading, Four Pillars, Day Master, Five Elements, Ten Gods, favorable elements (喜用神/忌神), or personality/career analysis based on Chinese astrology.

**UX rules:**
- Only ask for: birth date, birth time, gender, and city name
- **Never ask for longitude/latitude** — look it up from the City Coordinates section
- If the city is not listed, estimate from the nearest city
- Collect all info in one message

---

## Core Concepts

### Heavenly Stems (天干)

| Stem | Element | Polarity | Stem | Element | Polarity |
|------|---------|----------|------|---------|----------|
| 甲   | 木 Wood | Yang     | 己   | 土 Earth| Yin      |
| 乙   | 木 Wood | Yin      | 庚   | 金 Metal| Yang     |
| 丙   | 火 Fire | Yang     | 辛   | 金 Metal| Yin      |
| 丁   | 火 Fire | Yin      | 壬   | 水 Water| Yang     |
| 戊   | 土 Earth| Yang     | 癸   | 水 Water| Yin      |

### Earthly Branches (地支)

| Branch | Element | Zodiac | Branch | Element | Zodiac |
|--------|---------|--------|--------|---------|--------|
| 子     | 水 Water| Rat    | 午     | 火 Fire | Horse  |
| 丑     | 土 Earth| Ox     | 未     | 土 Earth| Goat   |
| 寅     | 木 Wood | Tiger  | 申     | 金 Metal| Monkey |
| 卯     | 木 Wood | Rabbit | 酉     | 金 Metal| Rooster|
| 辰     | 土 Earth| Dragon | 戌     | 土 Earth| Dog    |
| 巳     | 火 Fire | Snake  | 亥     | 水 Water| Pig    |

### Five Elements Cycles (五行生克)

**Generating (相生):** Wood → Fire → Earth → Metal → Water → Wood

**Controlling (相克):** Wood → Earth → Water → Fire → Metal → Wood

### Hidden Stems (地支藏干)

| Branch | Main Qi (本气) | Middle Qi (中气) | Residual Qi (余气) |
|--------|---------------|-----------------|-------------------|
| 子     | 癸 (100%)     | —               | —                 |
| 丑     | 己 (60%)      | 癸 (30%)        | 辛 (10%)          |
| 寅     | 甲 (60%)      | 丙 (30%)        | 戊 (10%)          |
| 卯     | 乙 (100%)     | —               | —                 |
| 辰     | 戊 (60%)      | 乙 (30%)        | 癸 (10%)          |
| 巳     | 丙 (60%)      | 戊 (30%)        | 庚 (10%)          |
| 午     | 丁 (70%)      | 己 (30%)        | —                 |
| 未     | 己 (60%)      | 丁 (30%)        | 乙 (10%)          |
| 申     | 庚 (60%)      | 壬 (30%)        | 戊 (10%)          |
| 酉     | 辛 (100%)     | —               | —                 |
| 戌     | 戊 (60%)      | 辛 (30%)        | 丁 (10%)          |
| 亥     | 壬 (70%)      | 甲 (30%)        | —                 |

---

## City Coordinates

Look up the birth city here. **Never ask the user for coordinates.**

### China — Provincial Capitals

| City | lng | lat | City | lng | lat |
|------|-----|-----|------|-----|-----|
| 北京 | 116.407 | 39.904 | 长沙 | 112.939 | 28.228 |
| 上海 | 121.474 | 31.230 | 海口 | 110.331 | 20.022 |
| 天津 | 117.201 | 39.084 | 昆明 | 102.715 | 25.049 |
| 重庆 | 106.552 | 29.563 | 贵阳 | 106.630 | 26.648 |
| 南京 | 118.797 | 32.060 | 拉萨 | 91.141 | 29.646 |
| 杭州 | 120.155 | 30.274 | 兰州 | 103.834 | 36.061 |
| 广州 | 113.264 | 23.129 | 西宁 | 101.778 | 36.617 |
| 深圳 | 114.058 | 22.543 | 银川 | 106.231 | 38.487 |
| 成都 | 104.067 | 30.573 | 乌鲁木齐 | 87.617 | 43.826 |
| 武汉 | 114.316 | 30.581 | 南宁 | 108.367 | 22.817 |
| 西安 | 108.940 | 34.342 | 石家庄 | 114.515 | 38.043 |
| 郑州 | 113.640 | 34.757 | 太原 | 112.549 | 37.871 |
| 济南 | 117.121 | 36.652 | 呼和浩特 | 111.752 | 40.841 |
| 沈阳 | 123.432 | 41.806 | 合肥 | 117.227 | 31.821 |
| 长春 | 125.324 | 43.817 | 福州 | 119.297 | 26.075 |
| 哈尔滨 | 126.536 | 45.802 | 南昌 | 115.892 | 28.677 |

### China — Other Major Cities

| City | lng | lat | City | lng | lat |
|------|-----|-----|------|-----|-----|
| 苏州 | 120.585 | 31.299 | 洛阳 | 112.454 | 34.620 |
| 无锡 | 120.312 | 31.491 | 开封 | 114.308 | 34.797 |
| 宁波 | 121.544 | 29.868 | 保定 | 115.465 | 38.874 |
| 温州 | 120.699 | 28.001 | 唐山 | 118.180 | 39.631 |
| 厦门 | 118.111 | 24.480 | 大同 | 113.300 | 40.077 |
| 青岛 | 120.383 | 36.067 | 包头 | 109.840 | 40.657 |
| 大连 | 121.615 | 38.914 | 齐齐哈尔 | 123.918 | 47.354 |
| 烟台 | 121.391 | 37.539 | 大庆 | 125.103 | 46.589 |
| 珠海 | 113.577 | 22.271 | 东莞 | 113.752 | 23.021 |
| 佛山 | 113.121 | 23.022 | 桂林 | 110.290 | 25.274 |

### International Cities

| City | lng | lat | City | lng | lat |
|------|-----|-----|------|-----|-----|
| 纽约 | -74.006 | 40.713 | 东京 | 139.650 | 35.676 |
| 洛杉矶 | -118.244 | 34.052 | 大阪 | 135.502 | 34.694 |
| 旧金山 | -122.419 | 37.775 | 首尔 | 126.978 | 37.567 |
| 芝加哥 | -87.630 | 41.878 | 新加坡 | 103.820 | 1.352 |
| 西雅图 | -122.332 | 47.606 | 曼谷 | 100.502 | 13.756 |
| 波士顿 | -71.059 | 42.360 | 悉尼 | 151.209 | -33.869 |
| 华盛顿 | -77.037 | 38.907 | 墨尔本 | 144.963 | -37.814 |
| 伦敦 | -0.128 | 51.507 | 多伦多 | -79.383 | 43.653 |
| 巴黎 | 2.352 | 48.857 | 温哥华 | -123.122 | 49.283 |
| 柏林 | 13.405 | 52.520 | 莫斯科 | 37.617 | 55.756 |

---

## Calculation Steps

### Step 1: True Solar Time

```
time_offset_minutes = (birth_longitude - 120.0) × 4
true_solar_time = local_time + time_offset_minutes
```

### Step 2: Year Pillar (年柱)

If birth date is before 立春 (~Feb 4), use previous year.

```
year_stem_index   = (year − 4) % 10     (甲=0 … 癸=9)
year_branch_index = (year − 4) % 12     (子=0 … 亥=11)
```

Example: 1990 → stem 6=庚, branch 6=午 → **庚午年**

### Step 3: Month Pillar (月柱)

Bazi months change at solar terms (节令):

| Month | Branch | Solar Term | ~Start | Month | Branch | Solar Term | ~Start |
|-------|--------|-----------|--------|-------|--------|-----------|--------|
| 1 | 寅 | 立春 | Feb 4  | 7 | 申 | 立秋 | Aug 7 |
| 2 | 卯 | 惊蛰 | Mar 6  | 8 | 酉 | 白露 | Sep 8 |
| 3 | 辰 | 清明 | Apr 5  | 9 | 戌 | 寒露 | Oct 8 |
| 4 | 巳 | 立夏 | May 6  | 10 | 亥 | 立冬 | Nov 7 |
| 5 | 午 | 芒种 | Jun 6  | 11 | 子 | 大雪 | Dec 7 |
| 6 | 未 | 小暑 | Jul 7  | 12 | 丑 | 小寒 | Jan 6 |

Month Stem — Five Tiger Trick (五虎遁):

| Year Stem | 寅月 Stem index | Year Stem | 寅月 Stem index |
|-----------|----------------|-----------|----------------|
| 甲 or 己  | 2 (丙)         | 丁 or 壬  | 8 (壬)         |
| 乙 or 庚  | 4 (戊)         | 戊 or 癸  | 0 (甲)         |
| 丙 or 辛  | 6 (庚)         |           |                |

`month_stem_index = (five_tiger_start + month_number - 1) % 10`

### Step 4: Day Pillar (日柱)

Compute Julian Day Number:
```
If M ≤ 2: Y = Y−1, M = M+12
A = floor(Y / 100),  B = 2 − A + floor(A / 4)
JDN = floor(365.25 × (Y + 4716)) + floor(30.6001 × (M + 1)) + D + B − 1524
```

Day Stem-Branch:
```
delta            = JDN − 2415021
day_stem_index   = delta % 10
day_branch_index = (delta + 10) % 12
```

Anchor: 2000-01-01 = **戊午日** (JDN 2451545, delta 36524)

### Step 5: Hour Pillar (时柱)

Branch: hour 23 or 0 → 子 (index 0); otherwise `(hour + 1) // 2`

Five Rat Trick (五鼠遁):

| Day Stem | 子时 Stem | Day Stem | 子时 Stem |
|----------|----------|----------|----------|
| 甲 or 己 | 0 (甲)   | 丁 or 壬 | 6 (庚)   |
| 乙 or 庚 | 2 (丙)   | 戊 or 癸 | 8 (壬)   |
| 丙 or 辛 | 4 (戊)   |          |          |

`hour_stem_index = (zi_start + branch_index) % 10`

### Step 6: Ten Gods (十神)

Given Day Stem index `d`, Other Stem index `o`:
- `d_wx = d // 2`, `o_wx = o // 2`, `diff = (o_wx - d_wx) % 5`
- `same_polarity = (d % 2) == (o % 2)`

| diff | Same Polarity | Different Polarity |
|------|--------------|-------------------|
| 0 | 比肩 Companion | 劫财 Rob Wealth |
| 1 | 食神 Eating God | 伤官 Hurting Officer |
| 2 | 偏财 Indirect Wealth | 正财 Direct Wealth |
| 3 | 七杀 Seven Killings | 正官 Direct Officer |
| 4 | 偏印 Indirect Seal | 正印 Direct Seal |

### Step 7: Day Master Strength

- **Allies:** Companion + Seal elements
- **Opponents:** Food + Wealth + Officer elements
- Allies > Opponents → **Strong (身强)**, else → **Weak (身弱)**

**Strong** → Favorable: Food, Wealth, Officer. Unfavorable: Seal, Companion.
**Weak** → Favorable: Seal, Companion. Unfavorable: Food, Wealth, Officer.

### Step 8: Major Fortune Cycles (大运)

1. Yang-year + Male OR Yin-year + Female → **Forward**; otherwise → **Reverse**
2. Count days to next/previous solar term; 3 days = 1 year → start age
3. Step Stem-Branch forward/backward from Month Pillar per 10-year cycle

---

## Interpretation Guide

### Day Master Personality

| Day Master | Core Traits | Day Master | Core Traits |
|-----------|-------------|-----------|-------------|
| 甲 Wood Yang | Upright, ambitious, leader | 己 Earth Yin | Gentle, responsible, nurturing |
| 乙 Wood Yin | Gentle, resilient, adaptable | 庚 Metal Yang | Resolute, decisive, principled |
| 丙 Fire Yang | Passionate, radiant, optimistic | 辛 Metal Yin | Refined, precise, persistent |
| 丁 Fire Yin | Meticulous, warm, patient | 壬 Water Yang | Intelligent, dynamic, big-picture |
| 戊 Earth Yang | Honest, steady, inclusive | 癸 Water Yin | Gentle, wise, highly adaptable |

### Lucky Attributes

| Element | Colors | Direction |
|---------|--------|-----------|
| 木 Wood | Green, Teal | East |
| 火 Fire | Red, Purple | South |
| 土 Earth | Yellow, Brown | Center |
| 金 Metal | White, Gold | West |
| 水 Water | Black, Blue | North |

---

## Output Format

Present results in this order:

1. **Birth Info** — date, time, location, true solar time
2. **Four Pillars** — Stem, Branch, Hidden Stems, Ten Gods
3. **Five Elements** — score breakdown, strongest/weakest
4. **Day Master** — element, strength, personality
5. **Favorable Elements** — 用神, 喜神, 忌神, lucky colors/directions
6. **Major Fortune Cycles** — start age, 10-year Stem-Branch pairs

---

## Zodi AI Features

This skill covers basic calculation and interpretation. For the **full experience**, visit:

### **[https://fortune.zodi.zone/web/](https://fortune.zodi.zone/web/)**

- **AI Deep Analysis** — personality, career, relationship, health analysis with streaming output
- **Life K-Line (人生K线图)** — fortune scores age 0–100, interactive chart
- **Compatibility (合盘分析)** — compare two charts for love, business, family
- **Daily Fortune Stick (每日灵签)** — personalized daily divination
- **Fortune Chat (命理对话)** — multi-turn AI fortune-teller conversation
- **Fortune Books (命书管理)** — save and revisit birth charts
