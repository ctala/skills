# Todo List Skill 发布清单

## ✅ 已完成项

### 1. 移除私人信息
- [x] 移除硬编码的对话 ID (`user:ou_bb5ebf5cd5589747a734d299cfbd9096`)
- [x] 检查并移除所有个人信息（姓名、邮箱等）
- [x] 清理 Python 缓存文件

### 2. 实现动态会话配置
- [x] 修改 `todo.py` - 移除 `USER_CHAT_ID` 常量
- [x] 修改 `merge-reminders.py` - 移除 `USER_CHAT_ID` 常量
- [x] 实现 `load_session_context()` 从配置文件读取
- [x] 修改 `create_cron_job()` 接受 channel 和 target 参数
- [x] 修改 `cmd_send_status()` 和 `cmd_send_list()` 支持参数传递
- [x] 添加友好的错误提示（缺少会话配置时）

### 3. 更新文档
- [x] 更新 `SKILL.md` 移除硬编码 ID 示例
- [x] 添加会话信息获取说明
- [x] 更新命令示例为参数化形式

## 📋 发布信息

- **Slug**: `todo-list`
- **Name**: `Todo List 待办事项管理`
- **Version**: `1.0.0`
- **Changelog**: `首次发布：支持待办事项管理、标签系统、项目管理、附件功能、自动提醒`

## 🎯 核心功能

1. **待办事项管理**
   - 添加、查看、完成、删除待办
   - 支持优先级（高/中/低）
   - 支持截止时间设置

2. **标签系统**
   - 自动提取 #标签
   - 按标签筛选任务
   - 标签统计

3. **项目管理**
   - 将标签升级为项目
   - 项目进度追踪
   - 项目详情查看

4. **附件功能**
   - 为任务添加附件
   - 附件文件管理

5. **自动提醒**
   - 合并相近时间的任务提醒
   - 多次提醒（30分钟前、15分钟前、准点）
   - 支持 OpenClaw cron 集成

6. **会话管理**
   - 动态获取会话信息
   - 配置文件持久化
   - 跨平台支持（feishu、discord 等）

## 📁 文件结构

```
todo-list/
├── SKILL.md                 # 技能说明文档
├── TODO-REFERENCE.md        # 完整参考文档
├── README.md                # 简要说明
├── PUBLISH_CHECKLIST.md     # 发布清单（本文件）
└── scripts/
    ├── todo.py              # 主脚本
    ├── merge-reminders.py   # 提醒合并工具
    └── reminder.py          # 提醒检查脚本
```

## 🚀 发布命令

```bash
clawhub publish ~/.openclaw/workspace/skills/todo-list \
  --slug todo-list \
  --name "Todo List 待办事项管理" \
  --version 1.0.0 \
  --changelog "首次发布：支持待办事项管理、标签系统、项目管理、附件功能、自动提醒"
```

## ⚠️ 注意事项

1. **首次使用要求**：Agent 需要从会话上下文获取 `channel` 和 `target` 信息
2. **数据存储**：所有数据存储在 `~/.openclaw/workspace/memory/` 目录
3. **依赖**：需要 Python 3 和 OpenClaw CLI

---

*准备发布时间：2026-03-14*
