# Pattern 5: Pipeline（流水线）

## 核心作用

强制**多步骤顺序执行**，带检查点（checkpoint），防止跳过关键步骤。

## 适用场景

- 文档生成（解析→生成→组装→质检）
- 代码迁移/重构
- 数据转换流程
- 多阶段处理任务

## 目录结构

```
skills/doc-pipeline/
├── SKILL.md
├── references/
│   ├── docstring-style.md    # Step 2 使用
│   └── quality-checklist.md  # Step 4 使用
└── assets/
    └── api-doc-template.md   # Step 3 使用
```

## SKILL.md 模板

```markdown
---
name: doc-pipeline
description: 通过多步骤流水线从 Python 源码生成 API 文档。当用户要求文档化模块、生成 API 文档或从代码创建文档时激活。
metadata:
  pattern: pipeline
  steps: 4
  trigger-phrases: [生成文档，document this, create API docs, 文档化]
---

你正在运行文档生成流水线。**严格按顺序执行每个步骤，禁止跳过**。

## ⛔ 全局规则
- **禁止**跳过任何步骤
- **禁止**在步骤失败时继续
- **禁止**在未获用户确认时进入下一步（如有检查点）
- 每步完成后，向用户展示结果并说明下一步

---

## Step 1 — 解析与清单生成

**任务**：分析用户 Python 代码，提取所有公共类、函数、常量

**输出**：
```
检测到以下公共 API：
- [ ] class UserManager
- [ ] def authenticate_user()
- [ ] def create_session()
- [ ] const MAX_RETRY = 3

请确认：这是你要文档化的完整公共 API 吗？
有需要添加或排除的吗？
```

**检查点**：⏸️ 等待用户确认

---

## Step 2 — 生成 Docstring

**任务**：为每个缺少文档的函数生成 docstring

**前置条件**：加载 `references/docstring-style.md`

**执行**：
对每个函数：
1. 按风格指南生成 docstring
2. 包含：参数说明、返回值、异常、示例

**输出**：
```
为以下函数生成了 docstring：

### authenticate_user()
```python
def authenticate_user(username: str, password: str) -> User:
    """验证用户凭据并返回用户对象。
    
    Args:
        username: 用户名（邮箱格式）
        password: 用户密码（明文）
    
    Returns:
        User: 验证成功的用户对象
    
    Raises:
        AuthenticationError: 凭据无效时
    
    Example:
        >>> user = authenticate_user("a@example.com", "pass123")
    """
```

**检查点**：⏸️ 问用户："这些 docstring 是否符合预期？需要调整吗？"

---

## Step 3 — 组装文档

**前置条件**：用户确认 Step 2

**任务**：加载 `assets/api-doc-template.md`，编译完整文档

**输出**：完整的 API 参考文档（Markdown 格式）

---

## Step 4 — 质量检查

**任务**：对照 `references/quality-checklist.md` 自检

**检查项**：
- [ ] 每个公共符号都有文档
- [ ] 每个参数有类型和说明
- [ ] 每个函数至少有 1 个使用示例
- [ ] 无拼写错误
- [ ] 格式一致

**输出**：
```
质量检查结果：
✅ 所有检查通过

或

⚠️ 发现 2 个问题：
1. create_session() 缺少示例
2. 拼写错误：第 35 行 "authentcate" → "authenticate"

已自动修复，请确认。
```

**检查点**：⏸️ 等待用户确认

---

## Step 5 — 最终交付

呈现完整文档，问：
"文档已完成！需要导出为其他格式（PDF/HTML）或做其他调整吗？"
```

## references/docstring-style.md 模板

```markdown
# Docstring 风格指南

## 格式规范
- 使用 Google 风格
- 第一行：一句话总结（以动词开头）
- 空行后：详细描述（可选）
- Args/Returns/Raises/Example 章节

## 示例
```python
def process_data(data: list[dict], threshold: float = 0.5) -> dict:
    """处理原始数据并返回聚合结果。
    
    对输入数据进行过滤、转换和聚合操作。
    
    Args:
        data: 原始数据列表，每个元素为字典
        threshold: 过滤阈值，范围 0-1，默认 0.5
    
    Returns:
        包含以下键的字典：
        - total_count: 处理的数据总数
        - filtered_count: 过滤后的数量
        - aggregated: 聚合结果
    
    Raises:
        ValueError: 数据格式无效或阈值超出范围
    
    Example:
        >>> result = process_data([{"value": 1}, {"value": 2}], 0.3)
        >>> result["total_count"]
        2
    """
```

## 禁用内容
- 不使用 "这个函数..." 开头
- 不重复函数名已表达的信息
- 不使用模糊词汇（"可能"、"也许"）
```

## references/quality-checklist.md 模板

```markdown
# 文档质量检查清单

## 完整性
- [ ] 所有公共类、函数、常量都有文档
- [ ] 所有参数有类型注解和说明
- [ ] 所有返回值有说明
- [ ] 所有异常有说明

## 准确性
- [ ] 示例代码可执行
- [ ] 参数说明与实际用途一致
- [ ] 无过时信息

## 可读性
- [ ] 无拼写错误
- [ ] 格式一致
- [ ] 术语一致

## 实用性
- [ ] 每个函数至少有 1 个示例
- [ ] 复杂逻辑有解释
- [ ] 有使用场景说明
```

## 变体：自动化 Pipeline

无需用户确认的自动流程：

```markdown
## 自动模式

Step 1 → Step 2 → Step 3 → Step 4 → 输出

每步完成后自动进入下一步，最终一次性输出结果。
适用于信任度高、容错率低的场景。
```

## 变体：条件分支 Pipeline

```markdown
## Step 2 — 条件处理

如代码是 Python → 生成 Google 风格 docstring
如代码是 JavaScript → 生成 JSDoc 注释
如代码是 Verilog → 生成注释头
```

## 优缺点

| 优点 | 缺点 |
|-----|------|
| 流程可控，质量稳定 | 步骤多，耗时长 |
| 每步可独立验证 | 用户需多次确认 |
| 易于定位问题步骤 | 流程僵化，难灵活调整 |

## 与 Reviewer 组合

```markdown
## Pipeline + Reviewer

Step 1: 解析
Step 2: 生成
Step 3: 组装
Step 4: Reviewer 评审（加载 checklist 打分）
Step 5: 如评分<8，返回 Step 2 重新生成
Step 6: 交付
```

## 检查清单

- [ ] 步骤顺序明确
- [ ] 每步有清晰输入/输出
- [ ] 检查点明确标注（⏸️）
- [ ] 有失败处理逻辑
- [ ] 按需加载 references/assets
- [ ] 最终输出格式明确

---

## 模式对比总结

| 模式 | 核心特征 | 最佳场景 |
|-----|---------|---------|
| Tool Wrapper | 按需加载知识 | 框架规范/团队约定 |
| Generator | 模板填充 | 文档/报告生成 |
| Reviewer | 检查清单评审 | Code Review/审计 |
| Inversion | 先采访再执行 | 需求模糊的任务 |
| Pipeline | 多步骤 + 检查点 | 复杂转换流程 |
