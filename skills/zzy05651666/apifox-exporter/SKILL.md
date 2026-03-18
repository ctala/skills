# Apifox Exporter Skill

**版本：** 1.0.0  
**作者：** 果果 @ 婉秋  
**描述：** 将 Apifox 导出的 OpenAPI JSON 文件整理成标准格式的文档

---

## ⚠️ 重要说明

**本 Skill 的功能：**
- ✅ 读取你**手动导出**的 OpenAPI JSON 文件
- ✅ 按模块分组整理接口
- ✅ 递归展开所有 `$ref` 引用，深挖到最底层数据结构
- ✅ 支持多项目管理，随时切换
- ✅ 自动整理输出到桌面
- ✅ 格式美观，带目录索引

**本 Skill 不会：**
- ❌ 自动登录 Apifox
- ❌ 自动从 Apifox 抓取数据
- ❌ 访问网络或 Apifox API

---

## 💡 使用场景

**一次性设置，长期便利：**

1. **第一次：** 手动从 Apifox 导出 JSON（1 分钟）
2. **之后：** 每次接口更新，只需说 **"更新接口文档"**（1 秒钟）
3. **自动：** 桌面生成整理好的标准文档

**对比手动整理：**
| 方式 | 时间 | 质量 |
|------|------|------|
| 手动整理 | 2-3 小时 | 容易出错 |
| 本 Skill | 1 秒钟 | 100% 准确 |

---

## 安装方法

### 方法 1：从 ClawHub 安装（推荐）

```bash
openclaw skill install apifox-exporter
```

### 方法 2：手动安装

1. 下载 skill 文件夹到 `~/.openclaw/workspace/skills/apifox-exporter/`
2. 首次运行会自动创建输入目录

---

## 使用方法

### 基础用法

**导出默认项目口令：**
```
更新接口文档
导出接口
刷新 Apifox 接口
```

**导出指定项目口令：**
```
更新接口文档，用商城项目
导出接口，用后台管理
```

### 高级用法

**命令行直接运行：**
```bash
# 使用默认 source.json
node script/export.js

# 使用指定项目
node script/export.js 商城
node script/export.js source-商城.json
```

---

## 文件结构

```
apifox-exporter/
├── SKILL.md              # Skill 描述文件
├── script/
│   └── export.js         # 导出脚本
├── examples/
│   └── source-example.json  # 示例文件（可选）
└── README.md             # 详细文档
```

---

## 配置文件

### 输入文件位置

将 Apifox 导出的 OpenAPI JSON 文件放在：
```
~/.openclaw/workspace/script/apifox/
```

**命名规则：**
- 默认项目：`source.json`
- 其他项目：`source-项目名.json`

### 输出文件位置

导出的接口文档保存在：
```
~/Desktop/Apifox 接口导出.txt
```

---

## 输出格式示例

```
================================================================================
目  录
================================================================================

【登录 - 认证】 (4 个接口)
  1. 使用账号密码登录
  2. 登出系统
  3. 刷新令牌
  4. 获取登录用户的权限信息

════════════════════════════════════════════════════════════════════════════════
【登录 - 认证】 (4 个接口)
════════════════════════════════════════════════════════════════════════════════

1. 使用账号密码登录
   所属模块：登录 - 认证
   接口地址：/system/auth/login  POST

请求参数 application/json：
{
  "username": "admin",
  "password": "lycheeai@123456",
  "rememberMe": false
}

响应数据：
{
  "code": 0,
  "data": {
    "userId": 0,
    "accessToken": "",
    "refreshToken": "",
    "expiresTime": ""
  },
  "msg": ""
}

────────────────────────────────────────────────────────────────────────────────
```

---

## 配置选项

### 自定义输出路径

编辑 `script/export.js`，修改：
```javascript
const outputFile = path.join(USER_HOME, 'Desktop', 'Apifox 接口导出.txt');
```

### 自定义脚本位置

编辑 `script/export.js`，修改：
```javascript
const WORKSPACE_DIR = path.join(USER_HOME, '.openclaw', 'workspace');
```

---

## ⚠️ 安全提示

**敏感数据警告：**
- 导出的文档会原样输出 OpenAPI JSON 中的内容
- 如果你的 JSON 包含真实密码、token、密钥等敏感信息，这些会出现在输出文件中
- **建议：** 在 Apifox 导出前删除敏感示例数据，或在受控环境中测试

**跨平台支持：**
- Windows: `C:\\Users\\用户名\\.openclaw\\workspace\\`
- Mac/Linux: `~/.openclaw/workspace/`

---

## 常见问题

### Q: 如何切换项目？
A: 从 Apifox 导出新项目，保存为 `source-项目名.json`，然后说"更新接口文档，用项目名"

### Q: 响应数据为什么是 `[object Object]`？
A: 旧版本问题，请升级到最新版 skill

### Q: 支持其他格式导出吗？
A: 目前只支持 OpenAPI 3.0 格式，如需其他格式请提 issue

### Q: 能自动从 Apifox 抓取数据吗？
A: 不支持。需要手动从 Apifox 导出 JSON 文件，本 Skill 只负责整理格式。

---

## 更新日志

### v1.0.1 (2026-03-18)
- 🔧 修复硬编码路径问题，支持跨平台
- 📝 明确说明需要手动导出 JSON
- ⚠️ 添加敏感数据警告

### v1.0.0 (2026-03-18)
- ✨ 初始版本发布
- ✨ 支持多项目管理
- ✨ 递归展开所有 schema 引用
- ✨ 按模块分组输出
- ✨ 带目录索引

---

## 许可证

MIT License

---

## 反馈与建议

- GitHub: https://github.com/openclaw/skills
- Discord: https://discord.com/invite/clawd
- ClawHub: https://clawhub.com

---

**Made with ❤️ by 果果**
