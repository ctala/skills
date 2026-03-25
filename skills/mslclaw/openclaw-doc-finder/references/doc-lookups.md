# Doc Lookups — 已查阅文档问题速查

> 每次使用 openclaw-doc-finder 技能查询官方文档后，将问题与结论记录于此，形成已有问题快速参考。

---

## 目录

- [Exec 审批与白名单](#exec-审批与白名单)
- [配置相关](#配置相关)

---

## Exec 审批与白名单

### exec-approvals.json 的正确配置格式

**问题**：如何正确配置 exec 命令白名单，实现「常用命令免审批，新命令弹一次审批后永久放行」？

**官方文档结论**：
- `~/.openclaw/exec-approvals.json` 是 exec 审批的**唯一正确配置位置**
- `openclaw.json` 中 **不存在** `security.exec.allowlist` 这个字段（之前配置错误）
- `ask` 三个取值：
  - `"off"` — 不弹审批，不在白名单直接拒绝（**太严，不推荐**）
  - `"on-miss"` — 不在白名单才弹审批，点 Always Allow 后加入白名单（**正确做法**）
  - `"always"` — 每次都弹审批
- `askFallback`：无法弹审批时的 fallback 行为，默认 deny
- 白名单条目使用**二进制文件的绝对路径**（如 `/usr/bin/ls`），不是命令名

**正确配置**：
```json
{
  "defaults": {
    "security": "allowlist",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": true
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "pattern": "/usr/bin/ls",
          "lastResolvedPath": "/usr/bin/ls"
        }
      ]
    }
  }
}
```

**相关文档**：`tools/exec-approvals.md`

**查阅时间**：2026-03-25

---

### Discord 审批按钮显示 "allow once" 但实际已执行 Always Allow

**问题**：点击 "Always Allow" 按钮后，Discord 确认消息仍显示 "allow once"，是否真的执行了 Always Allow？

**官方文档结论**：
- 这是 OpenClaw Discord 组件的**显示 Bug**，确认消息文案硬编码为 "allow once"
- 实际行为：**Always Allow 已正确执行**，只是确认消息显示错误
- "Always Allow" 效果：将该命令的绝对路径加入 `exec-approvals.json` 的 `allowlist`，下次同名命令直接放行

**查阅时间**：2026-03-25

---

## 配置相关

### openclaw.json 顶层字段列表

**问题**：openclaw.json 有哪些顶层配置字段？

**结论**：
```
meta, env, wizard, update, browser, auth, models, agents, tools, messages, commands, session, cron, channels, gateway, memory, skills, plugins
```

**注意**：`security` 不是顶层字段（不在列表中）

**查阅时间**：2026-03-24

---

<!-- 新条目追加在下方，保持按分类整理 -->

---

## 如何追加新条目

在对应分类下按以下格式追加：

```markdown
### 标题（简洁描述问题）

**问题**：xxx？

**官方文档结论**：
- 结论1
- 结论2

**相关文档**：`path/to/doc.md`

**查阅时间**：YYYY-MM-DD
```
