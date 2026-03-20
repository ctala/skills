# Pattern 1: Tool Wrapper（工具包装器）

## 核心作用

给 Agent 注入特定库/框架的专业知识，**按需加载**，不占用日常对话的 context。

## 适用场景

- 团队内部编码规范
- 框架最佳实践（FastAPI/React/Verilog）
- API 使用约定
- 领域特定术语表

## 目录结构

```
skills/api-expert/
├── SKILL.md
└── references/
    └── conventions.md
```

## SKILL.md 模板

```markdown
---
name: api-expert
description: FastAPI 开发最佳实践。当用户构建、审查或调试 FastAPI 应用、REST API 或 Pydantic 模型时激活。
metadata:
  pattern: tool-wrapper
  domain: fastapi
  trigger-keywords: [fastapi, pydantic, REST API, endpoint, dependency injection]
---

你是 FastAPI 开发专家。将以下规范应用于用户的代码或问题。

## 核心规范

当用户请求涉及 FastAPI 时，**必须**加载 `references/conventions.md` 获取完整规范列表。

## 审查代码时
1. 加载规范文件
2. 逐条检查用户代码是否符合规范
3. 每个违规点：引用具体规则 + 给出修复建议

## 编写代码时
1. 加载规范文件
2. 严格遵守每条规范
3. 所有函数签名添加类型注解
4. 依赖注入使用 Annotated 风格

## 示例输出格式

```python
# ❌ 错误示例
@app.get("/users")
def get_users():
    return db.query(User).all()

# ✅ 正确示例
@app.get("/users", response_model=list[UserSchema])
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[UserSchema]:
    result = await db.execute(select(User))
    return result.scalars().all()
```
```

## references/conventions.md 模板

```markdown
# FastAPI 团队规范 v1.0

## 1. 项目结构
- 使用 `src/` 布局
- 路由按功能模块拆分：`routes/users.py`, `routes/items.py`
- Schema 定义在 `schemas/` 目录

## 2. 异步规范
- 所有 I/O 操作必须 async/await
- 数据库会话使用 AsyncSession
- 禁止在 async 函数中调用同步阻塞方法

## 3. 错误处理
- 使用 HTTPException 抛出标准状态码
- 自定义异常处理器在 `exceptions.py` 统一注册
- 错误响应包含：`detail`, `error_code`, `timestamp`

## 4. 依赖注入
- 数据库连接、认证、日志等全部走 Depends()
- 依赖函数命名：`get_xxx()`
- 使用 Annotated[Type, Depends(func)] 风格

## 5. Pydantic 模型
- 所有请求/响应必须用 Schema 包装
- 禁止直接返回 ORM 对象
- 使用 model_config = ConfigDict(from_attributes=True)

## 6. 测试规范
- 使用 pytest + httpx.TestClient
- 每个 endpoint 至少一个测试
- Mock 外部依赖，不依赖真实数据库
```

## 激活条件设计

在 `description` 中明确触发关键词：

```yaml
description: >
  FastAPI 开发最佳实践。
  激活词：fastapi, pydantic, REST API, endpoint, dependency injection,
  路由，schema, Depends, HTTPException, async
```

## 优缺点

| 优点 | 缺点 |
|-----|------|
| 按需加载，节省 token | 依赖关键词匹配准确性 |
| 规范独立维护，易更新 | 多个 Tool Wrapper 可能冲突 |
| 可组合（同时激活多个） | 需要明确的触发词设计 |

## 变体

### 变体 A：多规范切换

```markdown
根据用户提到的技术栈加载对应规范：
- FastAPI → `references/fastapi-conventions.md`
- Django → `references/django-conventions.md`
- Flask → `references/flask-conventions.md`
```

### 变体 B：团队专属规范

```markdown
你是 [公司名] 后端开发助手。
**必须**优先遵循 `references/team-conventions.md` 中的内部规范，
其次参考通用最佳实践。
```

---

## 检查清单

- [ ] `description` 包含明确的触发关键词
- [ ] `references/` 目录存在且内容具体
- [ ] SKILL.md 明确说明何时加载规范
- [ ] 有正误对比示例
- [ ] 规范可独立更新，无需改 SKILL.md
