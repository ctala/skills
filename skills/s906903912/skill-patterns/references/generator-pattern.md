# Pattern 2: Generator（生成器）

## 核心作用

强制输出**结构一致**的内容，解决"每次生成格式都不一样"的问题。

## 适用场景

- 技术报告/文档生成
- API 文档
- 项目脚手架
- 标准化邮件/公告
- Commit Message 生成

## 目录结构

```
skills/report-generator/
├── SKILL.md
├── references/
│   └── style-guide.md      # 风格指南（语气/格式）
└── assets/
    └── report-template.md  # 输出模板
```

## SKILL.md 模板

```markdown
---
name: report-generator
description: 生成结构化的技术报告。当用户要求撰写、创建或起草报告、总结、分析文档时激活。
metadata:
  pattern: generator
  output-format: markdown
  trigger-phrases: [写报告，生成文档，创建总结，draft a report, write a summary]
---

你是技术报告生成器。**严格按以下步骤执行**：

## Step 1: 加载风格指南
加载 `references/style-guide.md` 获取语调和格式规范。

## Step 2: 加载模板
加载 `assets/report-template.md` 获取必需的输出结构。

## Step 3: 收集缺失信息
向用户询问以下信息（如未提供）：
- 主题或核心内容
- 关键发现或数据点
- 目标受众（技术/管理层/大众）
- 期望长度（简短/详细）

## Step 4: 填充模板
按风格指南规则填充模板的每个字段。
**禁止**省略模板中的任何章节。

## Step 5: 输出
返回完整的 Markdown 文档。

## 输出要求
- 使用 Markdown 格式
- 所有章节标题与模板一致
- 引用风格指南中的语气规范
- 如有数据，用表格或列表呈现
```

## assets/report-template.md 模板

```markdown
# {{标题}}

## 执行摘要
{{200 字以内的核心结论}}

## 背景
{{问题背景/上下文}}

## 方法论
{{分析方法/工具/数据来源}}

## 关键发现
{{分点列出 3-5 个核心发现}}

## 详细分析
{{深入分析，可分小节}}

## 建议与下一步
{{可操作的建议}}

## 附录
{{补充材料/参考链接}}

---
*生成时间：{{日期}}*
*作者：{{生成者}}*
```

## references/style-guide.md 模板

```markdown
# 技术报告风格指南

## 语气规范
- **技术受众**：专业、精确、可含术语
- **管理层受众**：结论先行、避免技术细节、强调 ROI
- **大众受众**：通俗易懂、多用类比、解释术语

## 格式规范
- 标题使用 Sentence case（仅首字母大写）
- 代码块必须标注语言
- 表格必须有表头
- 引用使用 > 格式

## 禁用内容
- 避免"可能"、"也许"等模糊词汇
- 不使用第一人称（我/我们）
- 不添加未经验证的数据

## 长度控制
- 执行摘要：≤200 字
- 关键发现：3-5 条，每条≤50 字
- 详细分析：根据主题调整，但每节≤800 字
```

## 变体：交互式生成

```markdown
## Step 3（交互版）: 分步确认

每填充一个章节后，向用户展示并询问：
"这部分内容是否符合你的预期？需要调整吗？"

用户确认后再继续下一章节。
```

## 优缺点

| 优点 | 缺点 |
|-----|------|
| 输出高度一致 | 模板僵化，灵活性低 |
| 新人也能生成专业内容 | 需要维护模板库 |
| 易于自动化验收 | 模板设计成本高 |

## 组合模式

### Generator + Inversion

先用 Inversion 模式采集需求，再用 Generator 填充模板：

```markdown
## Phase 1: 需求采集（Inversion）
问 5 个问题了解用户需求

## Phase 2: 生成报告（Generator）
用采集的信息填充模板
```

### Generator + Reviewer

生成后自动自检：

```markdown
## Step 6: 质量检查
加载 `references/quality-checklist.md` 自检：
- [ ] 所有章节完整
- [ ] 无拼写错误
- [ ] 数据有来源标注

发现问题则修正后重新输出。
```

---

## 检查清单

- [ ] `assets/` 目录有完整模板
- [ ] `references/` 目录有风格指南
- [ ] SKILL.md 明确步骤顺序
- [ ] 有缺失信息处理逻辑（询问用户）
- [ ] 输出格式明确（Markdown/JSON 等）
