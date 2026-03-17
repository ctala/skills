# online-shopping

## name
online-shopping

## description
全球在线购物指南 Skill，帮助用户根据商品类别推荐合适的国际电商平台，提供平台对比和购物决策建议。支持 Amazon、eBay、AliExpress、Temu、Shein、Walmart、Target 等主要平台。

## triggers
- "我想在亚马逊买东西"
- "哪个平台买...比较好"
- "推荐一个买...的网站"
- "Amazon 和 eBay 哪个好"
- "对比...平台"
- "全球购物推荐"
- "海淘推荐"
- "买...去哪个网站"

## workflow
1. 识别用户购物需求（商品类别、预算、时效要求等）
2. 调用 online-shopping.py 获取平台推荐或对比
3. 呈现推荐结果，包含推荐理由、最佳选择、注意事项
4. 如需详细指导，引用 references/ 下的文档

## usage
```bash
# 根据商品推荐平台
python3 online-shopping.py recommend <商品名称/类别>

# 列出支持的类别
python3 online-shopping.py categories

# 对比两个平台
python3 online-shopping.py compare <平台1> <平台2>
```

## data files
- `data/platforms.json` - 平台信息（特点、适用地区、优势类别）
- `data/categories.json` - 商品类别映射
- `data/regions.json` - 地区推荐配置

## references
- `references/platform-guide.md` - 平台详细指南
- `references/shopping-tips.md` - 购物技巧和注意事项
