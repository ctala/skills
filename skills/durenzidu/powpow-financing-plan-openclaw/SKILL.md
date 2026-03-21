# PowPow 投融资技能 – SKILL.md

本文件描述 PowPow 投融资技能的结构、字段含义、与两个目标平台（OpenClaw、ClawHub）的对应关系，以及校验与上传的要点，便于团队对接与自动化上传。以下内容为固定参考格式，便于直接在文档中查看与对比。

## 1. 概要
- 技能名称（Display name）：PowPow 投融资技能
- 内部标识（Skill-name / slug）: powpow_investment_openclaw
- 版本（Version）：1.0.0
- 语言（Language）：zh-CN
- 描述（My skill / description）：将 PowPow 的融资计划转化为可对话的投融资技能，便于对接、检索与对话场景使用

## 2. 文件结构与字段映射
- OpenClaw 版本 JSON（openclaw_skill.json）：核心技能定义，包含结构化章节。
- ClawHub 版本 JSON（clawhub_skill.json）：兼容模板，字段映射到 OpenClaw 的版本。
- README_upload.md：上传使用说明（本文件描述上传步骤、打包要求与验证要点）。
- 其他元数据：如 manifest.json，描述打包内容的清单。

注：自本文件发布起，不再使用 source_hash.sha256 来表示哈希值，哈希校验移至上传前的本地流程或由平台自动完成。

## 3. 结构化字段（核心摘要）
- 项目概述 / 项目概述
  - 项目名称、定位、核心理念、融资轮次、融资金额
- 项目亮点 / 项目亮点
  - PWA、区域服务/本地化场景、商业模式等要点
- 联系方式 / 联系方式
  - 项目负责人、邮箱、体验地址、对接入口

### OpenClaw JSON 对应要点
- skill_id: powpow_investment_openclaw
- name: PowPow 投融资技能
- version: 1.0.0
- language: zh-CN
- structure.sections: 包含三个章节：项目概述、项目亮点、联系方式
- examples: 如输入“展示融资计划概要”得到要点摘要

### ClawHub JSON 对应要点
- clawhub_asset_type: "skill"
- id / name: powpow_investment_openclaw / PowPow 投融资技能
- version: 1.0.0
- language: zh-CN
- content.sections 与 OpenClaw 对应（相同标题、相同文本结构）
- source.file 指向 OpenClaw 的原始 JSON，source.hash 由平台或本地流程提供
- urls: PowPow 的体验与对接入口

## 4. 示例片段（对照 OpenClaw 与 ClawHub）
OpenClaw 的核心 JSON 已在上文草案中给出，简要示例如下：
```
{
  "skill_id": "powpow_investment_openclaw",
  "name": "PowPow 投融资技能",
  "version": "1.0.0",
  "language": "zh-CN",
  "structure": { ... },
  "examples": [ { "input": "展示融资计划概要", "output": "包括：项目概述、项目亮点、联系方式三部分的要点" } ]
}
```
ClawHub 的模板应与之对齐，字段名与层级保持一致，方便跨平台迁移。

## 5. 校验与上传要点
- 本地校验：JSON 语法正确、字段命名一致、分支结构正确。
- 打包要求：将 openclaw_skill.json、clawhub_skill.json、README_upload.md 等放在同一打包根目录下（遵循 manifest.json 里 listing 的路径）。
- 上传前后：在 ClawHub/OpenClaw 的预览/测试中验证对话触发与显示内容的正确性。

## 6. 变更与版本控制
- 版本号遵循语义化版本（MAJOR.MINOR.PATCH）。首次公开可设为 1.0.0，后续如有向后兼容性变更可自增 Minor 或 Patch。
- 每次改动后，请重新打包并提供新的 SKILL.md 以便团队审核。

## 7. 参考文件位置
- OpenClaw JSON：package/openclaw_skill.json
- ClawHub JSON：package/clawhub_skill.json
- 说明文档：package/README_upload.md
- 打包清单：package/manifest.json
- SKILL 文档：package/SKILL.md

如需我把 SKILL.md 直接整合到现有 JSON 的注释中，告诉我你偏好的展示方式（纯文本、或在各字段旁边追加简短注释）。
