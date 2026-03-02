#!/usr/bin/env python3
"""
A股资讯数据查询脚本 - QGData Pro版本
基于qgdata API提供专业的A股分钟级数据查询服务
"""

import argparse
import json
import os
import sys

# 添加虚拟环境路径
import os; qgdata_path = os.path.expanduser("~/china-stock-skill/qgdata_env/lib/python3.11/site-packages"); sys.path.insert(0, qgdata_path)

try:
    import qgdata as ts
except ImportError:
    print("错误: 未找到qgdata包", file=sys.stderr)
    print("请确保qgdata已正确安装", file=sys.stderr)
    sys.exit(1)

def load_token() -> str:
    """加载API token"""
    # 优先从环境变量获取
    token = os.environ.get("QGDATA_TOKEN")
    if token:
        return token.strip()

    # 从.env文件获取
    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith("QGDATA_TOKEN="):
                        token = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                        if token:
                            return token
        except Exception:
            pass

    return "Kj9mN2xP5qR8vL3tY7wZ1aB4cD6eF8gH9nX4pL2qR7sT5vY8wZ1aB3cD6eF0gH2i"  # 默认token

def get_minute_data(symbol: str, freq: str = "5min", start_date: str = None,
                   fields: str = None, limit: int = 500) -> dict:
    """获取分钟级K线数据"""
    try:
        token = load_token()
        ts.set_token(token)
        pro = ts.pro_api(timeout=30.0)

        if fields is None:
            fields = "ts_code,trade_time,open,close,high,low,vol,amount"

        df = pro.stk_mins(
            ts_code=symbol,
            freq=freq,
            start_date=start_date,
            fields=fields,
            limit=limit,
        )

        return {
            "symbol": symbol,
            "freq": freq,
            "start_date": start_date,
            "data": df.to_dict('records') if not df.empty else [],
            "total": len(df),
            "fields": fields.split(','),
            "provider": "qgdata"
        }

    except Exception as e:
        return {
            "error": f"获取分钟数据失败: {str(e)}",
            "symbol": symbol,
            "freq": freq,
            "provider": "qgdata"
        }

def main():
    parser = argparse.ArgumentParser(description="QGData A股数据查询工具")
    parser.add_argument("--symbol", required=True, help="股票代码，如 000001.SZ")
    parser.add_argument("--freq", default="5min",
                       choices=["1min", "5min", "15min", "30min", "60min"],
                       help="K线频率 (默认: 5min)")
    parser.add_argument("--start-date", help="开始日期，如 20260227")
    parser.add_argument("--fields", help="查询字段，用逗号分隔")
    parser.add_argument("--limit", type=int, default=500, help="结果数量限制")
    parser.add_argument("--format", default="json", choices=["json", "dataframe"], help="输出格式")

    args = parser.parse_args()

    result = get_minute_data(
        symbol=args.symbol,
        freq=args.freq,
        start_date=args.start_date,
        fields=args.fields,
        limit=args.limit
    )

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "dataframe":
        if result.get("data"):
            import pandas as pd
            df = pd.DataFrame(result["data"])
            print(df.to_string())
        else:
            print("无数据可显示")

if __name__ == "__main__":
    main()
