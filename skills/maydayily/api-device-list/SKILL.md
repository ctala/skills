---
name: api-device-list
description: "调用 ai-open-gateway 的设备列表查询接口 POST /api/device/list，获取当前用户绑定的所有设备信息。Use when: 需要查看绑定了哪些设备、获取设备 MAC 地址、确认设备是否已绑定。⚠️ 需设置 AI_GATEWAY_API_KEY。"
---

# 设备列表查询接口

## 接口概述

`POST /api/device/list` 用于查询当前认证用户绑定的所有设备列表。该接口无需请求体，设备列表由 api_key 自动关联。

## 📦 安装方式

提供两种安装方式，任选其一：

### 方式一：ClawHub 安装（推荐）

```bash
npx clawhub@latest install closeli/api-device-list
```

自动下载到 `~/.openclaw/workspace/skills/api-device-list/` 并注册到 OpenClaw。

### 方式二：手动安装

1. 下载 skill 文件夹（包含 `SKILL.md` 和 `list_devices.py`）
2. 复制到 OpenClaw skills 目录：

```bash
cp -r api-device-list ~/.openclaw/workspace/skills/
```

3. 在 `~/.openclaw/openclaw.json` 的 `skills.entries` 中注册：

```json
{
  "skills": {
    "entries": {
      "api-device-list": {
        "enabled": true
      }
    }
  }
}
```

安装完成后无需重启 OpenClaw，skill 会在下一次对话中自动生效。

---

## ⚠️ 展示规则（必须严格遵守）

调用成功后，禁止直接展示原始 JSON。必须按以下规则格式化输出：

1. 当 `code == 0` 且 `data` 非空时，以表格展示：

| MAC 地址 | 设备名称 |
|----------|----------|
| aabbccddeeff | 客厅摄像机 |

**关键规则**：device_id 必须去掉 `xxxxS_` 前缀再展示。例如 `xxxxS_aabbccddeeff` → 展示为 `aabbccddeeff`。表头必须写"MAC 地址"，不要写"设备 ID"。

2. 当 `data` 为空数组时，回复："当前账户下没有绑定任何设备。"
3. 当 `code != 0` 时，回复："接口调用失败，错误码 {code}，原因：{message}"

---

## 🐍 前置准备

本技能使用 Python 脚本调用接口，仅依赖 Python 标准库，无需安装第三方包。

调用前请确认 Python 3 环境可用：

```bash
python3 --version
```

如果提示 command not found，请先安装 Python 3（macOS: `brew install python3`，Windows: 从 python.org 下载安装，Linux: `sudo apt install python3` 或 `sudo yum install python3`）。

## 🔑 凭证配置

脚本通过三级优先级自动获取 API_KEY：

| 优先级 | 方式 | 说明 |
|--------|------|------|
| 1（最高） | 环境变量 | 系统环境变量 `AI_GATEWAY_API_KEY` |
| 2 | 配置文件 | `~/.openclaw/.env` 文件 |
| 3（最低） | 命令行参数 | `--api-key` 参数 |

### 方式一：环境变量（当前终端会话有效，关闭终端后失效）

macOS / Linux：

```bash
export AI_GATEWAY_API_KEY="your_api_key"
```

Windows CMD：

```cmd
set AI_GATEWAY_API_KEY=your_api_key
```

Windows PowerShell：

```powershell
$env:AI_GATEWAY_API_KEY="your_api_key"
```

### 方式二：配置文件（永久生效，推荐使用）

在 `~/.openclaw/.env` 文件中添加一行（文件不存在则新建）：

```
AI_GATEWAY_API_KEY=your_api_key
```

所有 skill 共享同一个配置文件，配置一次即可。Windows 下路径为 `%USERPROFILE%\.openclaw\.env`。

### 方式三：命令行参数（仅当次执行有效）

```bash
python3 list_devices.py --api-key your_api_key
```

### 如何获取 API 授权

1. 打开我司 App，进入「AI 智能检测服务」（未开通服务的需要在开通服务后使用）
2. 在页面底部的「事件设置」区域下方，点击「开发者 OpenAPI (用于 OpenClaw 等)」
3. 在弹出的窗口中查看专属 AppID
4. 点击 AppSecret 旁边的「显示」按钮查看完整密钥
5. 分别点击「复制」按钮，将 AppID 和 Secret 粘贴到 OpenClaw 的配置栏中

⚠️ 请务必妥善保管 AppSecret，任何人获得此密钥都可能访问摄像头视频流或检测数据。

## 快速开始

```bash
python3 list_devices.py
```

如果未配置环境变量或 .env 文件，也可以通过命令行传参：

```bash
python3 list_devices.py --api-key your_api_key
```

## 服务地址

部署环境地址为 `https://AI_GATEWAY_DOMAIN`，已硬编码在脚本中。正式部署时请替换为实际域名。

## 认证方式

使用 Bearer Token 认证，脚本自动在请求头中携带 `Authorization: Bearer <api_key>`。

## 请求格式

### 请求头

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | string | 是 | `application/json` |
| Authorization | string | 是 | `Bearer <api_key>`，32 位十六进制字符串 |

### 请求体

无需请求体。

## 响应格式

### 统一响应结构

```json
{
  "code": 0,
  "message": "success",
  "request_id": "<32位请求追踪ID>",
  "data": [...]
}
```

- `code`: 业务错误码，0 表示成功
- `message`: 提示信息
- `request_id`: 请求唯一追踪 ID
- `data`: 响应数据，失败时为 null

### data 字段（设备数组）

| 参数名 | 类型 | 说明 |
|--------|------|------|
| device_id | string | 设备 ID，格式: `xxxxS_<mac地址>`，后续接口均使用此格式 |
| device_name | string | 设备名称，用户自定义的设备别名 |

## 成功响应示例

```json
{
  "code": 0,
  "message": "success",
  "request_id": "00000000000000000000000000000000",
  "data": [
    {
      "device_id": "xxxxS_aabbccddeeff",
      "device_name": "客厅摄像机"
    }
  ]
}
```

## 无设备时的响应

```json
{
  "code": 0,
  "message": "success",
  "request_id": "00000000000000000000000000000000",
  "data": []
}
```

## 错误码

| 错误码 | HTTP 状态码 | 说明 |
|--------|------------|------|
| 1001 | 401 | 未提供 api_key（缺少 Authorization 头或格式不正确） |
| 1002 | 401 | api_key 无效或已禁用 |
| 3001 | 502 | 网关内部服务调用失败 |
| 3004 | 502 | 网关内部服务调用失败 |
| 5000 | 500 | 内部错误 |

## 使用场景

| 场景 | 说明 |
|------|------|
| 📋 查看绑定设备 | 查询当前账户下绑定了哪些摄像机 |
| 🔍 获取设备 MAC | 获取设备 MAC 地址，用于后续接口调用 |
| ✅ 确认设备绑定 | 确认某台设备是否已绑定到当前账户 |
| 🔗 联动其他接口 | 获取 device_id 后调用直播、状态、事件查询等接口 |

## 数据流出说明

本技能通过 Python 脚本调用自建网关，不直接访问第三方服务。

```
Agent (python3 list_devices.py) → ai-open-gateway (自建网关)
```

- ✅ 数据仅发送到自建网关
- ✅ 凭证不暴露给调用方
- ❌ 不会发送数据到其他外部服务

## 注意事项

- device_id 格式为 `xxxxS_<mac>`，是后续所有设备相关接口的标识符
- 全局请求超时为 120 秒
