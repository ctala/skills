# WordPal

WordPal 是面向 ClawHub / Agent 工作流的词汇学习技能，提供新词暂存、出题、答题判定、复习调度与学习总结。

## 功能概览

- `stage-word.js`: 新词进入 `pending_words`，避免直接污染正式词库
- `next-question.js`: 统一出题入口，返回题型规划与题面约束
- `submit-answer.js`: 统一答题提交入口，返回评分结果与进度
- `updater.js`: 依据事件推进状态并写入 FSRS 结果
- `profile.js`: 读写用户画像（`user_profile`）
- `push-plan.js`: 将 `push_times` 转换为 learn/review 注册计划
- `question-plan.js`: 按难度、状态、上一题类型稳定选择题型
- `session-context.js`: 聚合用户画像、今日进度、近期记忆摘要
- `session-summary.js`: 按 `op_id` 输出结构化学习/复习总结
- `select-review.js`: 筛选到期复习词
- `report-stats.js`: 输出总量、趋势与风险词统计
- `validate-new-words.js`: 新词去重与合法性校验

## 安装说明

### 环境要求

- Node.js `>= 22.5.0`
- macOS / Linux / Windows
- 如需通过 CLI 安装/发布：`clawhub`

`node:sqlite` 为 Node 内置模块，本仓库通常不需要 `npm install` 即可运行。

### 1. 通过 ClawHub 安装

```bash
clawhub install wordpal
```

`clawhub` 默认将技能安装到：`~/.openclaw/skills/wordpal`（managed 全局目录）。

如需安装到自定义工作目录：

```bash
clawhub install wordpal --workdir <your-workdir> --dir skills
```

### 2. 确认 Node 版本

```bash
node --version
```

### 3. 查看可用脚本

```bash
cd ~/.openclaw/skills/wordpal
npm run
```

## 发布到 ClawHub

```bash
clawhub publish . \
  --slug wordpal \
  --name "WordPal" \
  --version 0.1.0 \
  --tags latest \
  --changelog "Initial release"
```

LICENSE: [LICENSE](./LICENSE)（MIT）

## 数据目录约定

- 默认 workspace：`~/.openclaw/workspace/wordpal`
- 词库文件：`~/.openclaw/workspace/wordpal/vocab.db`
- 用户画像：`vocab.db` 的 `user_profile` 表
- 记忆摘要目录：`~/.openclaw/workspace/memory`

可通过 `--workspace-dir` 与 `--memory-dir` 覆盖默认目录。

## 项目结构

```text
.
├── README.md
├── CHANGELOG.md
├── SKILL.md
├── docs/
│   └── scripts-contract.md
├── references/
│   ├── features.md
│   ├── onboarding.md
│   ├── learn.md
│   ├── review.md
│   └── report.md
└── scripts/
    ├── next-question.js
    ├── profile.js
    ├── push-plan.js
    ├── question-plan.js
    ├── stage-word.js
    ├── submit-answer.js
    ├── updater.js
    ├── session-context.js
    ├── session-summary.js
    ├── select-review.js
    ├── report-stats.js
    └── lib/
```
