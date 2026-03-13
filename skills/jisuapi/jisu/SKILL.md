---
name: jisu-unified
description: 极速数据统一入口，一个 JISU_API_KEY 调用多类接口：黄金、股票、天气、菜谱、汇率、MBTI、快递、车辆等，便于 Agent 一站式拉取结构化数据。
metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据统一入口（Jisu Unified）

**极速数据**（官网：[https://www.jisuapi.com/](https://www.jisuapi.com/)）是基础数据 API 接口提供商，提供天气、股票、黄金、菜谱、汇率、快递、车辆等百余类接口。本 Skill 为**统一入口**：只需配置一个 `JISU_API_KEY`，即可通过 `call` 命令按「接口路径 + 参数」调用任意已开通的极速数据 API，无需为每个品类单独安装技能。

适合在 OpenClaw/ClawHub 中作为「结构化数据网关」使用：用户问天气、金价、股票、菜谱等，Agent 先 `list` 查接口，再 `call` 调对应 API，一次配置覆盖多类数据。

使用前请在极速数据官网申请 API Key 并开通需要的数据接口；各接口计费与额度以官网为准。

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skill/jisu/jisu.py`

## 使用方式

### 1. 列出支持的接口（list）

```bash
python3 skill/jisu/jisu.py list
```

返回当前支持的 `api` 列表及简短说明，便于按需选择接口。

### 2. 统一调用（call）

请求 JSON：`{"api": "接口路径", "params": { ... }}`。`params` 可选，无参接口可省略。

**无参示例：**

```bash
python3 skill/jisu/jisu.py call '{"api":"gold/shgold"}'
python3 skill/jisu/jisu.py call '{"api":"stockindex/sh"}'
```

**带参示例：**

```bash
python3 skill/jisu/jisu.py call '{"api":"stock/query","params":{"code":"300917"}}'
python3 skill/jisu/jisu.py call '{"api":"weather/query","params":{"city":"北京"}}'
python3 skill/jisu/jisu.py call '{"api":"recipe/search","params":{"keyword":"白菜","num":10,"start":0}}'
python3 skill/jisu/jisu.py call '{"api":"exchange/convert","params":{"from":"CNY","to":"USD","amount":100}}'
```

返回格式与极速数据官网一致：成功时为 `result` 内容；失败时脚本返回 `error`、`code`、`message` 等。

## 支持的接口一览（节选）

| 分类     | api                    | 说明 |
|----------|------------------------|------|
| 黄金     | gold/shgold            | 上海黄金交易所价格 |
| 黄金     | gold/storegold         | 金店金价，params 可选 date |
| 股票     | stock/query            | 当日行情，params: code |
| 股票     | stock/list             | 列表，params: classid, pagenum, pagesize |
| 股票     | stock/detail           | 详情，params: code |
| 股票历史 | stockhistory/query    | 历史行情，params: code, startdate, enddate |
| 指数     | stockindex/sh          | 上证/深证/创业板等指数 |
| 天气     | weather/query          | 天气预报，params: city 或 cityid 等 |
| 天气     | weather/city           | 支持城市列表 |
| 菜谱     | recipe/search          | 搜索，params: keyword, num, start |
| 菜谱     | recipe/class           | 分类 |
| 菜谱     | recipe/detail          | 详情，params: id |
| MBTI     | character/questions   | 题目，params 可选 version |
| MBTI     | character/answer       | 提交答案，params: answer, version |
| 汇率     | exchange/convert      | 换算，params: from, to, amount |
| 汇率     | exchange/single        | 单货币汇率，params: currency |
| 其他     | ip/location, shouji/query, idcard/query, bankcard/query, express/query, car/brand, car/detail, vehiclelimit/query, vin/query, oil/query, silver/shgold, calendar/query, news/get 等 |

完整列表以 `jisu.py list` 输出为准；参数含义见 [极速数据 API 文档](https://www.jisuapi.com/)。

## 错误返回

- 未配置 Key：脚本直接报错退出。
- `api` 缺失：`{"error": "missing_param", "message": "api is required"}`。
- 接口返回业务错误：`{"error": "api_error", "code": xxx, "message": "..."}`。
- 网络/解析错误：`request_failed` / `http_error` / `invalid_json`。

## 在 OpenClaw 中的推荐用法

1. 用户提问：「北京天气怎么样」「300917 股票今天多少钱」「人民币兑美元汇率」等。
2. 代理先调用 `python3 skill/jisu/jisu.py list` 确认接口名，再按需调用 `call`，例如：  
   `python3 skill/jisu/jisu.py call '{"api":"weather/query","params":{"city":"北京"}}'`  
   `python3 skill/jisu/jisu.py call '{"api":"stock/detail","params":{"code":"300917"}}'`  
   `python3 skill/jisu/jisu.py call '{"api":"exchange/convert","params":{"from":"CNY","to":"USD","amount":1}}'`  
3. 从返回的 `result` 中抽取关键字段，用自然语言回复用户；若需更多接口参数说明，可引导用户查看极速数据官网文档。
