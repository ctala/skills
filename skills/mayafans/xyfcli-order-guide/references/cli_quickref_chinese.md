# XYFCLI命令快速参考（中文版）

## 基本命令结构

```bash
xyfcli [分组] [命令] [选项]
```

## 命令分组

### `order` - 订单相关命令
```bash
xyfcli order [命令] [选项]
```

### `shop` - 产品和客户信息
```bash
xyfcli shop [命令] [选项]
```

### `config` - 配置管理
```bash
xyfcli config [命令] [选项]
```

## `order`命令参考

### `order place` - 完成下单流程
**用途**：完成下单流程，生成订单页面 URL

```bash
xyfcli order place \
  --dealer-code <客户编号> \
  --dealer-name <客户名称> \
  --sales-code <业务员编号> \
  --product-codes <商品编号列表> \
  --departure-base <发货基地> \
  --destination <收货地址> \
  [--quantities <数量列表>] \
  [--transport-mode <运输方式>] \
  [--pickup-mode <提货方式>] \
  [--receiver-name <收货人姓名>] \
  [--receiver-phone <收货人电话>] \
  [--cover-images <封面图 URL>] \
  [--json]
```

**参数**：
- `--dealer-code`, `-dealer`：客户编号（必需）
- `--dealer-name`, `-name`：客户名称（必需）
- `--sales-code`, `-sales`：业务员编号（必需）
- `--product-codes`, `-products`：商品编号列表，逗号分隔（必需）
- `--departure-base`, `-base`：发货基地（必需）
- `--destination`, `-dest`：收货地址（必需）
- `--transport-mode`, `-transport`：运输方式，默认汽运（可选）
- `--pickup-mode`, `-pickup`：提货方式，默认统派车（客户付款）（可选）
- `--receiver-name`, `-receiver`：收货人姓名（可选）
- `--receiver-phone`, `-phone`：收货人电话（可选）
- `--cover-images`, `-images`：商品封面图 URL 列表，逗号分隔（可选）
- `--quantities`, `-q`：商品数量列表，逗号分隔，与商品一一对应（可选）
- `--json`, `-j`：输出 JSON 格式（可选）

**示例**：
```bash
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000" \
  -q "5" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
```

```bash
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000,ABC123456789" \
  -q "5,3" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
```

```bash
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000" \
  -q "10" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓" \
  -transport "铁路" \
  -pickup "自提" \
  -receiver "张三" \
  -phone "13800138000"
```

```bash
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000" \
  -q "20" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓" \
  -images "https://example.com/image1.jpg,https://example.com/image2.jpg" \
  -j
```


## `shop`命令参考

### `shop getproducturibydesc` - 通过产品描述查询产品URI
**用途**：通过产品描述查询产品信息的 URI 地址

```bash
xyfcli shop getproducturibydesc --description <产品描述> [--limit <数量限制>]
```

**参数**：
- `--description`, `-desc`：产品描述（必需）
- `--limit`, `-limit`：返回数量限制，-1 表示返回所有结果（可选，默认：5）
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
xyfcli shop getproducturibydesc -desc "含量 45% 13-5-27" -limit 5
```

### `shop getproductdetailbyuri` - 通过URI获取产品详情
**用途**：通过产品 URI 地址获取产品完整描述

```bash
xyfcli shop getproductdetailbyuri --uri <产品URI> [--offset <偏移量>] [--limit <数量限制>]
```

**参数**：
- `--uri`, `-uri`：产品 URI 地址（必需）
- `--offset`, `-offset`：偏移量（可选，默认：0）
- `--limit`, `-limit`：返回数量限制（可选，默认：-1）
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
xyfcli shop getproductdetailbyuri -uri "viking://resources/products/xxx.md" -offset 0 -limit -1
```

### `shop getgoodsinfo` - 通过产品编号查询商品信息
**用途**：通过产品编号查询商品信息（排除 AI 幻觉）

```bash
xyfcli shop getgoodsinfo <产品编码>
```

**参数**：
- `产品编码`：产品编号（必需，位置参数）
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
xyfcli shop getgoodsinfo "Y163U1305276020000"
```

### `shop getsalercode` - 获取业务员信息
**用途**：获取业务员信息，包含业务员编号和姓名等信息（从配置文件读取 token）

```bash
xyfcli shop getsalercode
```

**参数**：
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
xyfcli shop getsalercode
```

### `shop getdealercode` - 获取客户编号列表
**用途**：通过业务员编号获取客户编号列表

```bash
xyfcli shop getdealercode <业务员编号>
```

**参数**：
- `业务员编号`：业务员编号（必需，位置参数）
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
xyfcli shop getdealercode "EZB2019063"
```

### `shop getproductlist` - 获取可购买产品清单
**用途**：通过客户编号和产品编号验证客户端是否有权限购买此产品，并获取可购买产品清单

```bash
xyfcli shop getproductlist --dealer-code <客户编号> --search-value <产品编码或关键词>
```

**参数**：
- `--dealer-code`, `-dealercode`：客户编号（必需）
- `--search-value`, `-search`：产品编号（精确验证）或空格分隔的关键词（模糊查询）（必需）
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
# 精确验证：确认客户是否有权购买此产品`nxyfcli shop getproductlist -dealercode "J620522007" -search "Y163U1305276020000"`n`n# 模糊查询：查找客户可购买的 45% 含量产品`nxyfcli shop getproductlist -dealercode "J620522007" -search "45%"
```

### `shop getdeliverybase` - 获取发货基地列表
**用途**：通过客户编号和产品编号获取发货基地列表

```bash
xyfcli shop getdeliverybase --search-value <产品编码或关键词> --dealer-code <客户编号>
```

**参数**：
- `--product-code`, `-productcode`：产品编号（必需）
- `--dealer-code`, `-dealercode`：客户编号（必需）
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
xyfcli shop getdeliverybase -productcode "Y68000500000023100" -dealercode "J620522007"
```

### `shop getdealeraddresses` - 获取客户收货地址
**用途**：通过客户编号获取客户设置好的收货地址

```bash
xyfcli shop getdealeraddresses <客户编号>
```

**参数**：
- `客户编号`：客户编号（必需，位置参数）
- `--json`, `-j`：输出JSON格式（可选）

**示例**：
```bash
xyfcli shop getdealeraddresses "J620522007"
```

## 参数简写对照表

| 完整参数 | 简写 | 描述 |
|----------|------|------|
| `--description` | `-desc` | 产品描述用于搜索 |
| `--product-codes` | `-pc` | 产品编码，逗号分隔 |
| `--quantities` | `-q` | 数量，逗号分隔 |
| `--product-index` | `-pi` | 产品索引（0开始） |
| `--dealer-index` | `-di` | 客户索引（0开始） |
| `--base-index` | `-bi` | 发货基地索引（0开始） |
| `--address-index` | `-ai` | 地址索引（0开始） |
| `--address` | `-addr` | 直接地址 |
| `--json` | `-j` | JSON输出格式 |
| `--dealer-code` | `-dealer` | 客户编码（用于 order 命令） |
| `--dealer-code` | `-dealercode` | 客户编号（用于 shop 命令） |
| `--dealer-name` | `-name` | 客户名称 |
| `--sales-code` | `-sales` | 销售员编码 |
| `--departure-base` | `-base` | 发货基地 |
| `--destination` | `-dest` | 收货地址 |
| `--cover-images` | `-images` | 商品封面图 URL 列表，逗号分隔 |
| `--limit` | `-limit` | 返回数量限制 |
| `--uri` | `-uri` | 产品 URI 地址 |
| `--offset` | `-offset` | 偏移量 |
| `--product-code` | `-productcode` | 产品编号 |

## 常用命令组合

### 1. 先查客户再下单
```bash
# 步骤1：获取业务员编号（从配置）
xyfcli shop getsalercode
# 从输出中获取业务员编号，例如 EZB2019063

# 步骤2：查看该业务员的可用客户
xyfcli shop getdealercode "EZB2019063"
```

### 2. 产品搜索并下单
```bash
# 从JSON输出提取产品编码
# 使用提取的编码下单
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "提取的编码" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市..."
```

### 3. 多产品下单
```bash
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000,Y163U1305276020001" \
  -q "5,3" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓" \
  -transport "汽运" \
  -pickup "统派车" \
  -receiver "牛建建" \
  -phone "18093818192"
```

### 4. 完整信息简单下单
```bash
xyfcli order place \
  -dealer "J620522007" \
  -name "牛建建" \
  -sales "EZB2019063" \
  -products "Y163U1305276020000" \
  -q "5" \
  -base "新洋丰中磷" \
  -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
```

## 输出格式

### 人类可读输出（默认）
```
订单生成成功!
订单页面 URL: http://localhost:8000/static/logistics-route_1.html?customerCode=...
```

### JSON输出（使用`--json`标志）
```json
{
  "步骤": {
    "产品搜索": { ... },
    "产品详情": { ... },
    "产品验证": { ... },
    "销售员信息": { ... },
    "客户选择": { ... },
    "产品可用性": { ... },
    "发货基地": { ... },
    "地址": { ... }
  },
  "最终订单": {
    "订单数据": { ... },
    "订单结果": { ... },
    "url": "http://localhost:8000/..."
  }
}
```

## 帮助命令

### 通用帮助
```bash
xyfcli --help
```

### 订单命令帮助
```bash
xyfcli order --help
xyfcli order place --help
```

### 店铺命令帮助
```bash
xyfcli shop --help
xyfcli shop dealer-list --help
xyfcli shop product-list --help
xyfcli shop product-info --help
```

## 索引使用说明

所有索引参数都是**0开始**：

- `--product-index 0`：搜索结果中的第一个产品
- `--dealer-index 0`：列表中的第一个客户
- `--base-index 0`：第一个发货基地
- `--address-index 0`：客户地址列表中的第一个地址

**使用前检查索引**：
```bash
# 对于客户
xyfcli shop dealer-list
```

## 数量格式

### 单个产品
```bash
-q "5"  # 单个产品数量5
```

### 多个产品
```bash
# 3个产品，数量分别为10、5、3
-pc "P1,P2,P3" -q "10,5,3"

# 必须匹配长度：3个产品编码 = 3个数量
```

### 默认数量
如果未指定`--quantities`：
- 单个产品：数量1
- 多个产品：所有数量默认为1

## 常用选项

### `--json` (`-j`)
- 输出JSON格式，便于自动化处理
- 包含详细的步骤信息
- 错误调试时有用

### 详细输出
某些命令支持详细输出（检查每个命令的`--help`）

## 环境变量

CLI可能使用以下环境变量：
- `XYFCLI_API_BASE`：API基础URL
- `XYFCLI_SESSION`：认证用的会话Cookie
- `XYFCLI_DEBUG`：启用调试输出

## 快速提示

1. **始终检查`--help`** 获取命令特定选项
2. **使用简写** 在交互会话中更快输入
3. **验证索引** 再运行命令
4. **使用`--json`调试** 遇到错误时
5. **先用单个产品测试** 再进行多产品订单
6. **检查数量匹配** 对于多个产品
7. **验证地址** 再提交订单
8. **保持会话Cookie有效** 用于认证
