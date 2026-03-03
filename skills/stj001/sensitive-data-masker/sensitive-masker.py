#!/usr/bin/env python3
"""
Sensitive Data Masker - 敏感信息智能脱敏器

使用 Microsoft Presidio 进行智能检测，SQLite + LRU 缓存存储映射表。
"""

import sys
import json
import hashlib
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple, List
from collections import OrderedDict

# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════

DATA_DIR = Path.home() / ".openclaw" / "data" / "sensitive-masker"
DB_FILE = DATA_DIR / "mapping.db"
CONFIG_FILE = DATA_DIR / "config.json"
LOG_FILE = DATA_DIR / "masker.log"

DEFAULT_CONFIG = {
    "enabled": True,
    "ttl_days": 7,
    "cache_size": 1000,
    "auto_cleanup": True,
    "cleanup_interval_hours": 1,
    "log_enabled": True,
    "encrypt_storage": False,
    "presidio": {
        "language": "zh",
        "entities": [
            "PHONE_NUMBER",
            "EMAIL_ADDRESS",
            "CREDIT_CARD",
            "PERSON",
            "LOCATION",
            "DATE_TIME",
            "NRP",
            "LOCATION",
            "URL"
        ],
        "custom_patterns": True
    }
}

# 颜色输出
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

# ═══════════════════════════════════════════════════════════════
# Presidio 检测器
# ═══════════════════════════════════════════════════════════════

class PresidioDetector:
    """使用 Microsoft Presidio 进行智能检测。"""
    
    def __init__(self):
        try:
            from presidio_analyzer import AnalyzerEngine, PatternRecognizer
            
            self.analyzer = AnalyzerEngine()
            self._load_custom_patterns()
            self.enabled = True
        except ImportError:
            print(f"{YELLOW}⚠️  Presidio 未安装，使用基础正则检测{NC}")
            print(f"{YELLOW}提示：pip install presidio-analyzer presidio-anonymizer{NC}")
            self.enabled = False
    
    def _load_custom_patterns(self):
        """加载自定义检测模式。"""
        from presidio_analyzer import PatternRecognizer
        
        # API Key 检测器
        class APIKeyRecognizer(PatternRecognizer):
            def load_patterns(self):
                from presidio_analyzer import Pattern
                return [
                    Pattern(name="sk_key", regex=r"sk-[a-zA-Z0-9]{20,}", score=0.9),
                    Pattern(name="github_token", regex=r"ghp_[a-zA-Z0-9]{36}", score=0.9),
                    Pattern(name="aliyun_ak", regex=r"LTAI[a-zA-Z0-9]{12,}", score=0.9),
                ]
        
        # 密码检测器
        class PasswordRecognizer(PatternRecognizer):
            def load_patterns(self):
                from presidio_analyzer import Pattern
                return [
                    Pattern(name="password", regex=r"(?i)(password|passwd|pwd)[=:\s]+[\w@#$%^&*!]+", score=0.8),
                    Pattern(name="db_url", regex=r"(mongodb|mysql|postgresql|redis)://[^\s'\"]+", score=0.9),
                ]
        
        # 注册自定义检测器
        self.analyzer.registry.add_recognizer(APIKeyRecognizer())
        self.analyzer.registry.add_recognizer(PasswordRecognizer())
    
    def detect(self, text: str, language: str = 'zh') -> list:
        """检测敏感信息。"""
        if not self.enabled:
            # 降级到基础正则
            return self._regex_detect(text)
        
        try:
            results = self.analyzer.analyze(
                text=text,
                language=language,
                entities=[
                    "PHONE_NUMBER",
                    "EMAIL_ADDRESS",
                    "CREDIT_CARD",
                    "PERSON",
                    "LOCATION",
                    "URL",
                    "API_KEY",
                    "PASSWORD",
                    "DB_URL"
                ]
            )
            return list(results)
        except Exception as e:
            print(f"{YELLOW}⚠️  Presidio 检测失败：{e}{NC}")
            return self._regex_detect(text)
    
    def _regex_detect(self, text: str) -> list:
        """基础正则检测（降级方案）。"""
        import re
        
        patterns = [
            (r"(?i)(password|passwd|pwd)[=:\s]+[\w@#$%^&*!]+", "PASSWORD"),
            (r"sk-[a-zA-Z0-9]{20,}", "API_KEY"),
            (r"(mongodb|mysql|postgresql|redis)://[^\s'\"]+", "DB_URL"),
            (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "EMAIL_ADDRESS"),
            (r"1[3-9]\d{9}", "PHONE_NUMBER"),
        ]
        
        results = []
        for pattern, entity_type in patterns:
            for match in re.finditer(pattern, text):
                results.append(type('Result', (), {
                    'entity_type': entity_type,
                    'start': match.start(),
                    'end': match.end(),
                    'score': 0.8
                })())
        
        return results

# ═══════════════════════════════════════════════════════════════
# SQLite + LRU 缓存存储
# ═══════════════════════════════════════════════════════════════

class SensitiveMappingStore:
    """SQLite + LRU 缓存存储敏感数据映射。"""
    
    def __init__(self, db_path: Path = None, cache_size: int = 1000):
        if db_path is None:
            db_path = DB_FILE
        
        self.db_path = db_path
        self.cache_size = cache_size
        self.cache = OrderedDict()
        self._init_db()
    
    def _init_db(self):
        """初始化数据库。"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mappings (
                mask_id TEXT PRIMARY KEY,
                original TEXT NOT NULL,
                data_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                usage_count INTEGER DEFAULT 0
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_expires_at ON mappings(expires_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_data_type ON mappings(data_type)')
        
        conn.commit()
        conn.close()
    
    def add(self, original: str, data_type: str, ttl_days: int = 7) -> str:
        """添加映射，返回 mask_id。"""
        # 生成 mask_id
        mask_id = hashlib.sha256(
            f"{original}{time.time()}".encode()
        ).hexdigest()[:16]
        
        expires_at = datetime.now() + timedelta(days=ttl_days)
        
        # 写入数据库
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO mappings 
            (mask_id, original, data_type, expires_at, usage_count)
            VALUES (?, ?, ?, ?, 0)
        ''', (mask_id, original, data_type, expires_at.isoformat()))
        
        conn.commit()
        conn.close()
        
        # 更新缓存
        self.cache[mask_id] = {
            'original': original,
            'expires_at': expires_at
        }
        
        # LRU 淘汰
        if len(self.cache) > self.cache_size:
            self.cache.popitem(last=False)
        
        return mask_id
    
    def get(self, mask_id: str) -> Optional[str]:
        """获取原始数据（带缓存）。"""
        # 查缓存
        if mask_id in self.cache:
            data = self.cache[mask_id]
            if data['expires_at'] > datetime.now():
                # 移到末尾（LRU）
                self.cache.move_to_end(mask_id)
                return data['original']
            else:
                # 过期删除
                del self.cache[mask_id]
        
        # 查数据库
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT original, expires_at FROM mappings
            WHERE mask_id = ? AND expires_at > ?
        ''', (mask_id, datetime.now().isoformat()))
        
        result = cursor.fetchone()
        
        if result:
            # 增加使用计数
            cursor.execute('''
                UPDATE mappings SET usage_count = usage_count + 1
                WHERE mask_id = ?
            ''', (mask_id,))
            conn.commit()
            
            # 更新缓存
            self.cache[mask_id] = {
                'original': result[0],
                'expires_at': datetime.fromisoformat(result[1])
            }
            
            # LRU 淘汰
            if len(self.cache) > self.cache_size:
                self.cache.popitem(last=False)
            
            conn.close()
            return result[0]
        
        conn.close()
        return None
    
    def cleanup_expired(self) -> int:
        """清理过期数据。"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM mappings WHERE expires_at < ?
        ''', (datetime.now().isoformat(),))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        # 清理缓存
        now = datetime.now()
        expired_keys = [
            k for k, v in self.cache.items()
            if v['expires_at'] < now
        ]
        for key in expired_keys:
            del self.cache[key]
        
        return deleted
    
    def get_stats(self) -> dict:
        """获取统计信息。"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute('SELECT COUNT(*) FROM mappings')
        total = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute('''
            SELECT data_type, COUNT(*) 
            FROM mappings 
            GROUP BY data_type
        ''')
        by_type = dict(cursor.fetchall())
        
        # 即将过期
        cursor.execute('''
            SELECT COUNT(*) FROM mappings
            WHERE expires_at < ?
        ''', ((datetime.now() + timedelta(hours=24)).isoformat(),))
        expiring_soon = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total": total,
            "by_type": by_type,
            "expiring_soon": expiring_soon,
            "cache_size": len(self.cache)
        }

# ═══════════════════════════════════════════════════════════════
# 脱敏器
# ═══════════════════════════════════════════════════════════════

class ChannelSensitiveMasker:
    """Channel 级敏感信息脱敏器。"""
    
    def __init__(self):
        self.detector = PresidioDetector()
        self.store = SensitiveMappingStore()
    
    def mask_message(self, text: str, language: str = 'zh') -> Tuple[str, list]:
        """脱敏消息。"""
        # 检测
        results = self.detector.detect(text, language)
        
        # 建立映射并脱敏
        replacements = []
        masked_text = text
        
        # 按位置倒序排序，避免替换后位置变化
        sorted_results = sorted(results, key=lambda r: r.start, reverse=True)
        
        for result in sorted_results:
            original = text[result.start:result.end]
            entity_type = result.entity_type
            
            # 生成 mask_id
            mask_id = self.store.add(original, entity_type)
            
            # 创建脱敏标记
            masked = f"[{entity_type}:{mask_id}]"
            
            # 替换
            masked_text = masked_text[:result.start] + masked + masked_text[result.end:]
            
            replacements.append({
                'type': entity_type,
                'original': original[:20] + '...' if len(original) > 20 else original,
                'masked': masked,
                'mask_id': mask_id,
                'score': getattr(result, 'score', 0.8)
            })
        
        # 反转 replacements 顺序（因为我们是倒序处理）
        replacements.reverse()
        
        return masked_text, replacements
    
    def restore_message(self, text: str) -> str:
        """还原消息。"""
        import re
        
        def replace_match(match):
            full = match.group(0)
            # [TYPE:mask_id]
            parts = full.split(':')
            if len(parts) >= 2:
                mask_id = parts[1].rstrip(']')
                original = self.store.get(mask_id)
                if original:
                    return original
            return full
        
        # 匹配 [TYPE:mask_id] 格式
        pattern = r'\[[A-Z_]+:[a-f0-9]{16}\]'
        return re.sub(pattern, replace_match, text)

# ═══════════════════════════════════════════════════════════════
# 命令行工具
# ═══════════════════════════════════════════════════════════════

def test_mask_restore(text: str):
    """测试脱敏和还原。"""
    masker = ChannelSensitiveMasker()
    
    print(f"\n{BLUE}原始消息:{NC}")
    print(f"  {text}\n")
    
    # 脱敏
    masked, replacements = masker.mask_message(text)
    print(f"{GREEN}脱敏后:{NC}")
    print(f"  {masked}\n")
    
    if replacements:
        print(f"{YELLOW}检测到 {len(replacements)} 个敏感信息:{NC}")
        for r in replacements:
            print(f"  - {r['type']}: {r['original']} → {r['masked']} (置信度：{r['score']})")
        print()
    
    # 还原
    restored = masker.restore_message(masked)
    print(f"{BLUE}还原后:{NC}")
    print(f"  {restored}\n")
    
    # 验证
    if restored == text:
        print(f"{GREEN}✅ 还原成功！{NC}")
    else:
        print(f"{YELLOW}⚠️  还原结果与原始不一致{NC}")
        print(f"  原始：{text}")
        print(f"  还原：{restored}")
    print()

def show_stats():
    """显示统计信息。"""
    store = SensitiveMappingStore()
    stats = store.get_stats()
    
    print(f"\n{BLUE}📊 敏感数据映射统计:{NC}")
    print(f"  总数：{stats['total']}")
    print(f"  缓存大小：{stats['cache_size']}")
    print(f"  即将过期（24h 内）: {stats['expiring_soon']}")
    
    if stats['by_type']:
        print(f"\n  按类型:")
        for data_type, count in stats['by_type'].items():
            print(f"    - {data_type}: {count}")
    
    print()

def cleanup():
    """清理过期数据。"""
    store = SensitiveMappingStore()
    deleted = store.cleanup_expired()
    print(f"{GREEN}✅ 清理了 {deleted} 条过期数据{NC}\n")

def clear_all():
    """清空所有映射。"""
    import sys
    response = input(f"{YELLOW}⚠️  确定要清空所有敏感数据映射吗？(yes/no): {NC}")
    if response.lower() == 'yes':
        DB_FILE.unlink(missing_ok=True)
        print(f"{GREEN}✅ 已清空{NC}\n")
    else:
        print("已取消\n")

# ═══════════════════════════════════════════════════════════════
# OpenClaw Hook 集成
# ═══════════════════════════════════════════════════════════════

def on_message_received(message: dict) -> dict:
    """
    OpenClaw Hook: 消息接收时脱敏。
    
    Args:
        message: 消息对象 {'context': {'content': '...'}}
    
    Returns:
        脱敏后的消息对象
    """
    masker = ChannelSensitiveMasker()
    
    content = message.get('context', {}).get('content', '')
    if not content:
        return message
    
    # 脱敏
    masked, replacements = masker.mask_message(content)
    
    # 更新消息
    message['context']['content'] = masked
    
    # 记录
    if replacements:
        message['_masked'] = {
            'count': len(replacements),
            'types': list(set([r['type'] for r in replacements]))
        }
    
    return message

def before_task_execution(context: dict) -> dict:
    """
    OpenClaw Hook: 任务执行前还原。
    
    Args:
        context: 任务上下文
    
    Returns:
        还原后的上下文
    """
    masker = ChannelSensitiveMasker()
    
    for key, value in context.items():
        if isinstance(value, str):
            context[key] = masker.restore_message(value)
    
    return context

# ═══════════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"{YELLOW}用法:{NC}")
        print(f"  {sys.argv[0]} test <text>      # 测试脱敏/还原")
        print(f"  {sys.argv[0]} stats            # 显示统计")
        print(f"  {sys.argv[0]} cleanup          # 清理过期")
        print(f"  {sys.argv[0]} clear            # 清空所有")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'test' and len(sys.argv) >= 3:
        test_mask_restore(' '.join(sys.argv[2:]))
    elif cmd == 'stats':
        show_stats()
    elif cmd == 'cleanup':
        cleanup()
    elif cmd == 'clear':
        clear_all()
    else:
        print(f"{RED}❌ 未知命令：{cmd}{NC}")
        sys.exit(1)
