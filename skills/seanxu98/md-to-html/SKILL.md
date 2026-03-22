---
name: md-to-html
description: "将Markdown格式的笔记转换为带左侧固定目录大纲的可阅读HTML文件。适用于：(1) 将学习笔记、技术文档转换为可浏览的HTML；(2) 为Markdown文件生成带目录导航的阅读界面；(3) 整理长文档生成静态网站。触发条件：用户说转换HTML、markdown转html、生成HTML笔记、把笔记转成网页等"
metadata: { "openclaw": { "emoji": "📄", "requires": { "bins": ["python"] } } }
---

# Markdown转HTML工具

将Markdown笔记转换为带有左侧固定目录大纲的可阅读HTML页面。

## 使用方法

### 基本命令

```bash
<python路径> <skill路径>/scripts/md2html.py -i <markdown文件路径>
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `-i, --input` | 输入的Markdown文件路径（必需） |
| `-o, --output` | 输出的HTML文件路径（可选，默认与输入同目录） |
| `-t, --title` | HTML页面标题（可选，默认使用文件名） |
| `-l, --level` | 目录中显示的最大标题层级（1-6，默认4） |

### 示例

```bash
# 基本转换
<python路径> <skill路径>/scripts/md2html.py -i "AI学习笔记.md"

# 指定输出路径
<python路径> <skill路径>/scripts/md2html.py -i notes.md -o output.html

# 指定标题和目录层级
<python路径> <skill路径>/scripts/md2html.py -i notes.md -t "我的学习笔记" -l 3
```

> **注意**：当前环境实际命令：
> - `<python路径>` = `C:\App\anaconda3\envs\OpenClaw\python.exe`
> - `<skill路径>` = `C:\Users\Sean\.openclaw\workspace\skills\md-to-html`

## 输出特点

生成的HTML包含：
- **左侧固定目录**：自动从标题生成，支持折叠/展开
- **目录交互**：点击跳转、滚动高亮、可拖拽调整宽度
- **代码高亮**：Prism.js 支持 Python、Bash、JavaScript、JSON
- **数学公式**：MathJax 支持 LaTeX 语法
- **Mermaid图表**：支持 flowchart、sequenceDiagram、graph 等图表
- **响应式设计**：适配移动端，自动隐藏侧边栏
- **返回顶部**：滚动后显示返回顶部按钮

## 支持的Markdown特性

- 标题（H1-H6）
- 段落、粗体、斜体
- 有序/无序列表
- 代码块（带语法高亮）
- 表格
- 引用块
- 图片
- 超链接
- 数学公式（LaTeX）
- Mermaid 图表

## 依赖

- Python 3.13 (OpenClaw环境)
- markdown (Python库)

依赖已预装在OpenClaw环境中。