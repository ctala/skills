import json
import urllib.request
import urllib.error
import urllib.parse
import os
import time
import logging
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Callable
from dataclasses import dataclass, asdict, field
from datetime import datetime
from functools import wraps, lru_cache
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock


class IOCType(Enum):
    """IOC类型枚举"""
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    HASH = "hash"
    UNKNOWN = "unknown"


class QueryResult(Enum):
    """查询结果枚举"""
    MALICIOUS = "malicious"
    BENIGN = "benign"
    UNKNOWN = "unknown"


@dataclass
class PerformanceStats:
    """性能统计数据类"""
    avg_ms: float
    max_ms: int
    min_ms: int
    median_ms: int
    total_calls: int


@dataclass
class IOCQueryResult:
    """IOC查询结果数据类"""
    ioc: str
    ioc_type: str
    result: Dict[str, Any]
    response_time_ms: int
    success: bool
    error: Optional[str] = None


class YunzhanError(Exception):
    """云瞻威胁情报基础异常"""
    pass


class YunzhanConfigError(YunzhanError):
    """配置错误"""
    pass


class YunzhanAPIError(YunzhanError):
    """API错误"""
    def __init__(self, message: str, status_code: int = None, 
                 response_data: Dict = None):
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)


class YunzhanNetworkError(YunzhanError):
    """网络错误"""
    pass


class YunzhanTimeoutError(YunzhanError):
    """超时错误"""
    pass


class IOCTypeDetector:
    """IOC类型自动检测器"""
    
    IPV4_PATTERN = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    
    IPV6_PATTERN = re.compile(
        r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|'
        r'^(?:(?:[0-9a-fA-F]{1,4}:){1,7}:|'
        r'(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
        r'(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|'
        r'(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|'
        r'(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|'
        r'(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|'
        r'[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}|'
        r':(?::[0-9a-fA-F]{1,4}){1,7}|'
        r':(?:[0-9a-fA-F]{1,4}:){1,7}|'
        r'fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|'
        r'::(?:ffff(?::0{1,4}){0,1}:){0,1}'
        r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|'
        r'(?:[0-9a-fA-F]{1,4}:){1,4}:'
        r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$'
    )
    
    DOMAIN_PATTERN = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
        r'[a-zA-Z]{2,}$'
    )
    
    URL_PATTERN = re.compile(
        r'^https?://(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
        r'[a-zA-Z]{2,}(?:/[^\s]*)?$'
    )
    
    MD5_PATTERN = re.compile(r'^[a-fA-F0-9]{32}$')
    SHA1_PATTERN = re.compile(r'^[a-fA-F0-9]{40}$')
    SHA256_PATTERN = re.compile(r'^[a-fA-F0-9]{64}$')
    
    @classmethod
    @lru_cache(maxsize=1024)
    def detect(cls, ioc_value: str) -> Optional[str]:
        """自动检测IOC类型（带缓存）"""
        ioc_value = ioc_value.strip()
        
        if cls.IPV4_PATTERN.match(ioc_value) or cls.IPV6_PATTERN.match(ioc_value):
            return IOCType.IP.value
        elif cls.URL_PATTERN.match(ioc_value):
            return IOCType.URL.value
        elif cls.MD5_PATTERN.match(ioc_value):
            return IOCType.HASH.value
        elif cls.SHA1_PATTERN.match(ioc_value):
            return IOCType.HASH.value
        elif cls.SHA256_PATTERN.match(ioc_value):
            return IOCType.HASH.value
        elif cls.DOMAIN_PATTERN.match(ioc_value):
            return IOCType.DOMAIN.value
        
        return IOCType.UNKNOWN.value


def retry_on_failure(max_retries: int = 3, delay: int = 1, 
                    exceptions: tuple = (urllib.error.URLError,)) -> Callable:
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
            raise last_exception
        return wrapper
    return decorator


class YunzhanThreatIntel:
    """云瞻威胁情报查询插件 / Hillstone Threat Intelligence Plugin"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.api_key: Optional[str] = None
        self.api_url: str = "https://ti.hillstonenet.com.cn"
        self.response_times: List[int] = []
        self.language: str = "en"
        self.lang_config_path: Optional[str] = None
        self.cache_enabled: bool = True
        self.cache_ttl: int = 3600
        self.cache: Dict[str, Dict] = {}
        self._cache_lock: Lock = Lock()
        self._response_times_lock: Lock = Lock()
        self.max_retries: int = 3
        self.retry_delay: int = 1
        self.timeout: int = 30
        self.max_workers: int = 5
        self.logger: logging.Logger = self._setup_logger()
        
        self.load_config(config_path)
        self.load_language_config()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('hs-ti')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_dir = Path.home() / '.openclaw' / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / 'hs_ti.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def load_config(self, config_path: Optional[str] = None) -> None:
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
                    if 'api_url' in config:
                        self.api_url = config['api_url'].rstrip('/')
                    if 'timeout' in config:
                        self.timeout = config['timeout']
                    if 'max_retries' in config:
                        self.max_retries = config['max_retries']
                    if 'retry_delay' in config:
                        self.retry_delay = config['retry_delay']
                    if 'cache_enabled' in config:
                        self.cache_enabled = config['cache_enabled']
                    if 'cache_ttl' in config:
                        self.cache_ttl = config['cache_ttl']
                    if 'max_workers' in config:
                        self.max_workers = config['max_workers']
                self.logger.info(f"配置文件加载成功: {config_path}")
            except Exception as e:
                self.logger.error(f"加载配置文件失败: {e}")
        else:
            self.logger.warning(f"配置文件不存在: {config_path}")
    
    def load_language_config(self) -> None:
        """加载语言配置"""
        skill_dir = os.path.dirname(os.path.dirname(__file__))
        self.lang_config_path = os.path.join(skill_dir, "language.json")
        
        if os.path.exists(self.lang_config_path):
            try:
                with open(self.lang_config_path, 'r', encoding='utf-8') as f:
                    lang_config = json.load(f)
                    self.language = lang_config.get('language', 'en')
                self.logger.info(f"语言配置加载成功: {self.language}")
            except Exception as e:
                self.logger.error(f"加载语言配置失败: {e}")
                self.language = 'en'
    
    def save_language_config(self) -> None:
        """保存语言配置"""
        if self.lang_config_path:
            try:
                with open(self.lang_config_path, 'w', encoding='utf-8') as f:
                    json.dump({"language": self.language}, f, indent=2, ensure_ascii=False)
                self.logger.info(f"语言配置保存成功: {self.language}")
            except Exception as e:
                self.logger.error(f"保存语言配置失败: {e}")
    
    def set_language(self, lang: str) -> bool:
        """设置语言"""
        if lang in ['en', 'cn']:
            self.language = lang
            self.save_language_config()
            return True
        return False
    
    def _get_cache_key(self, ioc_value: str, ioc_type: str, advanced: bool) -> str:
        """生成缓存键"""
        data = f"{ioc_value}:{ioc_type}:{advanced}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """检查缓存是否有效"""
        return time.time() - cache_entry['timestamp'] < self.cache_ttl
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """从缓存获取数据（线程安全）"""
        with self._cache_lock:
            if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
                return self.cache[cache_key]['data']
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict) -> None:
        """保存数据到缓存（线程安全）"""
        with self._cache_lock:
            self.cache[cache_key] = {
                'data': data,
                'timestamp': time.time()
            }
    
    def _add_response_time(self, response_time: int) -> None:
        """添加响应时间（线程安全）"""
        with self._response_times_lock:
            self.response_times.append(response_time)
    
    def _cleanup_expired_cache(self) -> int:
        """清理过期缓存"""
        with self._cache_lock:
            current_time = time.time()
            expired_keys = [
                key for key, value in self.cache.items()
                if current_time - value['timestamp'] >= self.cache_ttl
            ]
            for key in expired_keys:
                del self.cache[key]
            return len(expired_keys)
    
    def get_text(self, key: str) -> str:
        """获取当前语言的文本"""
        texts = {
            'en': {
                'api_key_not_configured': 'API key not configured',
                'config_hint': 'Please configure your API key in config.json:\n1. Edit config.json in the hs-ti skill directory\n2. Replace "your-api-key-here" with your actual API key\n3. Restart OpenClaw if needed',
                'request_failed': 'Request failed',
                'invalid_json': 'Invalid JSON response',
                'result_malicious': 'malicious',
                'result_benign': 'benign',
                'result_unknown': 'unknown',
                'language_switched': 'Language switched to',
                'language_switched_to_en': 'Language switched to English',
                'language_switched_to_cn': 'Language switched to Chinese',
                'current_language': 'Current language',
                'default_language': 'Default language: English',
                'switch_to_chinese': 'Switch to Chinese',
                'switch_to_english': 'Switch to English',
                'query_results': 'Query Results',
                'single_query': 'Single Query',
                'batch_query': 'Batch Query',
                'cumulative_stats': 'Cumulative Statistics',
                'response_time': 'Response Time',
                'avg': 'Average',
                'max': 'Maximum',
                'min': 'Minimum',
                'median': 'Median',
                'total_calls': 'Total Calls',
                'threat_type': 'Threat Type',
                'credibility': 'Credibility',
                'ip_address': 'IP Address',
                'domain': 'Domain',
                'url': 'URL',
                'file_hash': 'File Hash',
                'no_results': 'No results found',
                'query_completed': 'Query completed',
                'performance_stats': 'Performance Statistics',
                'current_call': 'Current Call',
                'batch_stats': 'Batch Statistics',
                'total_stats': 'Total Statistics',
                'unknown_ioc_type': 'Unknown IOC type',
                'auto_detected_type': 'Auto-detected type'
            },
            'cn': {
                'api_key_not_configured': 'API密钥未配置',
                'config_hint': '请在config.json中配置您的API密钥：\n1. 编辑hs-ti技能目录下的config.json文件\n2. 将 "your-api-key-here" 替换为您的实际API密钥\n3. 如需要请重启OpenClaw',
                'request_failed': '请求失败',
                'invalid_json': '无效的JSON响应',
                'result_malicious': '恶意',
                'result_benign': '良性',
                'result_unknown': '未知',
                'language_switched': '语言已切换到',
                'language_switched_to_en': '语言已切换到英文',
                'language_switched_to_cn': '语言已切换到中文',
                'current_language': '当前语言',
                'default_language': '默认语言：英文',
                'switch_to_chinese': '切换到中文',
                'switch_to_english': '切换到英文',
                'query_results': '查询结果',
                'single_query': '单次查询',
                'batch_query': '批量查询',
                'cumulative_stats': '累计统计',
                'response_time': '响应时间',
                'avg': '平均',
                'max': '最大',
                'min': '最小',
                'median': '中位数',
                'total_calls': '总调用次数',
                'threat_type': '威胁类型',
                'credibility': '可信度',
                'ip_address': 'IP地址',
                'domain': '域名',
                'url': 'URL',
                'file_hash': '文件哈希',
                'no_results': '未找到结果',
                'query_completed': '查询完成',
                'performance_stats': '性能统计',
                'current_call': '本次调用',
                'batch_stats': '批量统计',
                'total_stats': '累计统计',
                'unknown_ioc_type': '未知的IOC类型',
                'auto_detected_type': '自动识别类型'
            }
        }
        return texts.get(self.language, texts['en']).get(key, key)
    
    def query_ioc(self, ioc_value: str, ioc_type: str = "domain", 
                  advanced: bool = False, use_cache: bool = True) -> Dict[str, Any]:
        """
        查询威胁情报
        
        Args:
            ioc_value: IOC值（域名、IP、URL、哈希等）
            ioc_type: IOC类型（domain/ip/url/hash）
            advanced: 是否使用高级接口
            use_cache: 是否使用缓存
        
        Returns:
            查询结果字典
        """
        if not self.api_key or self.api_key == "your-api-key-here":
            error_msg = self.get_text('api_key_not_configured')
            config_hint = f"\n\n{self.get_text('config_hint')}"
            self.logger.error("API密钥未配置")
            return {"error": error_msg + config_hint}
        
        if use_cache and self.cache_enabled:
            cache_key = self._get_cache_key(ioc_value, ioc_type, advanced)
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                self.logger.info(f"使用缓存结果: {ioc_value}")
                return cached_data
        
        self.logger.info(f"查询IOC: {ioc_value} (类型: {ioc_type}, 高级: {advanced})")
        
        headers = {
            "X-Auth-Token": self.api_key,
            "ACCEPT": "application/json",
            "X-API-Version": "1.0.0",
            "X-API-Language": self.language
        }
        
        type_mapping = {
            "ip": "ip",
            "domain": "domain", 
            "url": "url",
            "hash": "file",
            "md5": "file",
            "sha1": "file",
            "sha256": "file"
        }
        
        endpoint = type_mapping.get(ioc_type.lower(), "domain")
        
        if advanced:
            url = f"{self.api_url}/api/{endpoint}/detail"
        else:
            url = f"{self.api_url}/api/{endpoint}/reputation"
        
        start_time = time.time()
        
        try:
            url_with_params = f"{url}?key={urllib.parse.quote(ioc_value)}"
            request = urllib.request.Request(url_with_params, headers=headers)
            
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response_time_ms = int((time.time() - start_time) * 1000)
                self._add_response_time(response_time_ms)
                
                data = response.read().decode('utf-8')
                result = json.loads(data)
                result['response_time_ms'] = response_time_ms
                
                self.logger.info(f"查询成功: {ioc_value}, 耗时: {response_time_ms}ms")
                
                if use_cache and self.cache_enabled:
                    cache_key = self._get_cache_key(ioc_value, ioc_type, advanced)
                    self._save_to_cache(cache_key, result)
                
                return result
            
        except urllib.error.HTTPError as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            error_msg = f"{self.get_text('request_failed')}: HTTP {e.code} {e.reason}"
            
            try:
                error_body = e.read().decode('utf-8')
                self.logger.error(f"HTTP错误: {ioc_value}, 状态码: {e.code}, 原因: {e.reason}, 响应体: {error_body}")
            except:
                self.logger.error(f"HTTP错误: {ioc_value}, 状态码: {e.code}, 原因: {e.reason}")
            
            return {"error": error_msg, "response_time_ms": response_time_ms, "status_code": e.code}
        except urllib.error.URLError as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            if isinstance(e.reason, TimeoutError):
                error_msg = f"{self.get_text('request_failed')}: Timeout after {self.timeout}s"
                self.logger.error(f"超时错误: {ioc_value}, 超时时间: {self.timeout}s")
            else:
                error_msg = f"{self.get_text('request_failed')}: {str(e)}"
                self.logger.error(f"网络错误: {ioc_value}, 错误详情: {str(e)}")
            return {"error": error_msg, "response_time_ms": response_time_ms}
        except json.JSONDecodeError as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self.logger.error(f"JSON解析失败: {ioc_value}, 错误: {str(e)}")
            return {"error": self.get_text('invalid_json'), "response_time_ms": response_time_ms}
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            error_msg = f"{self.get_text('request_failed')}: {type(e).__name__} - {str(e)}"
            self.logger.error(f"未知错误: {ioc_value}, 异常类型: {type(e).__name__}, 错误: {str(e)}")
            return {"error": error_msg, "response_time_ms": response_time_ms}
    
    def query_ioc_auto(self, ioc_value: str, advanced: bool = False, 
                      use_cache: bool = True) -> Dict[str, Any]:
        """
        自动识别IOC类型的查询
        
        Args:
            ioc_value: IOC值
            advanced: 是否使用高级接口
            use_cache: 是否使用缓存
        
        Returns:
            查询结果字典
        """
        detected_type = IOCTypeDetector.detect(ioc_value)
        
        if detected_type == IOCType.UNKNOWN.value:
            self.logger.warning(f"无法识别IOC类型: {ioc_value}")
            return {
                "error": f"{self.get_text('unknown_ioc_type')}: {ioc_value}",
                "detected_type": IOCType.UNKNOWN.value
            }
        
        self.logger.info(f"{self.get_text('auto_detected_type')}: {detected_type}")
        return self.query_ioc(ioc_value, detected_type, advanced, use_cache)
    
    def batch_query(self, iocs: List[Dict[str, str]], 
                    use_cache: bool = True, concurrent: bool = True) -> Dict[str, Any]:
        """
        批量查询威胁情报
        
        Args:
            iocs: IOC列表，每个元素为 {"value": "ioc_value", "type": "ioc_type"}
            use_cache: 是否使用缓存
            concurrent: 是否使用并发查询（默认True）
        
        Returns:
            包含结果和统计信息的字典
        """
        self.logger.info(f"开始批量查询，共 {len(iocs)} 个IOC，并发: {concurrent}")
        
        results: List[IOCQueryResult] = []
        batch_times: List[int] = []
        
        if concurrent and len(iocs) > 1:
            results = self._batch_query_concurrent(iocs, use_cache)
        else:
            results = self._batch_query_sequential(iocs, use_cache)
        
        batch_times = [r.response_time_ms for r in results]
        batch_stats = self._calculate_stats(batch_times)
        total_stats = self._calculate_stats(self.response_times)
        
        success_count = sum(1 for r in results if r.success)
        failure_count = sum(1 for r in results if not r.success)
        self.logger.info(f"批量查询完成，成功: {success_count}, 失败: {failure_count}")
        
        return {
            "results": [asdict(r) for r in results],
            "batch_stats": asdict(batch_stats),
            "total_stats": asdict(total_stats)
        }
    
    def _batch_query_sequential(self, iocs: List[Dict[str, str]], 
                               use_cache: bool) -> List[IOCQueryResult]:
        """顺序批量查询"""
        results: List[IOCQueryResult] = []
        
        for ioc in iocs:
            ioc_value = ioc["value"]
            ioc_type = ioc.get("type", IOCTypeDetector.detect(ioc_value) or "domain")
            
            result = self.query_ioc(ioc_value, ioc_type, False, use_cache)
            response_time = result.get('response_time_ms', 0)
            
            query_result = IOCQueryResult(
                ioc=ioc_value,
                ioc_type=ioc_type,
                result=result,
                response_time_ms=response_time,
                success='error' not in result,
                error=result.get('error') if 'error' in result else None
            )
            results.append(query_result)
        
        return results
    
    def _batch_query_concurrent(self, iocs: List[Dict[str, str]], 
                                use_cache: bool) -> List[IOCQueryResult]:
        """并发批量查询"""
        results: List[IOCQueryResult] = []
        
        def query_single(ioc: Dict[str, str]) -> IOCQueryResult:
            ioc_value = ioc["value"]
            ioc_type = ioc.get("type", IOCTypeDetector.detect(ioc_value) or "domain")
            
            result = self.query_ioc(ioc_value, ioc_type, False, use_cache)
            response_time = result.get('response_time_ms', 0)
            
            return IOCQueryResult(
                ioc=ioc_value,
                ioc_type=ioc_type,
                result=result,
                response_time_ms=response_time,
                success='error' not in result,
                error=result.get('error') if 'error' in result else None
            )
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_ioc = {
                executor.submit(query_single, ioc): ioc 
                for ioc in iocs
            }
            
            for future in as_completed(future_to_ioc):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    ioc = future_to_ioc[future]
                    self.logger.error(f"查询异常: {ioc['value']}, 错误: {str(e)}")
                    results.append(IOCQueryResult(
                        ioc=ioc['value'],
                        ioc_type=ioc.get('type', 'unknown'),
                        result={"error": str(e)},
                        response_time_ms=0,
                        success=False,
                        error=str(e)
                    ))
        
        return results
    
    def _calculate_stats(self, times: List[int]) -> PerformanceStats:
        """计算统计数据"""
        if not times:
            return PerformanceStats(avg_ms=0, max_ms=0, min_ms=0, median_ms=0, total_calls=0)
        
        avg_ms = round(sum(times) / len(times), 2)
        max_ms = max(times)
        min_ms = min(times)
        sorted_times = sorted(times)
        median_ms = sorted_times[len(sorted_times) // 2]
        total_calls = len(times)
        
        return PerformanceStats(avg_ms=avg_ms, max_ms=max_ms, min_ms=min_ms, 
                              median_ms=median_ms, total_calls=total_calls)
    
    def validate_api_key(self) -> bool:
        """验证API密钥是否有效配置"""
        return bool(self.api_key and self.api_key != "your-api-key-here")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        if not self.response_times:
            return {
                "total_queries": 0,
                "avg_response_time_ms": 0,
                "max_response_time_ms": 0,
                "min_response_time_ms": 0
            }
        
        return {
            "total_queries": len(self.response_times),
            "avg_response_time_ms": round(sum(self.response_times) / len(self.response_times), 2),
            "max_response_time_ms": max(self.response_times),
            "min_response_time_ms": min(self.response_times)
        }
    
    def clear_cache(self) -> None:
        """清空缓存"""
        with self._cache_lock:
            self.cache.clear()
        self.logger.info("缓存已清空")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self._cache_lock:
            valid_entries = sum(1 for entry in self.cache.values() 
                              if self._is_cache_valid(entry))
            return {
                "total_entries": len(self.cache),
                "valid_entries": valid_entries,
                "expired_entries": len(self.cache) - valid_entries,
                "cache_enabled": self.cache_enabled,
                "cache_ttl": self.cache_ttl
            }
    
    def cleanup_cache(self) -> int:
        """清理过期缓存，返回清理的条目数"""
        expired_count = self._cleanup_expired_cache()
        if expired_count > 0:
            self.logger.info(f"清理了 {expired_count} 个过期缓存条目")
        return expired_count


yunzhan_intel = YunzhanThreatIntel()
