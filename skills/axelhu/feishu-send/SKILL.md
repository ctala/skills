---
name: feishu-send
version: 1.0.0
description: 飞书文件/图片/语音发送技能。使用 curl 调用飞书 API 发送本地文件、图片、语音到飞书群或个人。触发时机：需要发送文件到飞书时。
---

# Feishu Send

飞书文件/图片/语音发送技能。

## 概述

OpenClaw 的 `message` 工具在飞书上发送图片/文件时有 bug：
- filePath 参数 → 飞书收到的是路径文本
- media 参数 + 本地路径 → 可能失败

**正确方法**：用 exec 工具执行 curl 调用飞书 API。

## 敏感信息

飞书配置信息存储在 AGENTS.md 或 MEMORY.md 中：
- APP_ID
- APP_SECRET  
- 飞书群 ID

Skill 中使用占位符，运行时从上下文读取。

## 核心流程

### 通用流程（三步）

1. **获取 token**：从 openclaw.json 读取 appSecret，获取 tenant_access_token
2. **上传文件**：上传本地文件获取 file_key / image_key
3. **发送消息**：调用消息 API 发送

---

## 发送图片

### 步骤

```bash
# Step 1: 获取 token
APP_SECRET=$(python3 -c "import json; c=json.load(open('/home/axelhu/.openclaw/openclaw.json')); print(c['channels']['feishu']['accounts']['main']['appSecret'])")

TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"cli_a92389c631f81cba","app_secret":"'$APP_SECRET'"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# Step 2: 上传图片获取 image_key
IMAGE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/images' \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/path/to/image.png" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['image_key'])")

# Step 3: 发送图片到群
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"<飞书群ID>","msg_type":"image","content":"{\"image_key\":\"'$IMAGE_KEY'\"}"}'
```

### 支持格式
- JPEG, PNG, WEBP, GIF, TIFF, BMP, ICO

---

## 发送文件

### 步骤

```bash
# Step 1: 获取 token（同上）

# Step 2: 上传文件获取 file_key
FILE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=stream" \
  -F "file_name=xxx.zip" \
  -F "file=@/path/to/file.zip" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")

# Step 3: 发送文件到群
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"<飞书群ID>","msg_type":"file","content":"{\"file_key\":\"'$FILE_KEY'\"}"}'
```

---

## 发送语音

### 步骤

```bash
# Step 1: 获取 token（同上）

# Step 2: 上传 opus 文件获取 file_key
FILE_KEY=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=xxx.opus" \
  -F "file=@/path/to/audio.opus" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")

# Step 3: 发送语音（需要提供 duration 秒数）
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"<飞书群ID>","msg_type":"audio","content":"{\"file_key\":\"'$FILE_KEY'\",\"duration\":5}"}'
```

---

## 常见问题

### 1. image_key 获取失败
- 检查文件路径是否正确
- 检查文件格式是否支持
- 检查 token 是否过期

### 2. 发送失败
- 确认 receive_id 正确（群用 chat_id，个人用 open_id）
- 检查消息内容 JSON 格式是否正确

### 3. token 获取失败
- 确认 APP_ID 和 APP_SECRET 正确
- 确认飞书应用有 im:message 权限

---

## 触发时机

- 用户要求发送图片/文件/语音时
- 需要发送本地文件到飞书时
