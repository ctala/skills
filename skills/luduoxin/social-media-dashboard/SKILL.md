# Social Media Dashboard

多平台自媒体数据看板 - 一键聚合各平台粉丝、阅读、收益数据，生成可视化报表。

## 功能

- 采集头条号粉丝数、阅读量、收益数据
- 生成数据看板和趋势报告
- 支持多平台扩展（公众号、小红书、B站、抖音等）

---

## 支持的浏览器

| 浏览器 | AppleScript 支持 | 执行 JS | 需要权限 | 推荐度 |
|-------|-----------------|---------|---------|-------|
| **Chrome** | ✅ 完整支持 | ✅ | 需手动开启 | ⭐⭐⭐ 推荐 |
| **Safari** | ✅ 完整支持 | ✅ | 需手动开启 | ⭐⭐⭐ 推荐 |
| Firefox | ❌ 不支持 | ❌ | - | 不适用 |

---

## 使用方法

当用户请求查看头条号数据时，**必须按照以下流程执行**：

### 步骤 1：检测可用浏览器

优先检测 Chrome，其次 Safari：

```bash
# 检测 Chrome
osascript -e 'tell application "System Events" to return exists application process "Google Chrome"' 2>/dev/null || echo "NOT_INSTALLED"

# 检测 Safari
osascript -e 'tell application "System Events" to return exists application process "Safari"' 2>/dev/null || echo "NOT_INSTALLED"
```

#### 情况 A：没有支持的浏览器

如果 Chrome 和 Safari 都不可用：

> 你的电脑上没有支持的浏览器。本 skill 支持 Chrome 或 Safari。
>
> **解决方案：**
> 1. 安装 [Chrome](https://www.google.com/chrome/) 或使用系统自带的 Safari
> 2. 或者手动提供数据：在浏览器中打开头条号后台，复制页面数据给我

---

### 步骤 2：选择浏览器并检测权限

根据可用浏览器，使用对应的检测脚本：

#### Chrome 权限检测

```bash
osascript <<'EOF'
tell application "Google Chrome"
    try
        set windowCount to count of windows
        return "PERMISSION_OK"
    on error
        return "PERMISSION_DENIED"
    end try
end tell
EOF
```

#### Safari 权限检测

```bash
osascript <<'EOF'
tell application "Safari"
    try
        set docCount to count of documents
        return "PERMISSION_OK"
    on error
        return "PERMISSION_DENIED"
    end try
end tell
EOF
```

#### 情况 B：权限未开启

**Chrome 开启步骤：**
1. 打开 Chrome 浏览器
2. 点击顶部菜单「Chrome」→「视图」→「开发者」
3. 勾选「允许来自 Apple Events 的 JavaScript」

**Safari 开启步骤：**
1. 打开 Safari 浏览器
2. 点击顶部菜单「Safari」→「偏好设置」→「高级」
3. 勾选「在菜单栏中显示开发菜单」
4. 然后点击「开发」→勾选「允许来自 Apple Events 的 JavaScript」

> 检测到浏览器未开启 AppleScript 执行权限。
>
> 请按上述步骤开启权限后告诉我「好了」。

---

### 步骤 3：检测登录状态

使用已授权的浏览器访问头条号：

#### Chrome 采集脚本

```bash
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.toutiao.com/profile_v4/"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### Safari 采集脚本

```bash
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.toutiao.com/profile_v4/"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

#### 情况 C：未登录头条号

> 检测到你还未登录头条号，请先登录：
>
> 1. 我已为你打开头条号登录页面
> 2. 在浏览器中完成登录（扫码或账号密码）
> 3. 登录成功后告诉我「登录好了」

---

### 步骤 4：数据采集

所有条件满足后，执行完整数据采集：

#### Chrome 完整采集

```bash
# 首页
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.toutiao.com/profile_v4/"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF

# 收益数据
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.toutiao.com/profile_v4/analysis/income-overview"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF

# 作品数据-文章
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.toutiao.com/profile_v4/analysis/works-single/article"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF

# 粉丝数据
osascript <<'EOF'
tell application "Google Chrome"
    set URL of active tab of front window to "https://mp.toutiao.com/profile_v4/analysis/fans/overview"
    delay 3
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
```

#### Safari 完整采集

```bash
# 首页
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.toutiao.com/profile_v4/"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF

# 收益数据
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.toutiao.com/profile_v4/analysis/income-overview"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF

# 作品数据-文章
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.toutiao.com/profile_v4/analysis/works-single/article"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF

# 粉丝数据
osascript <<'EOF'
tell application "Safari"
    set URL of front document to "https://mp.toutiao.com/profile_v4/analysis/fans/overview"
    delay 3
    set pageText to do JavaScript "document.body.innerText" in front document
    return pageText
end tell
EOF
```

---

### 数据采集页面

| 页面 | URL | 数据内容 |
|-----|-----|---------|
| 首页 | `/profile_v4/` | 账号信息、粉丝数、总阅读、累计收益 |
| 收益数据 | `/analysis/income-overview` | 日收益明细、收益趋势、可提现金额 |
| 作品数据-全部 | `/analysis/works-overall/all` | 整体展现量、阅读量、点赞评论 |
| 作品数据-文章 | `/analysis/works-overall/article` | 文章整体数据 |
| 作品数据-微头条 | `/analysis/works-overall/weitoutiao` | 微头条整体数据 |
| 单篇作品-文章 | `/analysis/works-single/article` | 每篇文章详细数据 |
| 单篇作品-微头条 | `/analysis/works-single/weitoutiao` | 每条微头条详细数据 |
| 粉丝数据 | `/analysis/fans/overview` | 粉丝变化、活跃度、粉丝画像 |

---

### 步骤 5：生成报告

从页面文本中提取数据，生成 Markdown 格式的数据看板。

---

## 错误处理流程图

```
用户请求查看头条号数据
        ↓
    检测可用浏览器
     ↓         ↓
  Chrome/Safari  无 → 提示安装或手动提供数据
     ↓
    权限已开启？
     ↓        ↓
    是        否 → 引导用户开启权限
     ↓
   已登录？
     ↓        ↓
    是        否 → 引导用户登录
     ↓
  采集数据 → 生成报告
```

---

## 触发词

```
查看我的头条号数据
查看我的头条号详细数据
获取头条号粉丝统计
头条号收益查询
生成自媒体数据周报
我的自媒体数据
头条号数据看板
```

---

## 支持平台

| 平台 | 状态 | 数据类型 |
|-----|------|---------|
| 头条号 | ✅ 已支持 | 粉丝、阅读、收益 |
| 公众号 | 🚧 开发中 | 粉丝、阅读、用户画像 |
| 小红书 | 📋 计划中 | 粉丝、笔记数据 |
| B站 | 📋 计划中 | 粉丝、播放、互动 |
| 抖音 | 📋 计划中 | 粉丝、视频、直播 |

---

## 注意事项

- 请勿频繁请求，避免被平台限流（每次请求间隔 ≥ 3 秒）
- 首次使用需要登录授权
- 数据仅供个人分析参考
- 不要分享登录凭证

---

## 文件说明

```
social-media-dashboard/
├── SKILL.md              # 本文件
├── platforms/
│   └── toutiao.md       # 头条号接口说明
├── templates/
│   ├── dashboard.md     # 数据看板模板
│   └── daily-report.md  # 日报模板
└── scripts/
    └── fetch-toutiao.sh # 数据采集脚本
```
