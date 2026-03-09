# video-script-creator

短视频脚本生成器，支持抖音/快手/YouTube Shorts/B站等主流短视频平台。

## Description

生成短视频脚本、分镜提示、口播稿、爆款标题、标签推荐、开场钩子、结尾互动引导（CTA）等内容。纯本地模板生成，不依赖外部API。

**Use when:**
1. 需要生成短视频完整脚本（开场-主体-结尾+分镜提示）
2. 生成短视频开场钩子（前3秒留人）
3. 生成短视频爆款标题
4. 生成视频大纲/结构
5. 生成结尾引导互动文案（CTA）
6. 查看当前热门视频类型和方向
7. 任何与短视频脚本创作相关的任务

**Supported platforms:** 抖音 (douyin)、快手 (kuaishou)、YouTube Shorts (youtube)、B站 (bilibili)

## Commands

Run via `bash <skill_dir>/scripts/video-script.sh <command> [args]`

| Command | Description |
|---------|-------------|
| `script "主题" [--platform douyin\|kuaishou\|youtube\|bilibili] [--duration 30\|60\|90]` | 生成完整脚本（开场-主体-结尾+分镜提示） |
| `hook "主题"` | 生成5个开场钩子（前3秒留人） |
| `title "主题"` | 生成5个爆款标题 |
| `outline "主题"` | 生成视频大纲 |
| `cta "主题"` | 生成结尾引导互动文案 |
| `trending` | 热门视频类型/方向 |
| `help` | 显示帮助信息 |

## Examples

```bash
# 生成抖音60秒脚本
bash scripts/video-script.sh script "如何3分钟做一杯手冲咖啡" --platform douyin --duration 60

# 生成开场钩子
bash scripts/video-script.sh hook "租房避坑指南"

# 生成爆款标题
bash scripts/video-script.sh title "健身新手入门"

# 生成视频大纲
bash scripts/video-script.sh outline "Python学习路线"

# 生成CTA结尾
bash scripts/video-script.sh cta "旅行vlog"

# 查看热门方向
bash scripts/video-script.sh trending
```

## Requirements

- bash
- python3 (>= 3.6)
- 无需外部API
