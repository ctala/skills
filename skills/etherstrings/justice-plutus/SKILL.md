---
name: justice-plutus
description: A股股票分析助手，支持立即触发分析、设定定时、更新自选股（OCR识别图片）、临时分析指定股票
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["gh", "python3"]
---

# JusticePlutus A股分析助手

## 命令

### 立即分析
**触发词：** 「立即分析」「跑一下」「分析一下」

立即触发 GitHub Actions 工作流运行股票分析：

```bash
gh workflow run daily_analysis.yml -R Etherstrings/JusticePlutus
```

运行后可通过以下命令查看进度：
```bash
gh run list -R Etherstrings/JusticePlutus --limit 3
```

---

### 设定定时
**触发词：** 「设定定时 HH:MM」「定时 09:35」

修改本地 cron 配置中股票分析任务的执行时间。

1. 更新 `~/.openclaw/cron/jobs.json` 中 `justice-plutus` job 的 cron 表达式
2. 提示用户是否同步更新 GitHub Actions schedule（需手动编辑 `.github/workflows/daily_analysis.yml`）

**示例：** 「设定定时 09:35」→ cron 改为 `35 1 * * 1-5`（UTC，对应北京时间 09:35）

---

### 更新自选股
**触发词：** 「更新自选股」+ 图片

1. 调用 OCR 脚本识别图片中的股票代码：
   ```bash
   ~/.openclaw/skills/justice-plutus/scripts/ocr.sh <image_path>
   ```
2. 展示识别结果，请用户确认
3. 确认后更新 GitHub Actions 变量：
   ```bash
   gh variable set STOCK_LIST --body "<codes>" -R Etherstrings/JusticePlutus
   ```

---

### 临时分析
**触发词：** 「临时分析 600519」或「临时分析」+ 图片

1. 若提供图片，先 OCR 提取股票代码
2. 触发指定股票的分析工作流：
   ```bash
   gh workflow run daily_analysis.yml -R Etherstrings/JusticePlutus -f stocks=<codes>
   ```

---

## OCR 脚本

脚本位于 `scripts/ocr.sh`，输出识别到的6位股票代码（逗号分隔）。

支持：
- macOS Shortcuts（Vision 框架，高精度）
- Tesseract（fallback）
