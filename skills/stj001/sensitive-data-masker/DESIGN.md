# 敏感信息智能脱敏系统 - 完整设计方案

## 🎯 项目概述

在 OpenClaw Gateway 层实现智能敏感信息检测与脱敏，保护用户隐私数据，同时支持本地还原执行任务。

---

## 🏗️ 架构设计

### 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户消息                              │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Channel 插件 (Feishu/Telegram/etc)          │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│           OpenClaw Gateway (message:received)           │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│        Sensitive Data Masker Hook (拦截点)              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  1. Presidio 智能检测 (NLP + 规则)                │  │
│  │  2. SQLite + 缓存存储映射                          │  │
│  │  3. 脱敏处理                                       │  │
│  └───────────────────────────────────────────────────┘  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              脱敏后的消息                                │
│         "[PASSWORD:xxx]，帮我配置数据库"                 │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              发送给 LLM API (安全)                       │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              LLM 返回结果                                │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│         任务执行前从映射表还原敏感数据                   │
│         "password=MySecret123，帮我配置数据库"           │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              使用还原后的数据执行任务                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 技术选型

### 1️⃣ 检测引擎：Microsoft Presidio

**理由**：
- ✅ 微软开源，企业级品质
- ✅ NLP + 规则双重检测
- ✅ 100% 本地执行
- ✅ 支持 50+ 种语言
- ✅ MIT 许可，完全免费

**检测能力**：
- 人名、地址、电话、邮箱
- 信用卡号、身份证号
- 密码、API Key、Token
- 数据库连接串
- 自定义检测器

### 2️⃣ 存储方案：SQLite + LRU 缓存

**理由**：
- ✅ 查询速度 O(log n) vs JSON O(n)
- ✅ 支持索引和事务
- ✅ 自动过期清理
- ✅ 零配置，Python 内置
- ✅ 并发安全

**性能指标**：
- 热数据查询：< 0.1ms（内存缓存）
- 冷数据查询：~0.5ms（SQLite）
- 写入：< 2ms
- 支持：100,000+ 条记录

### 3️⃣ 集成方式：OpenClaw Hook

**事件**：`message:received`

**优势**：
- ✅ 无需修改 Channel 插件
- ✅ 统一处理所有渠道
- ✅ 易于维护和升级

---

## 📦 组件设计

### 组件 1：Presidio 检测器

```python
class PresidioDetector:
    """使用 Microsoft Presidio 进行智能检测。"""
    
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self._load_custom_patterns()
    
    def detect(self, text: str, language='zh') -> list:
        """检测敏感信息。"""
        results = self.analyzer.analyze(
            text=text,
            language=language,
            entities=self.entities
        )
        return results
    
    def _load_custom_patterns(self):
        """加载自定义检测模式（API Key 等）。"""
        # 阿里云 AccessKey
        # GitHub Token
        # 数据库连接串
        # ...
```

### 组件 2：映射表存储

```python
class SensitiveMappingStore:
    """SQLite + LRU 缓存存储。"""
    
    def __init__(self, db_path: str, cache_size: int = 1000):
        self.db_path = db_path
        self.cache = {}
        self.cache_max_size = cache_size
        self._init_db()
    
    def add(self, original: str, data_type: str, ttl_days: int = 7) -> str:
        """添加映射，返回 mask_id。"""
        mask_id = self._generate_id()
        self._write_db(mask_id, original, data_type, ttl_days)
        self.cache[mask_id] = original
        return mask_id
    
    def get(self, mask_id: str) -> Optional[str]:
        """获取原始数据（带缓存）。"""
        if mask_id in self.cache:
            return self.cache[mask_id]
        
        original = self._query_db(mask_id)
        if original:
            self.cache[mask_id] = original
            self._lru_evict()
        return original
    
    def cleanup_expired(self) -> int:
        """清理过期数据。"""
        # DELETE FROM mappings WHERE expires_at < now()
```

### 组件 3：脱敏器

```python
class ChannelSensitiveMasker:
    """Channel 级脱敏器。"""
    
    def __init__(self):
        self.detector = PresidioDetector()
        self.store = SensitiveMappingStore()
    
    def mask_message(self, text: str) -> tuple:
        """脱敏消息。"""
        # 1. 检测
        results = self.detector.detect(text)
        
        # 2. 建立映射并脱敏
        replacements = []
        masked_text = text
        
        for result in results:
            original = text[result.start:result.end]
            mask_id = self.store.add(original, result.entity_type)
            masked = f"[{result.entity_type}:{mask_id}]"
            masked_text = masked_text.replace(original, masked)
            replacements.append(...)
        
        return masked_text, replacements
    
    def restore_message(self, text: str) -> str:
        """还原消息。"""
        # 从映射表还原所有 [TYPE:mask_id] 标记
```

### 组件 4：OpenClaw Hook

```javascript
// handler.js
async function handler(event) {
    if (event.type !== 'message' || event.action !== 'received') {
        return;
    }
    
    const content = event.context.content;
    const masker = new ChannelSensitiveMasker();
    
    // 脱敏
    const [masked, replacements] = masker.mask_message(content);
    
    // 更新事件
    event.context.content = masked;
    
    // 记录日志
    if (replacements.length > 0) {
        console.log(`[sensitive-masker] 脱敏了 ${replacements.length} 个敏感信息`);
    }
}
```

---

## 🗄️ 数据库设计

### 表结构

```sql
CREATE TABLE mappings (
    mask_id TEXT PRIMARY KEY,
    original TEXT NOT NULL,
    data_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    usage_count INTEGER DEFAULT 0
);

CREATE INDEX idx_expires_at ON mappings(expires_at);
CREATE INDEX idx_data_type ON mappings(data_type);
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| **mask_id** | TEXT | 16 位哈希，主键 |
| **original** | TEXT | 原始敏感数据（加密存储） |
| **data_type** | TEXT | 数据类型（PASSWORD, API_KEY 等） |
| **created_at** | TIMESTAMP | 创建时间 |
| **expires_at** | TIMESTAMP | 过期时间（7 天后） |
| **usage_count** | INTEGER | 使用次数（审计用） |

---

## 🔐 安全设计

### 1️⃣ 文件权限

```bash
# 数据库文件
chmod 600 ~/.openclaw/data/sensitive-masker/mapping.db

# 配置文件
chmod 600 ~/.openclaw/config/sensitive-masker.json
```

### 2️⃣ 数据加密

```python
from cryptography.fernet import Fernet

# 加密原始数据
key = load_key()
f = Fernet(key)
encrypted = f.encrypt(original.encode())

# 存储到数据库
cursor.execute('INSERT ... VALUES (?, ?, ...)', (mask_id, encrypted, ...))
```

### 3️⃣ 自动过期

```python
# 后台线程每小时清理
def cleanup_loop():
    while True:
        time.sleep(3600)
        store.cleanup_expired()  # DELETE WHERE expires_at < now()
```

---

## ⚙️ 配置设计

### 配置文件

```json
{
  "enabled": true,
  "ttl_days": 7,
  "cache_size": 1000,
  "auto_cleanup": true,
  "cleanup_interval_hours": 1,
  "log_enabled": true,
  "encrypt_storage": true,
  "presidio": {
    "language": "zh",
    "entities": ["PHONE_NUMBER", "EMAIL_ADDRESS", ...],
    "custom_patterns": true
  }
}
```

### 配置位置

- `~/.openclaw/config/sensitive-masker.json` - 主配置
- `~/.openclaw/data/sensitive-masker/` - 数据目录

---

## 📊 性能优化

### 1️⃣ LRU 缓存

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached(mask_id: str) -> str:
    return store.get(mask_id)
```

### 2️⃣ 批量写入

```python
def batch_add(self, items: list):
    cursor.executemany('INSERT ...', items)
    conn.commit()
```

### 3️⃣ 异步清理

```python
thread = threading.Thread(target=cleanup_loop, daemon=True)
thread.start()
```

---

## 🧪 测试策略

### 单元测试

```python
def test_mask_password():
    masker = ChannelSensitiveMasker()
    masked, _ = masker.mask_message("password=MySecret123")
    assert "[PASSWORD:" in masked

def test_restore():
    masker = ChannelSensitiveMasker()
    masked, _ = masker.mask_message("password=123")
    restored = masker.restore_message(masked)
    assert restored == "password=123"

def test_cache_performance():
    store = SensitiveMappingStore()
    # 测试缓存命中率 > 90%
```

### 集成测试

```python
def test_hook_integration():
    # 模拟 OpenClaw 事件
    event = {
        'type': 'message',
        'action': 'received',
        'context': {'content': 'password=123'}
    }
    
    # 调用 Hook
    handler(event)
    
    # 验证脱敏
    assert "[PASSWORD:" in event.context.content
```

### 性能测试

```python
def test_performance():
    masker = ChannelSensitiveMasker()
    
    # 测试 1000 次查询
    start = time.time()
    for i in range(1000):
        masker.mask_message(f"password=secret{i}")
    elapsed = time.time() - start
    
    assert elapsed < 1.0  # < 1ms/次
```

---

## 📝 部署清单

### 1️⃣ 安装依赖

```bash
pip install presidio-analyzer presidio-anonymizer
python -m spacy download zh_core_web_sm
```

### 2️⃣ 创建 Hook

```bash
mkdir -p ~/.openclaw/workspace/hooks/sensitive-masker
# 复制 handler.js, masker-wrapper.py 等
```

### 3️⃣ 启用 Hook

```bash
openclaw hooks enable sensitive-masker
openclaw hooks check
```

### 4️⃣ 测试

```bash
# 发送测试消息
# "我的密码是 MySecret123"

# 查看日志
# [sensitive-masker] 脱敏了 1 个敏感信息
```

---

## 🎯 关键设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| **检测引擎** | Presidio | 业界领先，NLP+ 规则 |
| **存储方案** | SQLite + 缓存 | 性能 + 零配置 |
| **集成方式** | OpenClaw Hook | 无需改插件 |
| **TTL** | 7 天 | 平衡安全和可用 |
| **加密存储** | 可选 | 性能 vs 安全 |
| **缓存大小** | 1000 | 内存占用 < 1MB |

---

## 📋 未来扩展

1. **支持图片 OCR 脱敏**
2. **支持结构化数据（JSON/XML）**
3. **多租户隔离**
4. **审计日志导出**
5. **自定义脱敏策略**

---

*设计完成时间：2026-03-03*
