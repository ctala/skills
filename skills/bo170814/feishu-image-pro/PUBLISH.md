# Feishu Image Skill for OpenClaw

在飞书中发送图片需要两步：先上传图片获取 `image_key`，再发送消息。这个技能封装了整个流程。

## ✨ 功能特性

- 📤 上传图片到飞书服务器
- 📨 发送图片消息到用户或群聊
- 💬 支持附带文字说明
- 🔑 支持使用已有 image_key 发送
- ⚙️ 灵活配置（环境变量/配置文件）

## 🚀 快速开始

### 安装

```bash
clawhub install feishu-image
```

### 配置

**方法 1：环境变量**
```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

**方法 2：配置文件**
```bash
cp config.example.json ~/.feishu-image/config.json
# 编辑 ~/.feishu-image/config.json 填入你的凭证
```

### 使用

```bash
# 发送图片
feishu-image send --target ou_xxx --file image.png --message "说明文字"

# 或直接用 Node.js
node $(clawhub which feishu-image)/feishu-image-tool.js send \
  --target ou_xxx \
  --file image.png \
  --message "Hello"
```

## 📖 文档

- [README.md](README.md) - 详细使用说明
- [SKILL.md](SKILL.md) - 技能技术文档
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - 实现细节

## 🔐 权限要求

飞书应用需要以下权限：
- `im:message` - 发送消息
- `im:image` - 上传图片

## 📝 示例

### 发送股票报告

```javascript
const { sendImage } = require('feishu-image');

await sendImage(
  'ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  '/tmp/stock-report.png',
  '📊 今日股票报告'
);
```

### 在 OpenClaw 中使用

```javascript
const { exec } = require('child_process');

exec('feishu-image send --target ou_xxx --file image.png', (err, stdout) => {
  const result = JSON.parse(stdout);
  console.log('Sent:', result.message_id);
});
```

## 🛠️ 开发

```bash
# 克隆项目
git clone https://github.com/openclaw/feishu-image-skill
cd feishu-image-skill

# 安装依赖（可选，使用系统 SDK）
npm install

# 测试
node feishu-image-tool.js upload --file test.png
```

## 📦 文件结构

```
feishu-image/
├── feishu-image-tool.js  # 主要工具
├── index.js              # Node.js API
├── SKILL.md              # 技能文档
├── README.md             # 使用说明
├── IMPLEMENTATION.md     # 实现细节
├── package.json          # 项目配置
├── config.example.json   # 配置示例
└── .gitignore           # Git 忽略文件
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
