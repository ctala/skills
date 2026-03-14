# Todo List 待办事项管理技能

## 功能特性
- ✅ 添加待办事项，支持优先级和到期时间设置
- ✅ 查看待办列表，支持按状态和优先级筛选
- ✅ 标记任务完成
- ✅ 删除任务
- ✅ 查看任务详情
- ✅ 自动到期提醒

## 安装使用
1. 将技能目录放置到 `~/.openclaw/workspace/skills/`
2. 可以通过命令行直接使用：
   ```bash
   # 添加任务
   ~/.openclaw/workspace/skills/todo-list/scripts/todo.py add "任务标题" --priority high --due "2026-03-09 18:00"
   
   # 查看待办
   ~/.openclaw/workspace/skills/todo-list/scripts/todo.py list
   
   # 标记完成
   ~/.openclaw/workspace/skills/todo-list/scripts/todo.py done <任务ID>
   
   # 删除任务
   ~/.openclaw/workspace/skills/todo-list/scripts/todo.py delete <任务ID>
   ```

## 定时提醒配置
添加cron任务实现自动提醒：
```bash
# 每小时检查一次到期任务
0 * * * * ~/.openclaw/workspace/skills/todo-list/scripts/reminder.py

# 每天上午9点检查今日到期任务
0 9 * * * ~/.openclaw/workspace/skills/todo-list/scripts/todo.py list --status pending
```

## 数据存储
所有待办事项存储在 `~/.openclaw/workspace/memory/todo.json` 文件中