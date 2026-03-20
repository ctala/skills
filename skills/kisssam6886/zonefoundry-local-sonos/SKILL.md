---
name: zf-local-sonos
description: Use this skill when a user wants an OpenClaw/local agent/bot to control Sonos through `zf` on a machine inside the same LAN. It covers first-run Sonos readiness checks, default-room setup, service-readiness probing, safe command mapping, and failure routing for playback, queue recovery, and helper-room rebuild.
metadata: {"openclaw":{"emoji":"🔊","homepage":"https://github.com/kisssam6886/zonefoundry","requires":{"bins":["zf"]},"install":[{"id":"go-build","kind":"go","module":"github.com/kisssam6886/zonefoundry/cmd/zf","bins":["zf"]}]}}
---

# zf Local Sonos

Use this skill when the user is asking a local agent or bot to:

- connect to Sonos for the first time
- check whether Sonos control is ready
- play, pause, skip, change volume, or inspect status
- add songs to current queue without interrupting playback
- control NetEase / QQ Music through `zf`
- manage queue (list, reorder, remove, prune grey tracks)
- recover from queue or transport pollution

Do not use this skill for:

- Sonos account setup UX inside the official Sonos app
- billing, cloud relay, or hosted bot product logic
- arbitrary natural-language chat unrelated to Sonos control

## Core rule

Treat `zf` as the execution layer.

Layering must stay:

`bot / agent / web onboarding` -> `zf` -> `Sonos`

The bot/agent translates intent and explains results.
`zf` does discovery, playback, queueing, diagnostics, and recovery.

## First-run flow

When the user mentions Sonos for the first time, or says things like:

- "帮我连接 Sonos"
- "帮我喺 Sonos 播歌"
- "你可唔可以控制我个 Sonos"
- "检查下 Sonos 用唔用到"

do not immediately answer with a generic "未配置".

**推荐用 `zf setup`**（一条命令完成全部诊断）：

```bash
zf setup --format json
```

这条命令会自动检查：speaker 发现 → default room → 服务列表 + 认证状态 → default service → 总结。
返回 JSON 包含 `steps` 数组，每步有 `status`（ok/warn/fail）和 `action`（建议命令）。

如果 `zf setup` 不可用（旧版本），手动 preflight：

1. Verify `zf` is available.
2. Run `zf doctor --format json`.
3. Run `zf discover --format json`.
4. If rooms are found, check `zf config get defaultRoom`.
5. If no default room is set, ask the user to choose one visible room.
6. Run `zf service list --format json` to check available services and auth status.
7. If the user mentions a music service, check service visibility/readiness before claiming playback is ready.

## Environment gate

Before promising bot control, confirm there is an always-on local node in the same LAN as Sonos.

Valid nodes:

- Mac or Windows PC
- NAS
- mini PC
- Raspberry Pi
- Docker host

If the user only has a phone:

- explain that Sonos official mobile apps can add/login music services
- do not promise persistent local bot control
- do not pretend a phone alone is an always-on local agent

## Minimum preflight commands

Use JSON by default. Prefer `zf setup` for one-shot diagnostics:

```bash
zf setup --format json                    # 一条搞定全部检查（推荐）
```

或者逐步检查：

```bash
zf doctor --format json
zf discover --format json
zf config get defaultRoom
zf service list --format json             # 服务列表 + 认证状态
zf config get defaultService              # 默认音乐服务
```

If the user already specified a room, prefer `--name "<room>"` in later commands.

## Default room behavior

If there is no default room:

- ask only for one room choice
- after the user chooses, set it once

```bash
zf config set defaultRoom "客厅"
```

## Default service behavior

If there is no default service:

- run `zf service list --format json` to see available services
- ask user which service they primarily use
- set it once

```bash
zf config set defaultService "QQ音乐"
```

After room + service are set, allow simple requests:

- "暂停"
- "下一首"
- "播郑秀文" → `zf play music "郑秀文"`
- "播周杰伦的歌" → `zf play music "周杰伦"`
- "再加一首陈奕迅" → `zf play music "陈奕迅" --enqueue` ⚠️ 注意 --enqueue
- "帮我加几首 Adele 的歌" → `zf play music "Adele" --enqueue --limit 5`
- "看下队列" → `zf queue list`
- "删掉第 3 首" → `zf queue remove 3`

## Safe command mapping

For direct room control, prefer `execute` when the action maps cleanly.

Examples:

```bash
zf execute --data '{"action":"status","target":{"room":"客厅"}}'
zf execute --data '{"action":"pause","target":{"room":"客厅"}}'
zf execute --data '{"action":"next","target":{"room":"客厅"}}'
zf execute --data '{"action":"volume.set","target":{"room":"客厅"},"request":{"volume":20}}'
```

For music playback, prefer the unified `play music` command:

```bash
# 统一播放入口（清空队列并播放，自动使用 defaultService）
zf play music "周杰伦" --format json
zf play music "Taylor Swift" --service Spotify --format json

# 追加到队列（不打断当前播放！用户说"加歌"/"追加"/"再来一首"时必须用这个）
zf play music "郑秀文" --enqueue --format json
zf play music "陈奕迅" --enqueue --limit 5 --format json

# 队列管理
zf queue list --format json            # 查看当前队列
zf queue play 3                         # 播放队列中第 3 首
zf queue remove 5                       # 删除队列中第 5 首
zf queue prune --format json            # 清理灰色/不可播的歌曲

# 服务专用快捷命令（保留兼容）
zf ncm lucky --name "客厅" "郑秀文" --format json
zf ncm play --name "客厅" "周杰伦" --format json
zf play spotify "Taylor Swift" --format json

# 其他
zf smapi search --service "QQ音乐" --category tracks --open --index 1 --format json "周杰伦"
zf say "一分钟新闻" --name "客厅" --mode queue-insert --format json
```

### 播放命令选择指南

| 用户意图 | 推荐命令 | 说明 |
|---------|----------|------|
| "播放周杰伦" | `zf play music "周杰伦"` | 清空队列并开始播放搜索结果 |
| "再加一首郑秀文" / "加歌" / "追加" | `zf play music "郑秀文" --enqueue` | **不会打断当前播放**，追加到队列末尾 |
| "加几首陈奕迅的歌" | `zf play music "陈奕迅" --enqueue --limit 5` | 追加多首到队列 |
| "用网易云播放" | `zf play music "..." --service "网易云音乐"` 或 `zf ncm play "..."` | |
| "用 Spotify 播" | `zf play music "..." --service Spotify` | |
| "帮我清理灰色歌曲" | `zf queue prune` | |
| "看下队列" | `zf queue list --format json` | |
| "播第 3 首" | `zf queue play 3` | |
| "删掉第 5 首" | `zf queue remove 5` | |
| "设个闹钟" | `zf alarm add --time "07:00"` | |
| "30分钟后关掉" | `zf sleep set 30m` | |

### ⚠️ 关键区分：播放 vs 加歌

- **用户说"播放 XX"**：用 `zf play music "XX"` — 这会**清空**当前队列并播放新内容
- **用户说"加一首 XX" / "再来一首" / "追加" / "帮我加"**：**必须**用 `zf play music "XX" --enqueue` — 这**不会**打断当前播放
- **判断不清时**：如果已有歌曲在播放，默认用 `--enqueue` 更安全

## Known boundaries

- Sonos official app is still the default path for adding/logging in to QQ Music / NetEase Cloud Music on Sonos.
- `queue-insert` is the current stable insert/announcement path.
- `RelTime` exact restore is not a formal stable capability.
- `group rebuild` is a recovery tool, not proof that the original defect is fixed.

## Failure routing

Read structured JSON errors first:

- `error.code`
- `error.message`
- `error.details`

Do not classify every playback failure as auth or copyright.

Known cases:

- Same song plays in helper room but not in target room:
  classify as room-local queue/transport pollution first.
- `TRANSITIONING` / partial queue failure:
  do not loop infinite retries.
- Queue appears polluted:
  soft recovery can be "clear and rebuild queue".
- If deeper room-local pollution is confirmed:
  `group rebuild --name "<target>" --via "<helper>"` is the current strong recovery path.

## When to ask the user something

Ask only when needed:

- choose default room
- confirm preferred music service
- confirm helper room usage for `group rebuild`

Do not ask the user to learn repo internals or command names.

## User-facing tone

The user should experience:

- "我先检查这台电脑可不可以发现你局域网里的 Sonos"
- "我找到这些房间：客厅、浴室。你想默认控制哪一个？"
- "已经可以控制了，你现在可以直接说：暂停、下一首、播郑秀文"

Avoid:

- "请安装 Sonos 控制器"
- "请先学会 zf 命令"
- "我未配置到 Sonos 控制器" without having run preflight

## Read these docs when needed

- Onboarding/product boundary: [`references/onboarding-boundary.md`](references/onboarding-boundary.md)
- Command map and recovery rules: [`references/command-map.md`](references/command-map.md)
