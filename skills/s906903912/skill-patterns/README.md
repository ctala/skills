# Agent Skill 设计模式模板库

基于 Google ADK 和生态系统的最佳实践，提供 5 个可复用的技能设计模式。

## 🎯 适用场景

- 创建新的 Agent Skill 时需要结构化模板
- 优化现有技能的设计和质量
- 团队内部统一技能开发规范
- 学习 Agent Skill 设计的最佳实践

## 📦 包含的模式

| 模式 | 用途 | 典型场景 |
|-----|------|---------|
| [Tool Wrapper](./references/tool-wrapper-pattern.md) | 注入领域专业知识 | 框架规范、团队约定、API 使用指南 |
| [Generator](./references/generator-pattern.md) | 生成结构化内容 | 技术报告、文档、脚手架、Commit Message |
| [Reviewer](./references/reviewer-pattern.md) | 评审/审计/打分 | Code Review、安全审计、质量检查 |
| [Inversion](./references/inversion-pattern.md) | 先采访再执行 | 需求模糊的项目规划、复杂系统设计 |
| [Pipeline](./references/pipeline-pattern.md) | 多步骤顺序执行 | 文档生成、代码迁移、数据转换 |

## 🚀 快速开始

### 1. 激活技能

在对话中提到以下关键词即可激活：
- 创建 skill
- 技能模板
- skill 设计
- agent 模式
- skill pattern
- 技能结构

### 2. 选择模式

技能会根据你的需求推荐最适合的设计模式，或组合多个模式。

### 3. 按模板创建

遵循推荐模式的结构和流程，创建你的技能。

## 📁 目录结构

```
skill-patterns/
├── SKILL.md                          # 技能入口
├── README.md                         # 使用说明
└── references/
    ├── tool-wrapper-pattern.md       # 模式 1：工具包装器
    ├── generator-pattern.md          # 模式 2：生成器
    ├── reviewer-pattern.md           # 模式 3：评审器
    ├── inversion-pattern.md          # 模式 4：逆向采访
    ├── pipeline-pattern.md           # 模式 5：流水线
    └── creation-checklist.md         # 创建检查清单
```

## 💡 模式组合示例

- **Generator + Reviewer**: 生成报告后自动质量检查
- **Inversion + Generator**: 先采访需求，再生成方案
- **Pipeline + Reviewer**: 每步完成后评审质量
- **Tool Wrapper + Pipeline**: 每步加载不同规范

## 📊 选择决策树

```
用户请求是否明确？
├─ 是 → 是否需要特定领域知识？
│   ├─ 是 → Tool Wrapper
│   └─ 否 → 是否需要固定输出格式？
│       ├─ 是 → Generator
│       └─ 否 → 是否是评审任务？
│           ├─ 是 → Reviewer
│           └─ 否 → 单步执行（无需模式）
└─ 否 → 是否需要多轮采集需求？
    ├─ 是 → Inversion
    └─ 否 → 是否有多步骤强制顺序？
        ├─ 是 → Pipeline
        └─ 否 → Inversion（先澄清）
```

## 📖 来源

设计模式基于：Google Cloud Tech - "5 Agent Skill design patterns every ADK developer should know"

## 📝 版本

- v1.0.0 - 初始发布，包含 5 个核心模式 + 创建检查清单

## 🤝 贡献

欢迎提交新的模式变体和改进建议！
