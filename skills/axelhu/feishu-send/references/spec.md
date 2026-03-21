# Feishu Send 快速参考

## 快速调用

```bash
# 发送图片
/path/to/scripts/feishu-send-image.sh /path/to/image.png <chat_id>

# 发送文件
/path/to/scripts/feishu-send-file.sh /path/to/file.zip <chat_id>
```

## 手动调用流程

### 1. 获取 token

```bash
APP_SECRET=$(python3 -c "import json; c=json.load(open('/home/axelhu/.openclaw/openclaw.json')); print(c['channels']['feishu']['accounts']['main']['appSecret'])")

TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"cli_a92389c631f81cba","app_secret":"'$APP_SECRET'"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")
```

### 2. 根据类型上传

| 类型 | API | 参数 |
|------|-----|------|
| 图片 | /im/v1/images | image_type=message |
| 文件 | /im/v1/files | file_type=stream |
| 语音 | /im/v1/files | file_type=opus |

### 3. 发送消息

| 类型 | msg_type | content 格式 |
|------|----------|-------------|
| 图片 | image | {"image_key": "xxx"} |
| 文件 | file | {"file_key": "xxx"} |
| 语音 | audio | {"file_key": "xxx", "duration": 5} |

## 常见错误

| 错误 | 原因 |
|------|------|
| Can't recognize image format | 文件格式不支持或损坏 |
| 401 Unauthorized | token 无效或过期 |
| no right to access | 群ID/用户ID错误 |
