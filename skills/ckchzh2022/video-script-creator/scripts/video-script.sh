#!/usr/bin/env bash
# video-script-creator - 短视频脚本生成器
# 支持抖音/快手/YouTube Shorts/B站

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

COMMAND="${1:-help}"
shift 2>/dev/null || true

case "$COMMAND" in
  script|hook|title|outline|cta|trending|help)
    python3 "$SCRIPT_DIR/_engine.py" "$COMMAND" "$@"
    ;;
  *)
    echo "❌ 未知命令: $COMMAND"
    echo "运行 'video-script.sh help' 查看帮助"
    exit 1
    ;;
esac
