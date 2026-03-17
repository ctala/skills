#!/bin/bash
# 企业微信消息发送 - 极简版
# 用法: ./send_weixin.sh <webhook_key> <msgtype> <content> [mentioned_list] [mentioned_mobile_list]

set -e

WEBHOOK_KEY="$1"
MSGTYPE="$2"
CONTENT="$3"
MENTIONED_LIST="${4:-}"
MENTIONED_MOBILE_LIST="${5:-}"

if [ -z "$WEBHOOK_KEY" ] || [ -z "$MSGTYPE" ] || [ -z "$CONTENT" ]; then
    echo "用法: $0 <webhook_key> <msgtype> <content> [mentioned_list] [mentioned_mobile_list]"
    echo "示例: $0 'key' 'text' '消息内容' 'user1,user2' '13800001111,@all'"
    exit 1
fi

# 构建JSON
case "$MSGTYPE" in
    text)
        JSON_DATA='{"msgtype":"text","text":{"content":"'"$CONTENT"'"}}'
        if [ -n "$MENTIONED_LIST" ]; then
            JSON_DATA=$(echo "$JSON_DATA" | sed 's/}$/, "mentioned_list":['"$MENTIONED_LIST"']}/' | sed 's/\([a-zA-Z0-9_-]\+\)/"\1"/g')
        fi
        if [ -n "$MENTIONED_MOBILE_LIST" ]; then
            JSON_DATA=$(echo "$JSON_DATA" | sed 's/}$/, "mentioned_mobile_list":['"$MENTIONED_MOBILE_LIST"']}/' | sed 's/\([a-zA-Z0-9_-]\+\)/"\1"/g')
        fi
        ;;
    markdown)
        JSON_DATA='{"msgtype":"markdown","markdown":{"content":"'"$CONTENT"'"}}'
        ;;
    *)
        echo "不支持的消息类型: $MSGTYPE"
        exit 1
        ;;
esac

# 发送
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$WEBHOOK_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA"
