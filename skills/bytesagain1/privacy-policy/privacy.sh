#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  generate) cat << 'PROMPT'
You are an expert. Help with: 生成隐私政策. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  gdpr) cat << 'PROMPT'
You are an expert. Help with: GDPR合规版. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  ccpa) cat << 'PROMPT'
You are an expert. Help with: CCPA合规版. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  app) cat << 'PROMPT'
You are an expert. Help with: App隐私政策. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  website) cat << 'PROMPT'
You are an expert. Help with: 网站隐私政策. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  audit) cat << 'PROMPT'
You are an expert. Help with: 合规审计. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Privacy Policy Generator — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  generate        生成隐私政策
  gdpr            GDPR合规版
  ccpa            CCPA合规版
  app             App隐私政策
  website         网站隐私政策
  audit           合规审计

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
