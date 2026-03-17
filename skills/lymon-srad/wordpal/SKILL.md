---
name: WordPal
description: 结合用户画像与 memory 管理英语单词学习流程，包含新词学习(learn)、到期复习(review)、答题反馈和学习报告生成(report)。
user-invocable: true
metadata:
  openclaw:
    emoji: "📘"
    requires:
      bins:
        - node
---
# WordPal · 主控协议

## 技能目录约定
- `{baseDir}` 由 OpenClaw 自动替换为本技能的实际安装路径

## 执行顺序
1. 判断用户意图并路由：
   - features（问功能/能力）→ 读 `references/features.md`，不执行脚本
   - learn（学习意图，或只输入 `/wordpal`）→ 读 `references/learn.md`
   - review（复习意图）→ 读 `references/review.md`
   - report（报告意图）→ 读 `references/report.md`
2. 进入 learn/review/report 前，先执行 `session-context.js --mode <learn|review|report>`：
   - `profile_exists = false` → 读取 `references/onboarding.md` 引导初始化
   - `profile_exists = true` → `data.profile` 为用户画像唯一真值，继续流程

## 共享事件映射（learn/review 共用）
- 答对 → `submit-answer.js --event correct`
- 答错 → `submit-answer.js --event wrong`
- 提示后记住 → `submit-answer.js --event remembered_after_hint`
- 提示后仍不会 → `submit-answer.js --event wrong`
- 跳过/会了/斩词 → `submit-answer.js --event skip`
- 新词确认进入学习 → `next-question.js --validate`
`remembered_after_hint` vs `wrong` 判定见 `learn.md` / `review.md`「阶段 B-3」。

## 脚本通用规则
- 所有脚本前缀：`node {baseDir}/scripts/`
- 成功返回 `{ meta, data }` JSON
- 脚本失败统一兜底：`系统暂时不可用，请稍后再试。`

## 禁止项
- 不要直接操作 SQLite 词库文件或输出内部表快照。
- 不要跳过脚本直接改词条。
