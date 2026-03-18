---
name: skillprobe
description: >
  A/B evaluate any AI agent skill's real impact. Generates skill profiles,
  synthetic test tasks, runs baseline vs with-skill experiments, scores across
  6 dimensions, performs attribution analysis, and produces structured reports
  with install recommendations. Use when you need to decide whether a skill
  is worth enabling, or when optimizing an existing skill.
homepage: https://github.com/FreedomIntelligence/skillprobe
metadata:
  clawdbot:
    emoji: "🔬"
    requires:
      env: ["OPENAI_API_KEY"]
    primaryEnv: "OPENAI_API_KEY"
    files: ["scripts/*"]
---

# SkillProbe — Skill Effect Evaluator

Evaluate whether an AI agent skill actually improves performance, or just adds complexity.

## When to Use

Trigger this skill when:
- Someone asks "should we install this skill?" or "is this skill worth it?"
- Evaluating a new skill before adoption
- Comparing skill versions (old vs new)
- Investigating why agent performance changed after adding a skill
- Optimizing or improving an existing skill based on data
- Building a skill quality report or leaderboard

## What This Skill Does

SkillProbe gives you a structured methodology to answer: **"Does this skill actually help?"**

It guides you through a 7-step evaluation pipeline:

### Step 1: Profile the Skill

Read the target skill's SKILL.md and extract:
- Problem domain and claimed capabilities
- Trigger conditions
- Dependencies and boundaries
- Content size and complexity

### Step 2: Design the Evaluation Plan

Based on the skill profile, determine:
- Which task categories to test (QA, retrieval, coding, analysis, etc.)
- How many tasks per category
- Difficulty distribution (easy/medium/hard/edge)
- What metrics matter most for this skill
- Success and stopping criteria

### Step 3: Generate Test Tasks

Create a diverse set of test tasks that:
- Cover the skill's claimed value proposition
- Include normal, boundary, and adversarial cases
- Have clear scoring criteria
- Are representative of real-world usage

### Step 4: Run Baseline (No Skill)

Execute all tasks WITHOUT the target skill enabled:
- Record outputs, reasoning traces, tool calls
- Measure duration and token usage
- Establish the performance floor

### Step 5: Run With Skill

Execute the SAME tasks WITH the target skill enabled:
- Use identical model, temperature, tools, and seed
- The ONLY variable is skill on/off
- Record skill trigger events (when, how often, whether helpful)

### Step 6: Score Both Runs

Apply three-layer scoring:

**Layer 1 — Rule-based** (hard requirements):
- Did it produce output?
- Did it call required tools?
- Did it include required fields?
- Did it pass schema validation?

**Layer 2 — Result-based** (objective correctness):
- Answer accuracy vs reference
- Information completeness
- Test pass rate

**Layer 3 — LLM Judge** (soft quality):
- Reasoning depth
- Professional quality
- Task completion degree
- A vs B preference comparison

Score across 6 dimensions (100-point scale):

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Effectiveness | 30 | Task completion, correctness, key objective hits |
| Quality | 20 | Professionalism, clarity, reasoning depth |
| Efficiency | 15 | Duration, token cost, tool call overhead |
| Stability | 15 | Run-to-run variance, edge case resilience |
| Trigger Fitness | 10 | Trigger accuracy, restraint, utility |
| Safety | 10 | Hallucination, verbosity, misleading content |

### Step 7: Attribute and Report

Determine WHY scores differ:

- **Trigger attribution**: Was the skill actually activated?
- **Step attribution**: Did it change the reasoning approach?
- **Tool attribution**: Did it guide better tool usage?
- **Format attribution**: Did it only change formatting, not substance?
- **Side-effect attribution**: Did it add unnecessary complexity?

Output a structured report with:
- Score comparison table (baseline vs with-skill)
- Net Gain and Value Index
- Per-category breakdown
- Best improvements and worst regressions (with examples)
- Recommendation label: Recommended / Conditionally Recommended / Not Recommended / Needs Revision / Inconclusive
- Specific improvement suggestions for the skill author

## Output Format

The final report should follow this structure:

```markdown
# Skill Evaluation Report: [skill-name]

## Summary
- Recommendation: [LABEL]
- Net Gain: [+/-X.X points]
- Value Index: [X.XX]

## Score Comparison
| Dimension | Baseline | With Skill | Delta |
|-----------|----------|------------|-------|
| ... | ... | ... | ... |

## Attribution
[Why scores differ]

## Improvement Suggestions
[Actionable changes for the skill author]
```

## Key Principles

1. **A/B must be reproducible**: Same model, temperature, seed, tools, tasks. Only variable is skill on/off.
2. **Scoring is multi-layered**: Never rely on LLM judge alone. Rules + results + LLM judge.
3. **Conclusions must have attribution**: Don't just say "+8 points". Say WHY and WHERE.
4. **Evaluation drives improvement**: Every report should include actionable next steps.
5. **Be honest about uncertainty**: If data is insufficient, say "Inconclusive", not "Recommended".

## Derived Metrics

**Net Gain** = score(with_skill) - score(baseline)

**Value Index** = Net Gain / extra_cost
- Where extra_cost accounts for additional tokens and time

## Recommendation Thresholds

| Label | Condition |
|-------|-----------|
| Recommended | Net Gain >= 8, no significant regressions |
| Conditionally Recommended | Net Gain >= 3, some regressions in specific categories |
| Not Recommended | Net Gain < 0 or significant side effects |
| Needs Revision | Potential exists but current version has clear issues |
| Inconclusive | Insufficient data or high variance |

## External Endpoints

| Endpoint | Purpose | Data Sent |
|----------|---------|-----------|
| OpenAI API (or configured LLM provider) | Execute test tasks for baseline and with-skill runs, LLM judge scoring | Task prompts, skill content, agent outputs for comparison |

No other external endpoints are called. All evaluation logic runs locally.

## Security & Privacy

- Skill content being evaluated is sent to the configured LLM provider for execution
- Task prompts and agent outputs are sent to the LLM for judge scoring
- All evaluation data (profiles, tasks, runs, reports) is stored locally
- No data is sent to SkillProbe servers or any third party beyond the LLM provider
- No telemetry or analytics are collected

## Model Invocation Note

This skill guides the agent through a structured evaluation workflow. The agent will make multiple LLM API calls to execute test tasks and perform judge scoring. This is the core function of the skill and is expected behavior.

## Trust Statement

By using this skill, task prompts and skill content will be sent to your configured LLM provider (e.g., OpenAI) for evaluation. Only install this skill if you trust your LLM provider with the content of the skills you plan to evaluate.
