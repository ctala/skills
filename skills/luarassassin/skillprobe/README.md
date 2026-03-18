# SkillProbe

A/B evaluate any AI agent skill's real impact.

## What It Does

SkillProbe is a skill that gives your agent the ability to evaluate OTHER skills. It provides a structured 7-step methodology:

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

- `OPENAI_API_KEY` (or any LLM provider key supported by litellm)

## Usage

Ask your agent:
- "Evaluate whether [skill-name] is worth installing"
- "Compare the old and new versions of [skill-name]"
- "Should we keep [skill-name] enabled?"

The agent will follow the SkillProbe methodology to produce a structured evaluation report with scores, attribution analysis, and actionable recommendations.

## Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Effectiveness | 30% | Task completion and correctness |
| Quality | 20% | Output professionalism and reasoning |
| Efficiency | 15% | Time and token cost |
| Stability | 15% | Consistency across runs |
| Trigger Fitness | 10% | Activation accuracy |
| Safety | 10% | Absence of side effects |

## License

MIT
