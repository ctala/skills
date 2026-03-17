# WordPal · Learn 流程

## Session 状态展示

进入学习前，展示状态摘要：

```
📘 WordPal · 学习模式
🎯 目标：<learning_goal>（如 TOEFL / CET6）
📊 难度：<difficulty_level>（如 III）
📅 今日进度：已学 <today_reviewed_count> / 目标 <daily_target> 词
📋 本轮队列：<pending 数> 新词 + <due 数> 复习词
```

数据来自 `session-context.js --mode learn` 返回的 `data.profile` 和 `data.learn`。

## 执行顺序

1. 用 `data.learn.queue_preview` 作为本轮优先队列。
2. 若 `queue_preview` 为空且 `need_new_words <= 0`，结束本轮。
3. 按 `daily_target` 上限逐题推进：先消费 `queue_preview`，不足时补新词。
4. 补新词（仅 `need_new_words > 0` 时）：
   - 按 `learning_goal + difficulty_level + memory_digest` 生成 **1 个**新词候选
   - 调用 `next-question.js --mode learn --item-type pending --word "<word>" --difficulty-level <I-V> --validate [--last-type <Nk>]`
   - 若 `WORD_REJECTED`，重新生成并重试
5. 对 `queue_preview` 中已有词调用 `next-question.js`：
   - pending：`next-question.js --mode learn --item-type pending --word "<word>" --difficulty-level <I-V> [--last-type <Nk>]`
   - due：`next-question.js --mode learn --item-type due --word "<word>" --status <0-7> [--last-type <Rk>]`
6. 读取 `data.question` 后，按下方"单题输出规范"的 A → B → C 流程出题。题面规则见"题型速查"。
7. 每题反馈后记录题型编号，下一题传入 `--last-type`。
8. 用户暂停或本轮结束时，收集所有 `op_id`，调用 `session-summary.js --mode learn --op-ids "<op1>,<op2>,..."`.

## 题型速查

- **N1 单词释义选择**：直接给目标词，4 选 1 中文/短义项，不额外提示
- **N2 词卡同义词识别**：先展示词卡，再给 4 个简单英文同义/近义选项
- **N3 英文语境猜义**：给一条含目标词的英文句子，让用户猜大意
- **N4 场景选义**：先展示词卡，再判断目标词是否适合某个具体场景
- **N5 固定搭配入门**：先展示词卡，再从多个搭配里选最自然的一项
- **N6 词卡造句**：先展示词卡，再让用户用目标词写 1 句英文句子
- **N7 场景翻译**：先展示词卡，再把中文场景翻成含目标词的英文句子

## 单题输出规范

每道题分三个阶段，顺序固定：

### 阶段 A：出题

```
【<question_type_name>】

[词卡] （仅 reveal_word_card=true）
  单词：xxx | 音标：/xxx/ | 词性：xxx | 中文释义：xxx

[题面] 严格遵守 constraints
```

信息保护：reveal_word_card=false 时禁止泄露中文释义/词性/音标；选择题正确答案位置随机；不给暗示性线索。

### 阶段 B：答题判定

- **B-1 正确** → event=`correct`，调用 `submit-answer.js`，进入 C
- **B-2 跳过**（"跳过/会了/斩词"）→ event=`skip`，调用 `submit-answer.js`，进入 C
- **B-3 答错** → 子流程：
  1. 展示正确答案+解析（1-2 句）+ 补充词卡（若阶段 A 未展示）。不调用 submit-answer.js
  2. 引导确认："记住了吗？"
  3. 判定：用户主动复述/造句/说"懂了" → `remembered_after_hint`；仅被动确认"嗯/好"或说"记不住" → `wrong`
  4. 调用 `submit-answer.js`，进入 C

### 阶段 C：答后反馈

submit-answer.js 返回后展示：

```
[结果] ✅正确 / ❌答错 / 💡提示后记住 / ⏭️已跳过
[解析] 仅 correct 时可补充扩展用法（可选，1 句）
[词卡] 仅 correct 且阶段 A 未展示时补充
[状态] <status_emoji>（status N）| 下次复习：<next_review>
[进度] <已完成数> / <总数>
```

## 参数调整

- 难度显式调整（"调到 IV"）→ `profile.js set --difficulty-level IV`
- 难度相对反馈："太难了" → 降 1 级，"太简单了" → 升 1 级，钳制 I..V
- 难度调整后必须按顺序：①`profile.js set` → ②重跑 `session-context.js --mode learn` → ③清空未出题新词候选 → ④按新难度重新生成
- 每日目标：用户明确说"每天学 X 个词"时 → `profile.js set --daily-target X`（1-100）
- 未调整参数时不重跑 session-context
