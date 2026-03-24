# MiMo TTS

小米 MiMo V2 语音合成技能，支持中文、英文及多种风格。

## 特性

- 🎙️ 中文 / 英文语音合成
- 😊 情感风格：Happy、Sad、Angry 等
- 🎭 角色扮演：孙悟空、林黛玉等
- 🗣️ 方言支持：东北话、四川话、粤语等
- 📢 播报/讲故事风格
- 🎵 唱歌模式

## 快速开始

```bash
# 设置 API Key
export MIMO_API_KEY='your-api-key'

# 安装依赖
pip install openai

# 合成语音
python3 scripts/tts.py --text "你好世界" --output hello.wav
```

## 安装

```bash
npx clawhub install xiaomi-mimo-voice
```

## 许可证

MIT
