---
name: 2fun-pansou
description: Search Chinese cloud drive (网盘) resources via 2fun.live. Finds movies, TV shows, anime, dramas, and files on Aliyun (阿里云盘), Quark (夸克网盘), Baidu (百度网盘), 115, PikPak, UC, Xunlei, and Tianyi. Supports drive type filtering, pagination. Returns direct share links. Keywords: 网盘搜索, pan search, cloud drive, 阿里云盘, 夸克, 百度云, movie, 电影, 剧集, 资源, Chinese media.
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"] }
    }
  }
---

# 2fun-pansou — 网盘资源搜索

通过 [2fun.live](https://2fun.live) 聚合搜索阿里云盘、夸克网盘、百度网盘等中国主流网盘的分享资源，支持云盘筛选与翻页。

> **免责声明 / DMCA Notice**
>
> 本工具仅为搜索聚合器，不托管、不存储任何受版权保护的内容。搜索结果均为第三方用户上传的公开分享链接，
> 本工具不对其内容、合法性或可用性负责。如需举报侵权内容，请联系相应网盘平台或 [2fun.live](https://2fun.live)。
> 用户须遵守所在地区的法律法规及各网盘平台的服务条款。
>
> This tool is a search aggregator only. It does not host or distribute any copyrighted content.
> All links are publicly shared by third parties. For DMCA takedown requests, contact the respective
> cloud storage platform or [2fun.live](https://2fun.live). Users are responsible for complying with
> applicable laws and platform terms of service.

## 触发场景

用户说：
- "搜一下 XX 网盘"、"找一下 XX 的网盘资源"
- "有没有 XX 的百度云"、"夸克有没有 XX"
- "下一页"、"第2页"（接上一次搜索）
- "只看阿里云盘"、"换成夸克"（切换云盘筛选）

## 调用方式

```bash
# 基本搜索（第1页，所有云盘）
python3 {skill_dir}/scripts/search.py "关键词"

# 指定云盘筛选（可多个）
python3 {skill_dir}/scripts/search.py "关键词" --cloud aliyun
python3 {skill_dir}/scripts/search.py "关键词" --cloud aliyun quark

# 翻页
python3 {skill_dir}/scripts/search.py "关键词" --page 2

# 组合
python3 {skill_dir}/scripts/search.py "关键词" --cloud baidu --page 3

# 每页条数（默认8）
python3 {skill_dir}/scripts/search.py "关键词" --page-size 5
```

`{skill_dir}` 替换为本 skill 的实际目录路径。

## 云盘参数速查

| 用户说 | --cloud 值 |
|--------|-----------|
| 阿里/阿里云盘 | aliyun |
| 夸克 | quark |
| 百度/百度云 | baidu |
| 115 | 115 |
| PikPak | pikpak |
| UC | uc |
| 迅雷 | xunlei |
| 123网盘 | 123 |
| 天翼 | tianyi |
| 移动云盘 | mobile |
| 磁力 | magnet |
| ED2K | ed2k |

中文名也可以直接传，脚本内部会自动转换（如 `--cloud 阿里`）。

## 对话状态管理

**记住上一次的搜索关键词**，当用户说"下一页"/"第N页"/"换成XX盘"时，使用同一关键词：

```
用户: 搜一下太平年
→ python3 search.py "太平年"               # page=1, cloud=all

用户: 下一页
→ python3 search.py "太平年" --page 2      # 记住关键词

用户: 只看夸克
→ python3 search.py "太平年" --cloud quark --page 1

用户: 第3页
→ python3 search.py "太平年" --cloud quark --page 3
```

## 输出示例

```
🔍 太平年
第 1/23 页 · 共 184 条（387ms）
────────────────────────────
☁️ 阿里云盘
  1. `alipan.com/s/xxx`  太平年 4K HDR DV 高码率 全48集 · 2026-03-01
  2. `alipan.com/s/yyy`  太平年 4K 全48集 · 2026-02-16

⚡ 夸克网盘
  3. `pan.quark.cn/s/zzz`  太平年 4K[臻彩]

────────────────────────────
➡️ 下一页：「第2页 太平年」
📂 筛选云盘: 阿里云盘(6) · 夸克网盘(59) · 百度网盘(28) · ...
🌐 https://s.2fun.live/search?q=太平年
```

## 注意事项

- 磁力链接默认显示「🔒 需登录查看完整链接」（服务端白名单控制）
- 限速 10次/分钟（按服务器出口 IP）
- 搜索结果有 5 分钟服务端缓存
- 分享链接可能随时失效，建议直接跳转 s.2fun.live 获取最新结果
- 仅支持中文内容搜索，数据来源为中国大陆网盘平台
