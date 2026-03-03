# Sensitive Data Masker - 敏感信息自动脱敏

在 RAG 检索和 API 调用前自动识别并替换敏感信息。

## 🚀 快速开始

### 安装

```bash
# 技能已安装在
/home/subline/.openclaw/workspace/skills/sensitive-data-masker/
```

### 测试

```bash
# 测试脱敏效果
python3 sensitive-data-masker.py test "我的 password=MySecret123，API Key 是 sk-1234567890abcdef"

# 输出
原始文本：我的 password=MySecret123，API Key 是 sk-1234567890abcdef
脱敏后：我的 [PASSWORD:***]，API Key 是 [SK_KEY:***]
检测到 2 个敏感信息
```

---

## 🔐 支持的敏感信息类型

| 类型 | 示例 | 脱敏后 |
|------|------|--------|
| **密码** | `password=MySecret123` | `[PASSWORD:***]` |
| **API Key** | `sk-abcdefghijklmnop` | `[SK_KEY:***]` |
| **Token** | `token=xyz123` | `[TOKEN:***]` |
| **Secret** | `secret=abc+/==` | `[SECRET:***]` |
| **私钥** | `BEGIN RSA PRIVATE KEY` | `[PRIVATE_KEY:***]` |
| **数据库连接** | `mongodb://user:pass@host` | `[DB_CONNECTION:***]` |

---

## ⚙️ 配置

**文件位置**: `~/.openclaw/config/sensitive-data.json`

```json
{
  "enabled": true,
  "mode": "rag_and_api",
  "patterns": [
    {
      "name": "password",
      "regex": "(?i)(password=|password:)[\\w@#$%^&*!]+",
      "replacement": "[PASSWORD:***]",
      "enabled": true
    }
  ],
  "whitelist": ["test_password", "example.com"],
  "log_enabled": true
}
```

### 模式说明

| 模式 | 说明 |
|------|------|
| `rag_and_api` | RAG 和 API 调用都脱敏（推荐） |
| `rag_only` | 仅 RAG 检索时脱敏 |
| `api_only` | 仅 API 调用时脱敏 |
| `disabled` | 禁用脱敏 |

---

## 🛠️ 命令

```bash
# 测试脱敏
python3 sensitive-data-masker.py test "password=MySecret"

# 扫描文件
python3 sensitive-data-masker.py scan config.txt

# 查看配置
python3 sensitive-data-masker.py config

# 启用/禁用
python3 sensitive-data-masker.py enable
python3 sensitive-data-masker.py disable
```

---

## 🔗 OpenClaw 集成

### 方式 1：钩子函数

```python
from sensitive_data_masker import before_rag, before_api_call

# RAG 前脱敏
query = before_rag("我的 password=123")
# 输出："我的 [PASSWORD:***]"

# API 调用前脱敏
prompt = before_api_call("使用 sk-abcdef123 调用 API")
# 输出："使用 [SK_KEY:***] 调用 API"
```

### 方式 2：配置文件

在 `~/.openclaw/config/hooks.json` 中添加：

```json
{
  "before_rag": "sensitive-data-masker",
  "before_api_call": "sensitive-data-masker"
}
```

---

## 📊 脱敏日志

**位置**: `~/.openclaw/config/sensitive-data-masker.log`

```
============================================================
Time: 2026-03-03T15:58:00
Detected: 2 items
  - Type: password, Found: password=MySec...
  - Type: sk_key, Found: sk-abcdef123...
Original (first 200 chars): 我的 password=MySecret123...
============================================================
```

---

## 🎯 使用场景

### 场景 1：RAG 检索前脱敏

```python
# 用户查询
query = "如何配置 password=MySecret123 的数据库？"

# 脱敏后提交给搜索引擎
masked_query = before_rag(query)
# "如何配置 [PASSWORD:***] 的数据库？"
```

### 场景 2：API 调用前脱敏

```python
# 用户消息
message = "用 sk-abcdef123 这个 key 调用 API"

# 脱敏后发送给大模型
masked_message = before_api_call(message)
# "用 [SK_KEY:***] 这个 key 调用 API"
```

### 场景 3：扫描文件中的敏感信息

```bash
# 检查配置文件是否有敏感信息
python3 sensitive-data-masker.py scan ~/.bashrc
```

---

## 🔧 自定义规则

添加新的脱敏规则：

```json
{
  "patterns": [
    {
      "name": "my_custom_pattern",
      "regex": "MY_SECRET_[\\w]+",
      "replacement": "[MY_SECRET:***]",
      "enabled": true
    }
  ]
}
```

---

## ⚠️ 注意事项

1. **白名单** - 添加到白名单的内容不会脱敏
2. **误报** - 可能误报正常文本，检查日志调整规则
3. **性能** - 大量正则匹配可能影响性能
4. **本地存储** - 会话历史仍明文存储（用户可接受）

---

## 📝 版本历史

### v1.0 (2026-03-03)
- 初始版本
- 支持 6 种敏感信息类型
- RAG 和 API 调用前脱敏
- 可配置规则和模式
- 脱敏日志记录

---

*最后更新：2026-03-03*
