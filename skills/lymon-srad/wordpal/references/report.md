# WordPal · 学习报告流程

学习报告统一采用「脚本算事实 + LLM 做解读」：
先读取 `session-context.js` 的记忆摘要与画像，再读取 `report-stats.js` 的统计 JSON，最后基于这些事实生成个性化报告。

---

## 第零步：风格识别与持久化（先做）

`session-context.js --mode report` 已由主协议先执行，可直接读取 `data.profile.report_style`：
- 允许值：`MIXED | EXAM | LIFE`
- 缺失或非法值：按 `MIXED` 处理

若用户在本次对话明确提出切换风格，先调用 `profile.js set --report-style ...`，再继续后续步骤：
- 「偏备考」「考试导向」「考试模式」→ `EXAM`
- 「偏生活」「场景导向」「生活模式」→ `LIFE`
- 「混合」「都要」「双视角」→ `MIXED`

读取已拿到的 `data.memory_digest` 与最新 `data.profile.learning_goal`，作为个性化洞察的唯一事实来源。

---

## 第一步：调用统计脚本（必做）

先执行只读脚本，拿到结构化统计结果：

`node {baseDir}/scripts/report-stats.js --days 7 --top-risk 10`

可选参数：
- `--today YYYY-MM-DD`：回放指定日期
- `--workspace-dir <path>`：本地调试目录

**执行规则：**
- 先执行脚本并等待成功返回，再组织报告内容
- 后续所有数字只允许来自脚本 JSON，不允许 LLM 在文本里二次计算
- 若脚本返回 `data.totals.total_words = 0`，直接结束并告知当前没有学习记录

---

## 第二步：读取事实层

两份脚本的字段含义以各自 JSON 输出为准；本流程只读取下列最小事实集。

本流程至少需要读取：
- `session-context.data.memory_digest`
- `session-context.data.profile.learning_goal`
- `session-context.data.profile.report_style`
- `report-stats.data.totals`
- `report-stats.data.due`
- `report-stats.data.trend_7d`
- `report-stats.data.risk_words`
- `report-stats.data.next_action.kind`

---

## 第三步：LLM 解读边界

报告格式不固定，但必须遵守：
- 只能引用已读取到的真实信息，不编造用户经历
- 个性化洞察优先使用 `memory_digest`，不足时降级到 `learning_goal`
- 风险词只能来自 `data.risk_words`
- 不输出 JSON 原文，不解释 `risk_score` 公式

---

## 第四步：下一步动作

只读取 `report-stats.data.next_action.kind`：
- `review_now` -> 引导用户进入 review
- `learn_now` -> 引导用户进入 learn
- `light_encouragement` -> 给轻量反馈，不强推任务

---

## LLM 责任

- 只负责 `report_style` 的自然语言映射与个性化解读
- 只使用脚本给出的事实层字段
- 不自行计算统计数字、趋势或复习间隔
