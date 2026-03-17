# weixin-webhook

企业微信 webhook 消息发送，一行命令搞定。

如何在微信中接收openclaw消息(企业微信法):

1. 在企业微信创建一个组织
2. 在企业微信管理后台, 我的企业中开启微信插件
3. 用微信扫码关注并绑定企业, 开启接收企业微信openclaw消息

## 快速使用

```bash
# 发送文本消息
~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh "webhook_key" "text" "消息内容"

# 发送 Markdown 消息
~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh "webhook_key" "markdown" "**重要** <font color=\"warning\">提醒</font>"

# @人员
~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh "key" "text" "会议提醒" "zhangsan,lisi" "13800001111"
```

## 参数说明

| 位置 | 说明 |
|------|------|
| 1 | webhook_key |
| 2 | msgtype (text/markdown) |
| 3 | 消息内容 |
| 4 | @用户userid列表 (逗号分隔，可选) |
| 5 | @用户手机号列表 (逗号分隔，可选) |

## 设置定时任务

```bash
# 每天14:00发送提醒
openclaw cron add \
  --cron "0 14 * * *" \
  --agent main \
  --message "执行：~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh 'd624f026-9fc6-4f45-9b7f-0a7b9d5bc0cc' 'text' '【健康提醒】请做提肛运动！' 'liujie'" \
  --name "daily_kegel" \
  --description "每日提肛提醒"

# 每天9:00团队通知
openclaw cron add \
  --cron "0 9 * * *" \
  --agent main \
  --message "执行：~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh 'your_key' 'text' '晨会即将开始，请准时参加' '@all'" \
  --name "morning_meeting" \
  --description "晨会通知"

# 每日汇报提醒 (Markdown格式)
openclaw cron add \
  --cron "0 17 * * *" \
  --agent main \
  --message "执行：~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh 'your_key' 'markdown' '【日报提醒】请在18:00前提交日报。<font color=\"info\">1. 今日完成</font><font color=\"info\">2. 遇到问题</font><font color=\"info\">3. 明日计划</font>'" \
  --name "daily_report" \
  --description "日报提醒"
```

## 管理任务

```bash
openclaw cron list                    # 查看所有任务
openclaw cron run daily_kegel         # 手动执行测试
openclaw cron disable daily_kegel     # 禁用
openclaw cron enable daily_kegel      # 启用
openclaw cron rm daily_kegel          # 删除
```

## 获取 Webhook

### 步骤

1. **打开企业微信** → 进入群聊

2. **添加群机器人**
   - 点击群设置 (右上角三个点)
   - 选择「消息推送」
   - 添加消息推送

3. **获取 Webhook 地址**
   - 复制生成的 Webhook URL
   - 格式: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx-xxxxx`

### 注意事项

- 不要分享 Webhook URL 给他人
- 泄露后可删除推送重建

## 消息格式示例

### 文本

```json
{
  "msgtype": "text",
  "text": {
    "content": "会议提醒",
    "mentioned_list": ["zhangsan", "@all"],
    "mentioned_mobile_list": ["13800001111", "@all"]
  }
}
```

### Markdown

```json
{
  "msgtype": "markdown",
  "markdown": {
    "content": "实时新增<font color=\"warning\">132例</font>\n>普通用户:<font color=\"comment\">117例</font>\n>VIP用户:<font color=\"comment\">15例</font>"
  }
}
```

## 文件结构

```
weixin-webhook/
├── SKILL.md       # 本文档
└── send_weixin.sh # 发送脚本
```

## 依赖

- `curl` (系统自带)