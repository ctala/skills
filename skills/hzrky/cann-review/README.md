# CANN Review Skill 🔍

[![ClawHub](https://img.shields.io/badge/ClawHub-Publish-green)](https://clawhub.gitcode.com)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](./skill.yaml)
[![License](https://img.shields.io/badge/license-MIT-orange)](./LICENSE)

CANN runtime 项目自动化代码审查技能，帮助开发者快速完成 PR 审查工作。

## ✨ 功能特性

- 🔍 **全面审查**: 自动分析代码变更，检查内存泄漏、安全漏洞和可读性问题
- 📊 **结构化报告**: 生成清晰、专业的审查报告
- 🚀 **自动化发布**: 自动发布审查评论和 `/lgtm` 标记
- ⚙️ **可配置**: 支持自定义审查重点和严重程度阈值

## 📦 安装

### 从 ClawHub 安装

```bash
claw install cann-review
```

### 手动安装

```bash
git clone https://gitcode.com/clawhub/cann-review.git
cd cann-review
claw install .
```

## 🚀 快速开始

### 基本用法

```bash
claw run cann-review --pr-url "https://gitcode.com/cann/runtime/pull/472"
```

### 指定审查重点

```bash
# 只检查内存泄漏
claw run cann-review --pr-url "..." --focus memory

# 只检查安全问题
claw run cann-review --pr-url "..." --focus security

# 全面检查 (默认)
claw run cann-review --pr-url "..." --focus all
```

### 配置 LGTM 阈值

```bash
# 低风险才发 /lgtm
claw run cann-review --pr-url "..." --threshold low

# 中低风险都发 /lgtm (默认)
claw run cann-review --pr-url "..." --threshold medium

# 只发审查报告，不发 /lgtm
claw run cann-review --pr-url "..." --threshold high
```

## 📋 审查报告格式

```markdown
## Code Review Report

### 1. 整体情况
- **严重程度**: low
- **是否可以合入**: ✅ 可以合入

### 2. 问题点

#### 2.1 代码可读性 - 建议改进
- `rts_device.h:551` 文档中参数名不一致

### 3. 修改建议
...

### 4. 优点
- 代码结构清晰
- 错误处理完善

### 5. 内存泄漏检查
- 未发现明显的内存泄漏问题

### 6. 安全检查
- 参数空指针检查已到位

总体评价：代码质量良好，可以合入。
```

## ⚙️ 配置选项

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `pr_url` | string | 必填 | PR 页面链接 |
| `focus_areas` | string | `all` | 审查重点: `memory`, `security`, `readability`, `all` |
| `severity_threshold` | string | `medium` | 发布 /lgtm 的阈值: `low`, `medium`, `high` |

## 🔍 审查重点说明

### 内存泄漏检查 (memory)
- 动态内存分配/释放配对
- RAII 模式使用
- 异常路径资源释放
- 容器内存管理

### 安全漏洞检查 (security)
- 缓冲区溢出
- 空指针解引用
- 类型转换安全
- 整数溢出

### 代码可读性 (readability)
- 命名规范
- 注释完整性
- 代码结构
- 项目风格遵循

## 📊 严重程度等级

| 等级 | 描述 | 是否可合入 | 自动 /lgtm |
|------|------|------------|------------|
| Low | 建议性改进 | ✅ | ✅ |
| Medium | 一般问题 | ⚠️ | ✅ |
| High | 严重问题 | ❌ | ❌ |
| Critical | 安全/内存严重问题 | ❌ | ❌ |

## 🛠️ 开发

### 项目结构

```
cann-review/
├── skill.yaml      # 技能元数据定义
├── prompt.md       # 提示词模板
├── README.md       # 使用文档
├── LICENSE         # 许可证
└── examples/       # 示例
    └── example_report.md
```

### 本地测试

```bash
# 使用 OpenClaw 测试
claw test . --pr-url "https://gitcode.com/cann/runtime/pull/472"
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件

## 🙏 致谢

- OpenClaw 团队
- CANN runtime 项目组
- 所有贡献者

---

<p align="center">
  Made with ❤️ by OpenClaw Team
</p>
