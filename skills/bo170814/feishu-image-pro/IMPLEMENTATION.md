# 飞书图片发送功能实现总结

## 问题背景

在飞书聊天中发送图片需要两步：
1. 调用上传图片接口获取 `image_key`
2. 使用该 `image_key` 发送消息

OpenClaw 原有的飞书 `message` 工具不支持直接发送本地图片。

## 解决方案

创建了 `feishu-image` 技能，封装了飞书图片上传和发送功能。

## 实现细节

### 技术栈
- Node.js
- 飞书 SDK: `@larksuiteoapi/node-sdk`
- 飞书应用：企业自建应用

### 核心功能

**1. 上传图片**
```javascript
const imageKey = await client.im.image.create({
  data: {
    image_type: 'message',
    image: imageBuffer,
  },
});
```

**2. 发送图片消息**
```javascript
await client.im.message.create({
  params: { receive_id_type: 'open_id' },
  data: {
    receive_id: targetOpenId,
    msg_type: 'image',
    content: JSON.stringify({ image_key: imageKey }),
  },
});
```

### 文件结构

```
feishu-image-pro/
├── SKILL.md              # 技能文档
├── README.md             # 使用说明
├── feishu-image-tool.js  # 主要工具脚本
├── index.js              # 简化封装
├── config.example.json   # 配置示例
├── .gitignore           # Git 忽略
└── package.json         # 项目配置
```

## 使用方法

### 命令行调用

```bash
# 发送图片给用户（带文字）
node feishu-image-tool.js send \
  --target ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  --file /tmp/image.png \
  --message "图片说明"

# 仅上传图片
node feishu-image-tool.js upload \
  --file /tmp/image.png

# 使用已有 image_key 发送
node feishu-image-tool.js send-with-key \
  --target ou_xxx \
  --image-key img_v3_xxx
```

### 在代码中调用

```javascript
const { sendImage } = require('feishu-image');

// 发送图片
const result = await sendImage(
  'ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  '/tmp/stock-report.png',
  '📊 今日股票报告'
);
console.log('Message ID:', result.message_id);
```

## 限制

- 图片大小：≤ 10 MB
- 支持格式：JPG, JPEG, PNG, WEBP, GIF, BMP, ICO
- 分辨率：
  - GIF: ≤ 2000 x 2000
  - 其他：≤ 12000 x 12000

## 配置

敏感配置已移除，使用以下方式配置：

1. **环境变量**（推荐）
   ```bash
   export FEISHU_APP_ID="cli_xxx"
   export FEISHU_APP_SECRET="xxx"
   ```

2. **配置文件** (`~/.feishu-image/config.json`)
   ```json
   {
     "appId": "cli_xxx",
     "appSecret": "xxx"
   }
   ```

示例配置文件：`config.example.json`

## 后续优化建议

1. **集成到 OpenClaw 飞书扩展**
   - 在 OpenClaw 飞书扩展中添加 `sendImageFeishu()` 函数
   - 暴露为 `feishu_image` 工具

2. **支持更多消息类型**
   - 图文消息
   - 图片 + 按钮卡片

3. **错误处理增强**
   - 自动重试
   - 图片压缩

4. **配置外部化**
   - 从 OpenClaw 配置读取飞书凭证
   - 支持多账号

## 参考资料

- [飞书开放平台 - 上传图片](https://open.feishu.cn/document/server-docs/im-v1/image/create)
- [飞书开放平台 - 发送消息](https://open.feishu.cn/document/server-docs/im-v1/message/create)
- [@larksuiteoapi/node-sdk](https://www.npmjs.com/package/@larksuiteoapi/node-sdk)

---

创建时间：2026-03-02
作者：OpenClaw Assistant
