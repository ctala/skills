#!/usr/bin/env python3
"""
Sensitive Data Masker - OpenClaw Hook Wrapper
"""

import sys
import json
from pathlib import Path

# 导入脱敏器
sys.path.insert(0, str(Path(__file__).parent))
from sensitive_masker import ChannelSensitiveMasker

def mask_message(content: str) -> dict:
    """脱敏消息内容。"""
    masker = ChannelSensitiveMasker()
    masked_text, replacements = masker.mask_message(content)
    
    return {
        "masked": masked_text,
        "count": len(replacements),
        "types": list(set([r['type'] for r in replacements]))
    }

def restore_message(masked_content: str) -> str:
    """还原消息中的敏感数据。"""
    masker = ChannelSensitiveMasker()
    return masker.restore_message(masked_content)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"用法：{sys.argv[0]} <command> <content>")
        print("命令:")
        print("  mask <content>    - 脱敏消息")
        print("  restore <content> - 还原消息")
        sys.exit(1)
    
    command = sys.argv[1]
    content = ' '.join(sys.argv[2:])
    
    if command == 'mask':
        result = mask_message(content)
        print(json.dumps(result, ensure_ascii=False))
    elif command == 'restore':
        restored = restore_message(content)
        print(restored)
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
