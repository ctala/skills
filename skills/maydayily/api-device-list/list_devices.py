#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备列表查询脚本

调用 ai-open-gateway 的 POST /api/device/list 接口，
获取当前用户绑定的所有设备信息。

API_KEY 获取优先级：
  1. 环境变量 AI_GATEWAY_API_KEY
  2. 配置文件 ~/.openclaw/.env 中的 AI_GATEWAY_API_KEY
  3. 命令行参数 --api-key

依赖：需要安装第三方包 httpx。请求时忽略 HTTPS 证书校验。
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import httpx
except ImportError:
    print("❌ 缺少依赖 httpx，请先安装：python3 -m pip install httpx", file=sys.stderr)
    sys.exit(1)

# 网关地址
API_HOST = "https://ai-open-gateway.closeli.cn"


def load_env_file():
    """从 ~/.openclaw/.env 文件加载环境变量配置"""
    env_path = Path.home() / ".openclaw" / ".env"
    if not env_path.exists():
        return {}
    result = {}
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    result[key] = value
    except Exception as e:
        print(f"⚠️ 读取配置文件 {env_path} 失败: {e}", file=sys.stderr)
    return result


def get_api_key(cli_key=None):
    """
    三级优先级获取 API_KEY：
      1. 环境变量 AI_GATEWAY_API_KEY
      2. ~/.openclaw/.env 配置文件
      3. 命令行参数 --api-key
    """
    # 1. 环境变量
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if key:
        return key

    # 2. 配置文件
    env_vars = load_env_file()
    key = env_vars.get("AI_GATEWAY_API_KEY")
    if key:
        return key

    # 3. 命令行参数
    if cli_key:
        return cli_key

    return None


def call_device_list(api_key):
    """调用设备列表接口"""
    url = f"{API_HOST}/api/device/list"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        with httpx.Client(verify=False, timeout=120.0, headers=headers) as client:
            resp = client.post(url, content=b"")
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP 错误 {e.response.status_code}: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"❌ 网络错误: {e}", file=sys.stderr)
        print(f"   请确认网关服务 {API_HOST} 是否已启动", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询设备列表")
    parser.add_argument("--api-key", help="API Key（优先级最低，建议用环境变量）")
    args = parser.parse_args()

    # 1. 获取 API_KEY
    api_key = get_api_key(cli_key=args.api_key)
    if not api_key:
        print("❌ 未找到 AI_GATEWAY_API_KEY，请通过以下任一方式配置：", file=sys.stderr)
        print("   1. 环境变量: export AI_GATEWAY_API_KEY=\"your_key\"", file=sys.stderr)
        print("   2. 配置文件: ~/.openclaw/.env 中添加 AI_GATEWAY_API_KEY=your_key", file=sys.stderr)
        print("   3. 命令行:   --api-key your_key", file=sys.stderr)
        sys.exit(1)

    # 2. 调用接口
    result = call_device_list(api_key)

    # 3. 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
