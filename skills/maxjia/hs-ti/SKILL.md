---
name: hs-ti
version: 2.1.1
description: 云瞻威胁情报查询技能。查询IP地址、域名、URL、文件哈希等是否在云瞻威胁情报库中。支持中英文双语。/ Hillstone Threat Intelligence Skill. Query IP addresses, domains, URLs, and file hashes in the Hillstone threat intelligence database. Supports Chinese/English bilingual.
metadata: {"openclaw":{"emoji":"🔍","commands":["/threat-check","/hs-ti","/threat","/hs-ti cn","/hs-ti en"],"aliases":["hs-ti","threat-intel","威胁情报","云瞻"],"title":"Hillstone Threat Intelligence"}}
---

# 云瞻威胁情报查询技能 / Hillstone Threat Intelligence Skill

**功能**：查询IP地址、域名、URL、文件哈希等是否在云瞻威胁情报库中。
**Features**: Query IP addresses, domains, URLs, and file hashes in the Hillstone threat intelligence database.

## 新功能 / New Features (v2.0.0)

### 中文 / Chinese
- **IOC类型自动识别**：自动识别IP、域名、URL、哈希等IOC类型
- **智能缓存**：内置缓存机制，显著提升查询性能
- **结果格式化**：支持文本、JSON、表格等多种格式
- **结果导出**：支持导出为CSV、JSON、HTML、Markdown等格式
- **日志记录**：完整的操作日志记录
- **错误处理**：完善的错误处理和重试机制
- **类型提示**：完整的类型提示，提高代码可维护性

### English
- **Automatic IOC Type Detection**: Automatically detect IP, domain, URL, hash, and other IOC types
- **Smart Caching**: Built-in caching mechanism for significantly improved query performance
- **Result Formatting**: Support for text, JSON, table, and other formats
- **Result Export**: Support for exporting to CSV, JSON, HTML, Markdown, and other formats
- **Logging**: Complete operation logging
- **Error Handling**: Comprehensive error handling and retry mechanisms
- **Type Hints**: Full type annotations for better code maintainability

## 语言切换 / Language Switching

默认语言：英文 / Default Language: English

切换到中文 / Switch to Chinese:
```
/hs-ti cn
```

切换到英文 / Switch to English:
```
/hs-ti en
```

## 配置 / Configuration

需要创建 `config.json` 文件并配置有效的 API Key：
You need to create a `config.json` file and configure a valid API Key:

1. 复制 `config.example.json` 为 `config.json`
   Copy `config.example.json` to `config.json`

2. 在 `config.json` 中填入你的 API Key
   Fill in your API Key in `config.json`:

```json
{
  "api_key": "your-api-key-here",
  "api_url": "https://ti.hillstonenet.com.cn",
  "timeout": 30,
  "max_retries": 3,
  "retry_delay": 1,
  "cache_enabled": true,
  "cache_ttl": 3600
}
```

**配置参数说明 / Configuration Parameters**:
- `api_key`: 云瞻威胁情报API密钥 / Hillstone Threat Intelligence API Key (必需/required)
- `api_url`: API地址 / API URL (可选/optional, 默认/default: https://ti.hillstonenet.com.cn)
- `timeout`: 请求超时时间（秒）/ Request timeout in seconds (可选/optional, 默认/default: 30)
- `max_retries`: 最大重试次数 / Maximum retry attempts (可选/optional, 默认/default: 3)
- `retry_delay`: 重试延迟（秒）/ Retry delay in seconds (可选/optional, 默认/default: 1)
- `cache_enabled`: 是否启用缓存 / Enable cache (可选/optional, 默认/default: true)
- `cache_ttl`: 缓存有效期（秒）/ Cache time-to-live in seconds (可选/optional, 默认/default: 3600)

## 使用示例 / Usage Examples

### 中文 / Chinese
```
/threat-check 45.74.17.165
/threat-check deli.ydns.eu  
/threat-check 45.74.17.165,deli.ydns.eu,www.blazingelectricz.com
/threat-check -a 45.74.17.165
/threat-check -a deli.ydns.eu
```

### English
```
/threat-check 45.74.17.165
/threat-check deli.ydns.eu  
/threat-check 45.74.17.165,deli.ydns.eu,www.blazingelectricz.com
/threat-check -a 45.74.17.165
/threat-check -a deli.ydns.eu
```

## 高级接口 / Advanced API

### 中文 / Chinese
使用 `-a` 参数调用高级接口，获取更详细的威胁情报信息：
```
/threat-check -a 45.74.17.165
```

高级接口提供的信息包括：
- **基本信息**: 网络、运营商、地理位置、国家、省份、城市、经纬度
- **ASN信息**: 自治系统信息
- **威胁类型**: 判定恶意类型
- **细分标签**: 威胁相关标签
- **DNS记录**: 可逆DNS记录（最多10个）
- **域名信息**: 当前域名和历史域名（最多10个）
- **文件关联**: 下载文件、引用文件、相关文件的哈希值（仅恶意文件）
- **端口信息**: 开放端口、应用协议、应用名称、版本

### English
Use `-a` parameter to call the advanced API and get more detailed threat intelligence:
```
/threat-check -a 45.74.17.165
```

Advanced API provides:
- **Basic Info**: Network, carrier, location, country, province, city, coordinates
- **ASN Info**: Autonomous System information
- **Threat Type**: Malicious type classification
- **Tags**: Threat-related tags
- **DNS Records**: Reverse DNS records (up to 10)
- **Domain Info**: Current and historical domains (up to 10)
- **File Associations**: Downloaded, referenced, and related file hashes (malicious only)
- **Port Info**: Open ports, application protocols, application names, versions

## 支持的IOC类型 / Supported IOC Types

### 中文 / Chinese
- **IP地址**: 自动识别并查询 `/api/ip/reputation`
- **域名**: 自动识别并查询 `/api/domain/reputation`  
- **URL**: 自动识别并查询 `/api/url/reputation`
- **文件哈希**: 支持 MD5/SHA1/SHA256，查询 `/api/file/reputation`

### English
- **IP Address**: Automatically detect and query `/api/ip/reputation`
- **Domain**: Automatically detect and query `/api/domain/reputation`
- **URL**: Automatically detect and query `/api/url/reputation`
- **File Hash**: Supports MD5/SHA1/SHA256, query `/api/file/reputation`

## 特性 / Features

### 中文 / Chinese
- **批量查询**: 支持逗号分隔的多个IOC同时查询
- **实时响应时间统计**: 显示本次调用的平均、最大、最小、中位数响应时间
- **累计性能监控**: 跟踪所有历史调用的性能指标
- **详细威胁信息**: 返回威胁类型、可信度、具体分类等信息
- **智能缓存**: 内置缓存机制，显著提升查询性能
- **结果格式化**: 支持文本、JSON、表格等多种格式
- **结果导出**: 支持导出为CSV、JSON、HTML、Markdown等格式
- **日志记录**: 完整的操作日志记录
- **错误处理**: 完善的错误处理和重试机制

### English
- **Batch Query**: Support for querying multiple IOCs at once (comma-separated)
- **Real-time Response Time Statistics**: Display average, max, min, and median response times for current query
- **Cumulative Performance Monitoring**: Track performance metrics for all historical queries
- **Detailed Threat Information**: Return threat type, credibility, and specific classification
- **Smart Caching**: Built-in caching mechanism for significantly improved query performance
- **Result Formatting**: Support for text, JSON, table, and other formats
- **Result Export**: Support for exporting to CSV, JSON, HTML, Markdown, and other formats
- **Logging**: Complete operation logging
- **Error Handling**: Comprehensive error handling and retry mechanisms

## 响应时间统计说明 / Response Time Statistics

### 中文 / Chinese
每次查询都会显示详细的性能统计：
- **单次查询**: 显示本次调用的响应时间
- **批量查询**: 显示本次批量的统计（平均/最大/最小/中位数）
- **累计统计**: 显示所有历史调用的累计统计和总调用次数

### English
Each query displays detailed performance statistics:
- **Single Query**: Display response time for current call
- **Batch Query**: Display statistics for current batch (avg/max/min/median)
- **Cumulative Statistics**: Display cumulative statistics and total call count for all historical queries

## 依赖 / Dependencies

### 中文 / Chinese
- Python 3.8+
- 山石网科云瞻威胁情报 API 访问权限
- 本技能使用Python标准库，无需额外安装依赖

### English
- Python 3.8+
- Hillstone Threat Intelligence API access permission
- This skill uses Python standard library, no additional dependencies required

## API 端点 / API Endpoints

### 中文 / Chinese
#### 普通信誉接口 / Reputation API
- IP 查询: `/api/ip/reputation?key={ip}`
- 域名查询: `/api/domain/reputation?key={domain}`  
- URL 查询: `/api/url/reputation?key={url}`
- 文件哈希查询: `/api/file/reputation?key={hash}`

#### 高级详情接口 / Advanced Detail API
- IP 高级查询: `/api/ip/detail?key={ip}`
- 域名高级查询: `/api/domain/detail?key={domain}`
- URL 高级查询: `/api/url/detail?key={url}`
- 文件哈希高级查询: `/api/file/detail?key={hash}`

### English
#### Reputation API
- IP Query: `/api/ip/reputation?key={ip}`
- Domain Query: `/api/domain/reputation?key={domain}`
- URL Query: `/api/url/reputation?key={url}`
- File Hash Query: `/api/file/reputation?key={hash}`

#### Advanced Detail API
- IP Advanced Query: `/api/ip/detail?key={ip}`
- Domain Advanced Query: `/api/domain/detail?key={domain}`
- URL Advanced Query: `/api/url/detail?key={url}`
- File Hash Advanced Query: `/api/file/detail?key={hash}`

## 故障排除 / Troubleshooting

### 中文 / Chinese
- **API Key无效**: 确保使用有效的云瞻API Key
- **网络连接问题**: 检查能否访问 `https://ti.hillstonenet.com.cn`
- **查询超时**: 默认超时30秒，可在config.json中调整timeout参数
- **编码问题**: 确保系统支持UTF-8编码
- **日志查看**: 日志文件位于 `~/.openclaw/logs/hs_ti.log`

### English
- **Invalid API Key**: Ensure you are using a valid Hillstone API Key
- **Network Connection Issues**: Check if you can access `https://ti.hillstonenet.com.cn`
- **Query Timeout**: Default timeout is 30 seconds, can be adjusted in config.json
- **Encoding Issues**: Ensure your system supports UTF-8 encoding
- **Log Viewing**: Log file is located at `~/.openclaw/logs/hs_ti.log`
