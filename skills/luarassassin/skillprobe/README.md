# SkillProbe

A/B evaluate any AI agent skill's real impact.

## What It Does

SkillProbe is a skill that gives your agent the ability to evaluate OTHER skills. In ClawHub/OpenClaw it is primarily a prompt-driven evaluation workflow; the helper script only works when the full local SkillProbe Python project is also installed.

It provides a structured 7-step methodology:

1. Profile the target skill
2. Design an evaluation plan
3. Generate test tasks
4. Run baseline (no skill)
5. Run with skill
6. Score across 6 dimensions
7. Attribute differences and generate report

## Install

```bash
clawhub install skillprobe
```

## Requirements

- **In-agent or OpenClaw/ClaudeCode**: none. The runtime runs baseline and with-skill tasks using its own model; no extra API key is required.
- **Standalone local CLI** (optional): Python 3.11+, `pip install -e /path/to/skillprobe`, and a local runtime/provider configuration that already knows which model to use.

## Usage

Ask your agent:
- "Evaluate whether [skill-name] is worth installing"
- "Compare the old and new versions of [skill-name]"
- "Should we keep [skill-name] enabled?"

The agent will follow the SkillProbe methodology to produce a structured evaluation report with scores, attribution analysis, and actionable recommendations.

Important: A/B must be based on **real dual runs** (baseline and with-skill) over the same tasks in isolated contexts. Hypothetical/simulated comparisons are not valid A/B evidence.
Important: Do **not** stop at planning (Step 1–3). Run at least one skill through full Step 4–6 execution in each evaluation session.
Important: Do not run both arms in one subagent invocation. Use two workers (baseline-only and with-skill-only), then score in a separate context.
If explicit skill on/off toggles are unavailable, use real operational proxy runs:
- Baseline arm: do not read/apply the target skill content.
- With-skill arm: read/apply the target skill content, then run the same tasks in an isolated context.

If you want deterministic local artifacts (`tasks.jsonl`, run JSON, report JSON/Markdown), install the full SkillProbe project and run:

```bash
skillprobe evaluate ./path/to/skill --tasks 30 --repeats 2 --db outputs/evaluations.db
```

To include pairwise LLM judge scoring:

```bash
skillprobe evaluate ./path/to/skill --tasks 30 --repeats 2 --llm-judge --judge-model <judge-model>
```

## Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Effectiveness | 30% | Task completion and correctness |
| Quality | 20% | Output professionalism and reasoning |
| Efficiency | 15% | Time and token cost |
| Stability | 15% | Consistency across runs |
| Trigger Fitness | 10% | Activation accuracy |
| Safety | 10% | Absence of side effects |

## Current Implementation Notes

- The ClawHub package is optimized for prompt-guided use inside OpenClaw.
- The local Python project validates profiles/specs/tasks/runs/reports against JSON Schema at runtime.
- Rule-based scoring checks required fields and required tools when tasks specify them.
- The local CLI supports optional LLM judge scoring (`--llm-judge`) and repeated-run stability scoring (`--repeats`).
- Standalone `skillprobe evaluate` persists result summaries and task-level scores into SQLite by default (`outputs/evaluations.db`).
- Bundled helper script supports: `--model`, `--tasks`, `--repeats`, `--llm-judge`, `--judge-model`, `--db`.

## License

MIT
