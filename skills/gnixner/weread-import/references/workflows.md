# weread-import workflows

## 0. 首次安装依赖

```bash
cd scripts
npm install
```

## 1. 首次导入到真实目录

适用：用户已经确定输出目录，想把微信读书笔记导入到 Obsidian / Reading。

推荐命令：

```bash
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading"
```

## 2. 先临时验证，再落真实目录

适用：刚改完模板、merge、frontmatter、tags，想先确认输出结构。

先跑临时目录：

```bash
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output /tmp/weread-verify --force
```

确认没问题后，再跑真实目录：

```bash
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading" --force
```

## 3. 重渲染已有文件

适用：模板变了、frontmatter 变了、tags 变了、删除归档逻辑变了。

```bash
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading" --force
```

## 4. 自定义 frontmatter tags

```bash
bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading" --tags "reading/weread,book"
```

或：

```bash
WEREAD_TAGS="reading/weread,book" bash ./scripts/run.sh --book "自卑与超越" --mode api --cookie-from browser --output "/path/to/Reading"
```

## 5. 常见故障

### 登录超时 / 业务错误

现象：CLI 报错，提示业务错误、登录超时、或浏览器里没有可用 cookie。

处理：
1. 确认 Chrome 远程调试实例还在
2. 确认该实例里已经登录微信读书
3. 再重跑 `--cookie-from browser`
4. 必要时改用 `--cookie '...'`

### 想先验证不想污染真实笔记

优先输出到 `/tmp/...`，确认结构后再重跑真实目录。
