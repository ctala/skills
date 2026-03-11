# Windows Screenshot

为 Windows 无头节点提供 GDI+ 截图能力。

## 功能

- **纯 PowerShell 实现**：无外部依赖
- **GDI+ 屏幕捕获**：支持多屏幕
- **图像缩放**：自动优化分辨率
- **Telegram 集成**：两步流程发送截图

## 安装

1. 从 [GitHub 仓库](https://github.com/vvxer/windows-screenshot) 克隆或下载 `screenshot.ps1`
2. 将 `screenshot.ps1` 放在 OpenClaw 工作目录的可执行路径中
3. 配置 OpenClaw `exec` 工具指向 Windows 节点
4. 设置 `TELEGRAM_BOT_TOKEN` 环境变量（可选，用于 Telegram 集成）

### 快速开始

```powershell
# 克隆或获取源代码
git clone https://github.com/vvxer/windows-screenshot.git

# 或下载 screenshot.ps1（直接访问 GitHub）
```

## 使用

### 方法 1：直接执行

```bash
openclaw exec powershell -File screenshot.ps1
```

### 方法 2：通过网关（推荐）

```bash
# 步骤 1：执行脚本获取路径
openclaw exec powershell -File screenshot.ps1

# 输出示例：
# MEDIA:C:\Users\YourUsername\.openclaw\media\screenshot_YYYYMMDD_HHMMSS.png

# 步骤 2：发送到 Telegram
openclaw message send --channel telegram --target YOUR_USER_ID --media /path/to/screenshot_YYYYMMDD_HHMMSS.png
```

## 输出

脚本将截图保存为 PNG：

```
.openclaw/media/screenshot_YYYYMMDD_HHMMSS.png
```

并输出 `MEDIA:` 前缀路径用于后续处理。

## 技术细节

- **图像库**：System.Drawing (GDI+)
- **格式**：PNG 24-bit
- **分辨率**：自适应（根据屏幕缩放）
- **文件大小**：通常 50-200 KB

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| "找不到类型"System.Drawing"" | 在 .NET Framework 4.x+ 上运行（Windows 默认） |
| 图像全黑 | 检查屏幕/GPU 状态；确保不在锁屏 |
| 文件名冲突 | 脚本使用时间戳自动避免重复 |

## 许可证

MIT-0 - 无署名、无限制使用
