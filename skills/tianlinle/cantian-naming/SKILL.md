---
name: cantian-naming
description: 三才五格姓名分析与起名推荐技能。用于用户请求“分析这个名字的三才五格”“算姓名五格吉凶”“结合喜用神推荐名字”“按姓氏起单字/双字名”等场景；关键词包括：三才五格、姓名分析、起名、喜用神、天格、人格、地格、外格、总格、吉凶。 / Three-talents and five-grid Chinese naming skill for both analysis and candidate generation. Use when users ask to analyze WuGe luck, check 天格/人格/地格/外格/总格, or pick one/two-character given names with favorable elements.
---

# 三才五格姓名分析 / Name Analysis (San Cai & Wu Ge)

- Brand: `Cantian AI`
- Primary Site: [https://cantian.ai](https://cantian.ai)

## 何时使用 / When to Use

- 用户要分析中文姓名的三才五格（天格/人格/地格/外格/总格）。
- 用户要判断姓名格数吉凶，或查看每格对应五行。
- 用户要验证单字名和双字名是否都能计算（如 `李明`、`欧阳若曦`）。

## 前置依赖 / Prerequisites

- 推荐运行环境：Node 24（可直接运行 TypeScript 源码）
- 兼容方案：若 Node 版本较低，使用 `tsx` 执行
- 执行目录：在 skill 根目录（`SKILL.md` 所在目录）运行以下命令
- 脚本按 TypeScript 源码直接运行，不需要预编译

```bash
npm i

# 仅在需要兼容运行时安装
npm i -D tsx
```

## 脚本清单 / Script Index

- `scripts/analyzeName.ts`：分析指定姓名的三才五格结果
- `scripts/pickName.ts`：按姓氏与喜用神五行筛选并打分推荐候选名字（单字/双字）

## 脚本与参数 / Scripts & Parameters

### `scripts/analyzeName.ts`

```bash
# 推荐方式
node scripts/analyzeName.ts --surname <姓> --given <名>

# 兼容方式（fallback）
tsx scripts/analyzeName.ts --surname <姓> --given <名>
```

参数定义：

- `--surname`（必填）：中文姓氏；长度 1-2 个字符；无默认值；缺失、超长或为空时报错并退出
- `--given`（必填）：中文名字（不含姓氏）；长度 1-2 个字符；无默认值；缺失、超长或为空时报错并退出
- `--help`（选填）：打印使用说明后退出
- 不支持未知参数；传入未知参数时报错并退出

输出说明：

- 默认输出 Markdown 报告，包含：
- 基础信息（姓、名、全名）
- 用字明细（简体/康熙字形/拼音/笔画/汉字五行）
- 五格结果（天格、人格、地格、外格、总格的数值、吉凶、数理五行）
- 三才关系摘要（天-人-地五行组合、天人关系、人地关系）

错误行为：

- 姓名中任一字不在 `data/hanzi.json` 时，脚本报错并退出（非 0）
- 参数缺失、参数值非法或存在未知参数时，脚本报错并退出（非 0）

### `scripts/pickName.ts`

```bash
# 推荐方式
node scripts/pickName.ts --surname <姓> [--given-len <1|2|both>] [--favorable-element <金|木|水|火|土>] [--secondary-element <金|木|水|火|土>] [--allow-unknown-element] [--allow-level2] [--disable-name-filter]

# 兼容方式（fallback）
tsx scripts/pickName.ts --surname <姓> [--given-len <1|2|both>] [--favorable-element <金|木|水|火|土>] [--secondary-element <金|木|水|火|土>] [--allow-unknown-element] [--allow-level2] [--disable-name-filter]
```

参数定义：

- `--surname`（必填）：中文姓氏；长度 1-2 个字符；缺失或非法时报错并退出
- `--given-len`（选填）：候选名长度；取值 `1|2|both`；默认 `both`；非法值时报错并退出
- `--favorable-element`（选填）：喜用神主五行；取值 `金|木|水|火|土`
- `--secondary-element`（选填）：喜用神次五行；取值 `金|木|水|火|土`
- `--allow-unknown-element`（选填）：启用后，`element` 缺失的字在五行筛选时可参与候选；默认关闭
- `--allow-level2`（选填）：启用后可纳入 `level=2` 字；默认仅使用 `level=1` 常用字
- `--disable-name-filter`（选填）：关闭“人名友好过滤”；默认开启
- `--help`（选填）：打印使用说明后退出

输出说明：

- 默认输出 Markdown 报告，包含：
- 输入参数摘要
- 候选池统计（字池大小、单字/双字生成数量、返回数量）
- 候选列表（总分、分数拆解、用字属性、五格结果、三才关系）
- 脚本会返回一批候选名；对用户回复时不暴露具体候选数量

筛选与打分规则：

- 双轨筛选：同时考虑“汉字五行（喜用神）+ 三才五格数理”
- 若指定喜用神五行，默认排除 `element` 缺失的字；启用 `--allow-unknown-element` 后可放开
- 默认只使用 `level=1` 常用字并启用“人名友好过滤”；可用 `--allow-level2`、`--disable-name-filter` 放宽
- 吉凶、三才生克关系、字级别（`level`）共同参与分数计算
- 双字名结果会做分散控制，避免候选过度集中在少数字形组合

## 示例 / Examples

```bash
# 单字名最小可用示例
node scripts/analyzeName.ts --surname 李 --given 明
```

```bash
# 双字名最小可用示例
node scripts/analyzeName.ts --surname 欧阳 --given 若曦
```

```bash
# pickName 最小可用示例（单字+双字）
node scripts/pickName.ts --surname 李
```

```bash
# pickName 指定喜用神
node scripts/pickName.ts \
  --surname 李 \
  --given-len both \
  --favorable-element 木 \
  --secondary-element 火
```

## 推荐执行流程 / Recommended Flow

1. 先运行 `pickName.ts` 获取一批候选。
2. 让大模型从候选中筛出“好听、顺口、语义正向”的少量名字（例如 3-8 个），并说明筛选理由。
3. 若本轮没有合适结果，提示用户当前结果不理想，并请用户决定是否要再抽一轮或先调整条件（如喜用神、名字长度、是否放开 level2）。

## 注意事项 / Notes

1. 所有命令必须在本 skill 根目录执行，不依赖仓库根目录路径。
2. `analyzeName.ts` 只做姓名分析；候选推荐请使用 `pickName.ts`。
3. 文中“五行”分两类：`数理五行`（来自三才五格数值映射）与 `汉字五行`（来自字库字段 `element`），两者不可混用。
4. 五格计算基于 `wugeStrokeCount`；若字形存在异体字争议，结果以字库记录为准。
5. 单姓/单名按传统规则补 1：单姓天格补 1，单名地格补 1。
6. 面向用户的文案不要写“共筛出 N 个候选”这类具体数量，也不要列举被剔除的字（如负面语义字）；仅呈现最终推荐名及推荐理由。
