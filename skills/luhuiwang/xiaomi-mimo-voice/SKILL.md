---
name: xiaomi-mimo-voice
version: 1.0.2
description: |
  使用小米 MiMo V2 TTS 模型进行语音合成（文字转语音）。
  支持中文、英文、多种风格（情感、角色扮演、方言、语速控制等）。
author: 小老弟
category: audio-generation
tags:
  - tts
  - voice
  - audio
  - mimo
  - xiaomi
---

# MiMo 语音合成技能

通过小米 MiMo V2 TTS API 将文字转为自然流畅的语音。

## 前置条件

### 1. 安装依赖

```bash
pip install openai
```

### 2. 设置 API Key

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "tools": {
    "mimoTts": {
      "apiKey": "your-api-key"
    }
  }
}
```

或使用环境变量（优先级更高）：

```bash
export MIMO_API_KEY='your-api-key'
```

## 使用方式

```bash
python3 <skill_dir>/scripts/tts.py --text "要合成的文字" --output audio.wav
```

### 参数

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `--text` | ✅ | 要合成的文字（可包含风格标签） | — |
| `--output` | ❌ | 输出音频文件路径 | `output.wav` |
| `--voice` | ❌ | 音色：`mimo_default` / `default_zh` / `default_en` | `mimo_default` |
| `--style` | ❌ | 语音风格（见下方列表） | — |
| `--format` | ❌ | 输出格式：`wav` / `pcm16` | `wav` |
| `--user-text` | ❌ | 用户侧消息（可选，辅助上下文） | — |

### 音色

| 音色 | 说明 |
|------|------|
| `mimo_default` | 默认音色 |
| `default_zh` | 中文优化音色 |
| `default_en` | 英文优化音色 |

### 风格列表

**情感**
`Happy` · `Sad` · `Angry` · `Surprised` · `Fearful` · `Disgusted` · `Calm`

**语速控制**
`Speed up` · `Slow down`

**角色扮演**
`Sun Wukong` · `Lin Daiyu` · `Zhang Fei` · `Guan Yu` · `Zhuge Liang`

**风格变化**
`Whisper` · `Clamped voice` · `Taiwanese accent`

**方言**
`Northeastern dialect` · `Sichuan dialect` · `Cantonese` · `Henan dialect`

**其他**
`唱歌` · `Narration` · `Storytelling`

## 示例

```bash
# 基础语音合成
python3 scripts/tts.py --text "你好，世界！" --output hello.wav

# 带情感风格
python3 scripts/tts.py --text "太开心了！" --style Happy --output happy.wav

# 角色扮演
python3 scripts/tts.py --text "俺老孙来也！" --style "Sun Wukong" --output wukong.wav

# 英文语音
python3 scripts/tts.py --text "Hello world!" --voice default_en --output hello_en.wav

# 方言
python3 scripts/tts.py --text "干啥呢老铁" --style "Northeastern dialect" --output dongbei.wav

# 播报风格
python3 scripts/tts.py --text "以下是今天的新闻摘要" --style Narration --output news.wav
```

## 输出格式

脚本输出 JSON 格式的结果：

```json
{
  "status": "success",
  "file": "output.wav",
  "size_kb": 128.5,
  "duration_sec": 5.2,
  "voice": "mimo_default",
  "style": "Happy",
  "text": "太开心了！"
}
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `未设置 MIMO_API_KEY` | 配置文件未配置或环境变量未设置 | 在 openclaw.json 中配置 `tools.mimoTts.apiKey` 或设置环境变量 |
| `API 返回异常` | API Key 无效或过期 | 检查 Key 是否正确 |
| `未获取到音频数据` | 文本内容被拒绝 | 检查文本是否合规 |
| `requests 超时` | 网络问题 | 检查网络连接 |

## 技术细节

- 模型：`mimo-v2-tts`
- API：`https://api.xiaomimimo.com/v1/chat/completions`
- 采样率：24kHz（PCM16 格式）
- 文字需放在 `role: assistant` 的消息中
- 风格标签格式：`<style>风格</style>` 放在文字开头

## 更新日志

### v1.0.2 (2026-03-24)
- name 同步更新为 xiaomi-mimo-voice

### v1.0.1 (2026-03-24)
- 更改 ClawHub slug 为 xiaomi-mimo-voice

### v1.0.0 (2026-03-24)
- 首次发布
- 支持中文、英文语音合成
- 支持情感、角色扮演、方言等多种风格
- 支持 WAV 和 PCM16 两种输出格式
