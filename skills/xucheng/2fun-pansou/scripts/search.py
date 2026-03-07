#!/usr/bin/env python3
"""
2fun.live 网盘资源搜索 — 分页版

API: POST https://www.2fun.live/api/pan/search
    { kw: "关键词", res: "merge" }

限速: 10次/分钟（按IP）

Usage:
  python3 search.py "流浪地球2"                        # 第1页，全部网盘
  python3 search.py "太平年" --cloud aliyun            # 只看阿里云盘
  python3 search.py "太平年" --cloud aliyun quark      # 阿里+夸克
  python3 search.py "太平年" --page 2                  # 第2页
  python3 search.py "太平年" --page-size 5             # 每页5条
  python3 search.py "流浪地球2" --json                  # 原始JSON
"""

import sys
import json
import urllib.request
import urllib.parse
import argparse

API_URL = "https://www.2fun.live/api/pan/search"

DRIVE_PRIORITY = [
    "aliyun", "quark", "115", "baidu", "pikpak",
    "uc", "xunlei", "123", "tianyi", "mobile",
    "magnet", "ed2k", "other",
]

DRIVE_NAMES = {
    "115": "115网盘",
    "quark": "夸克网盘",
    "baidu": "百度网盘",
    "aliyun": "阿里云盘",
    "tianyi": "天翼云盘",
    "uc": "UC网盘",
    "mobile": "移动云盘",
    "pikpak": "PikPak",
    "xunlei": "迅雷云盘",
    "123": "123网盘",
    "magnet": "磁力链接",
    "ed2k": "ED2K",
    "other": "其他",
}

DRIVE_EMOJI = {
    "aliyun": "☁️",
    "quark": "⚡",
    "baidu": "🔵",
    "115": "🔷",
    "pikpak": "🟣",
    "uc": "🟠",
    "xunlei": "🌩️",
    "123": "🟢",
    "tianyi": "🔴",
    "mobile": "📱",
    "magnet": "🧲",
    "ed2k": "🔗",
    "other": "📁",
}

# 云盘筛选别名（支持中文和英文简写）
DRIVE_ALIASES = {
    "阿里": "aliyun", "阿里云盘": "aliyun", "aliyun": "aliyun",
    "夸克": "quark", "夸克网盘": "quark", "quark": "quark",
    "百度": "baidu", "百度网盘": "baidu", "baidu": "baidu",
    "115": "115", "115网盘": "115",
    "pikpak": "pikpak", "pik": "pikpak",
    "uc": "uc", "UC": "uc",
    "迅雷": "xunlei", "xunlei": "xunlei",
    "123": "123", "123网盘": "123",
    "天翼": "tianyi", "tianyi": "tianyi",
    "移动": "mobile", "mobile": "mobile",
    "磁力": "magnet", "magnet": "magnet",
    "ed2k": "ed2k",
}


def resolve_cloud(name: str) -> str:
    """将用户输入的云盘名称标准化"""
    return DRIVE_ALIASES.get(name, name)


def search(keyword: str) -> dict:
    payload = {"kw": keyword, "res": "merge"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://www.2fun.live/",
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode("utf-8"))


def flatten_results(result: dict, cloud_filter: list = None) -> list:
    """
    将 merged_by_type 扁平化为有序列表。
    按云盘优先级排列：同一云盘的结果连续分组，各云盘按 DRIVE_PRIORITY 排序。
    """
    by_type = result.get("merged_by_type", {})
    flat = []

    # 按优先级排列云盘
    ordered = [t for t in DRIVE_PRIORITY if t in by_type and by_type[t]]
    for t in by_type:
        if t not in ordered and by_type[t]:
            ordered.append(t)

    # 应用云盘筛选
    if cloud_filter:
        ordered = [t for t in ordered if t in cloud_filter]

    for drive_type in ordered:
        for lnk in by_type.get(drive_type, []):
            flat.append({
                "drive_type": drive_type,
                **lnk,
            })

    return flat


def format_page(result: dict, page: int = 1, page_size: int = 8,
                cloud_filter: list = None) -> str:
    keyword = result.get("keyword", "")
    total_all = result.get("total_count", 0)
    duration = result.get("search_duration", 0)
    from_cache = result.get("from_cache", False)

    flat = flatten_results(result, cloud_filter)
    total = len(flat)

    if total == 0:
        if cloud_filter:
            names = "、".join(DRIVE_NAMES.get(t, t) for t in cloud_filter)
            return f"❌ 在 **{names}** 中未找到「{keyword}」的资源\n（全网共 {total_all} 条，可去掉筛选重试）"
        return f"❌ 未找到「{keyword}」的网盘资源"

    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    items = flat[start:end]

    cache_tag = "缓存" if from_cache else f"{duration}ms"

    # 标题行
    filter_tag = ""
    if cloud_filter:
        filter_tag = " | 筛选: " + "/".join(DRIVE_NAMES.get(t, t) for t in cloud_filter)
    lines = [
        f"🔍 **{keyword}**{filter_tag}",
        f"第 **{page}/{total_pages}** 页 · 共 {total} 条（{cache_tag}）",
        "─" * 28,
    ]

    current_drive = None
    for i, item in enumerate(items, start=start + 1):
        drive_type = item.get("drive_type", "other")
        emoji = DRIVE_EMOJI.get(drive_type, "📁")
        drive_name = DRIVE_NAMES.get(drive_type, drive_type)

        # 换云盘时显示小标题
        if drive_type != current_drive:
            if current_drive is not None:
                lines.append("")
            lines.append(f"**{emoji} {drive_name}**")
            current_drive = drive_type

        url = item.get("url", "")
        pwd = item.get("password", "")
        note = item.get("note", "")
        date = item.get("datetime", "")
        restricted = item.get("_restricted", False)

        if restricted:
            lines.append(f"  {i}. 🔒 需登录查看完整链接")
            continue

        line = f"  {i}. `{url}`"
        extras = []
        if pwd:
            extras.append(f"密码:`{pwd}`")
        if note:
            extras.append(note[:40])
        if date:
            extras.append(date[:10])
        if extras:
            line += "  " + " · ".join(extras)
        lines.append(line)

    lines.append("")
    lines.append("─" * 28)

    # 翻页提示
    nav = []
    if page > 1:
        nav.append(f"⬅️ 上一页：「第{page-1}页 {keyword}」")
    if page < total_pages:
        nav.append(f"➡️ 下一页：「第{page+1}页 {keyword}」")
    if nav:
        lines.extend(nav)

    # 云盘筛选提示
    available = [t for t in DRIVE_PRIORITY
                 if t in (result.get("merged_by_type") or {}) and result["merged_by_type"][t]]
    if available and not cloud_filter:
        drive_hints = " · ".join(
            f"{DRIVE_NAMES.get(t,t)}({len(result['merged_by_type'][t])})" for t in available
        )
        lines.append(f"📂 筛选云盘: {drive_hints}")
        lines.append("  说「阿里 {关键词}」即可筛选")

    q = urllib.parse.quote(keyword)
    lines.append(f"🌐 <https://s.2fun.live/search?q={q}>")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="2fun.live 网盘资源搜索（分页版）")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("--cloud", nargs="+", default=None,
                        help="筛选云盘类型（可多选）: aliyun quark baidu 115 magnet ...")
    parser.add_argument("--page", type=int, default=1, help="页码（默认第1页）")
    parser.add_argument("--page-size", type=int, default=8, help="每页条数（默认8）")
    parser.add_argument("--json", dest="as_json", action="store_true", help="输出原始JSON")
    args = parser.parse_args()

    # 标准化云盘名称
    cloud_filter = None
    if args.cloud:
        cloud_filter = [resolve_cloud(c) for c in args.cloud]

    try:
        result = search(args.keyword)
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_page(result, page=args.page,
                              page_size=args.page_size, cloud_filter=cloud_filter))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "RATE_LIMIT" in body:
            print("❌ 搜索过于频繁，稍等一分钟再试")
        else:
            print(f"❌ API 错误 {e.code}: {body[:200]}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        sys.exit(1)
