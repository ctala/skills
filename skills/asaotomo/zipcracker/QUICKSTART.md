# 🚀 ZipCracker Skill 快速入门

ZipCracker 是 Hx0 战队出品的高性能 ZIP 密码破解工具。本版本已专为 OpenClaw 深度优化，支持 AI 代理后台静默异步调用。

## 1. 安装与注册 (OpenClaw 环境)

将解压后的文件夹移入 OpenClaw 的工作区（通常是 `skills/` 目录），然后执行一键挂载脚本：

```
# 赋予执行权限并运行
chmod +x install.sh
./install.sh

```

## 2. 验证状态

挂载完成后，检查 OpenClaw 是否已成功接管该技能：

```
openclaw skills list

```

*💡 如果在列表中看到 `✓ ready | 📦 zipcracker`，说明大模型已经准备好调用它了！*

## 3. 立即体验 (自然语言调用)

你可以直接向 OpenClaw 智能助手发送以下指令：

* **伪加密修复**："检查一下桌面的 `flag.zip` 是不是伪加密，是的话直接帮我解压出来。"
* **掩码攻击**："用掩码 `?d?d?d?d` 帮我爆破一下 `secret.zip`，密码应该是4位纯数字。"
* **字典攻击**："调用 ZipCracker，用内置字典破解 `test.zip`。"

---

> 📚 **进阶阅读**: 关于 CRC32 碰撞、自定义大字典处理以及命令行 (CLI) 模式的具体参数说明，请查阅 [SKILL.md](https://www.google.com/search?q=./SKILL.md)。