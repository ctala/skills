# Pattern 3: Reviewer（评审器）

## 核心作用

将**评审标准**与**评审逻辑**分离，用外部检查清单实现模块化审计。

## 适用场景

- Code Review
- 安全审计（OWASP）
- 合规检查
- 设计审查
- 文档质量检查

## 目录结构

```
skills/code-reviewer/
├── SKILL.md
└── references/
    └── review-checklist.md   # 评审检查清单
```

## SKILL.md 模板

```markdown
---
name: code-reviewer
description: Python 代码质量评审。当用户提交代码求反馈、请求审查或需要代码审计时激活。
metadata:
  pattern: reviewer
  severity-levels: [error, warning, info]
  trigger-phrases: [代码审查，review 这个，检查代码，code review, audit this]
---

你是 Python 代码评审员。**严格按以下流程执行**：

## Step 1: 加载检查清单
加载 `references/review-checklist.md` 获取完整评审标准。

## Step 2: 理解代码意图
先阅读用户代码，理解其功能和目标。
**禁止**在不理解意图的情况下直接挑错。

## Step 3: 逐条应用检查清单
对清单中的每条规则：
1. 检查代码是否符合
2. 如违规，记录：行号 + 严重度 + 原因 + 修复建议

## Step 4: 生成结构化报告

输出格式如下：

### 📊 总览
- **功能**：这段代码做什么
- **整体质量**：一句话评价

### 🚨 错误（必须修复）
{{列出所有 error 级别问题}}

### ⚠️ 警告（建议修复）
{{列出所有 warning 级别问题}}

### ℹ️ 提示（可考虑优化）
{{列出所有 info 级别问题}}

### 📈 评分
**X/10 分** - 评分理由

### 🎯 Top 3 建议
{{按影响力排序的前 3 个改进建议}}
```

## references/review-checklist.md 模板

```markdown
# Python 代码评审检查清单 v2.0

## P0 - 错误（必须修复）

### 安全性
- [ ] 硬编码密码/密钥/API Token
- [ ] SQL 注入风险（字符串拼接 SQL）
- [ ] 命令注入风险（os.system 用户输入）
- [ ] 敏感信息打印到日志

### 正确性
- [ ] 未处理的异常（裸 except）
- [ ] 资源未释放（文件/连接未 close）
- [ ] 竞态条件风险
- [ ] 边界条件未处理（空列表/None/负数）

## P1 - 警告（建议修复）

### 可读性
- [ ] 函数超过 50 行
- [ ] 嵌套超过 4 层
- [ ] 变量命名不清晰（单字母/无意义）
- [ ] 缺少类型注解

### 性能
- [ ] 循环内重复计算
- [ ] 不必要的列表拷贝
- [ ] 使用 list 而非生成器
- [ ] N+1 查询问题

### 可维护性
- [ ] 重复代码（DRY 原则）
- [ ] 魔法数字（未定义常量）
- [ ] 过长的参数列表（>5 个）
- [ ] 缺少文档字符串

## P2 - 提示（可优化）

### 最佳实践
- [ ] 可使用标准库替代自定义实现
- [ ] 可使用更 Pythonic 的写法
- [ ] 可添加单元测试
- [ ] 可添加类型提示
```

## 变体：领域专用 Reviewer

### 安全审计

```markdown
references/security-checklist.md
- OWASP Top 10
- 认证授权检查
- 数据加密检查
- 日志审计检查
```

### 前端设计审查

```markdown
references/design-checklist.md
- 响应式布局
- 无障碍访问（a11y）
- 颜色对比度
- 交互反馈
- 加载状态处理
```

### EDA 代码审查

```markdown
references/rtl-checklist.md
- 可综合性检查
- 时序约束
- 复位策略
- 时钟域交叉
- 面积优化建议
```

## 输出示例

```markdown
### 📊 总览
- **功能**：用户登录验证，包含密码哈希和 JWT 生成
- **整体质量**：核心逻辑正确，但存在 2 个安全风险

### 🚨 错误（必须修复）
1. **第 15 行** - 硬编码 JWT_SECRET
   - 风险：密钥泄露导致 Token 可伪造
   - 修复：从环境变量读取 `os.environ.get("JWT_SECRET")`

2. **第 28 行** - 裸 except 捕获所有异常
   - 风险：掩盖真实错误，难以调试
   - 修复：明确捕获具体异常类型 `except AuthenticationError:`

### ⚠️ 警告（建议修复）
1. **第 10 行** - 函数 65 行，建议拆分
2. **第 33 行** - 缺少类型注解

### 📈 评分
**6/10 分** - 功能可用但有严重安全隐患

### 🎯 Top 3 建议
1. 立即移除硬编码密钥（安全风险）
2. 添加输入验证和参数校验
3. 拆分函数为 validate_user() + generate_token()
```

## 优缺点

| 优点 | 缺点 |
|-----|------|
| 检查清单可独立更新 | 清单设计需要领域专家 |
| 可复用（换清单=换场景） | 可能产生大量低价值提示 |
| 输出结构化，易自动化处理 | 严重度分级可能主观 |

## 自动化扩展

### 与 CI 集成

```bash
# 评审输出 JSON 格式，供 CI 解析
{
  "score": 6,
  "errors": [...],
  "warnings": [...],
  "info": [...]
}
```

### 与 LLM-as-a-judge 集成

```markdown
## Step 5: 二次验证
将评审结果发送给另一个 LLM 实例：
"请评估以上评审是否合理，是否有遗漏或误判？"
```

---

## 检查清单

- [ ] `references/checklist.md` 存在且分类清晰
- [ ] 严重度分级明确（error/warning/info）
- [ ] SKILL.md 要求理解代码意图后再评审
- [ ] 输出格式结构化
- [ ] 有评分机制和 Top 建议
