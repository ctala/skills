---
name: ocas-praxis
description: >
  Bounded behavioral refinement loop. Records outcomes, extracts micro-lessons,
  consolidates into capped active behavior shifts, and generates debriefs.
---

# Praxis

Praxis improves future agent behavior through a bounded refinement loop. It records outcomes, extracts lessons from repeated patterns, consolidates them into a small active set of behavior shifts, and produces auditable debriefs.

Praxis is not a diary, general memory system, or self-rewriting identity layer. It is a bounded behavioral refinement loop.

## When to use

- Record a task outcome, failure, success, or correction
- Extract lessons from repeated patterns
- Review or manage active behavior shifts
- Generate the current runtime brief (active shifts only)
- Produce a debrief explaining what changed and why

## When not to use

- General knowledge storage — use Elephas
- Preference tracking — use Taste
- One-off trivia or domain facts
- Broad autobiographical summaries
- Silent personality mutation

## Core promise

Turn repeated patterns into bounded, auditable behavior shifts. Only active shifts influence runtime. Every shift traces back to recorded events.

## Commands

- `praxis.event.record` — record a completed event or outcome with evidence
- `praxis.lesson.extract` — derive micro-lessons from recorded events
- `praxis.shift.propose` — propose a new behavior shift from lessons
- `praxis.shift.list` — list all shifts with status
- `praxis.shift.activate` — activate a proposed shift (enforces cap)
- `praxis.shift.expire` — expire or reject a shift with reason
- `praxis.runtime.brief` — generate runtime brief with active shifts only
- `praxis.debrief.generate` — produce a plain-language debrief
- `praxis.status` — event count, active shifts, cap usage, last debrief

## Core loop

1. Record event → 2. Extract lessons (if pattern detected) → 3. Propose shift → 4. Activate (if cap allows) → 5. Generate debrief

## Hard constraints

- No autonomous identity rewriting
- No silent safety boundary changes
- No unlimited behavior rule accumulation
- Only active shifts influence runtime
- Maximum 12 active shifts (configurable)
- Every shift must trace to recorded events

## Capping and consolidation rules

Default cap: 12 active shifts. When at cap and a new shift is proposed: merge overlapping shifts, replace a weaker shift, or reject the new shift. No duplicate or contradictory active shifts.

## Runtime injection rules

The runtime brief is a compact list of active shifts only. Target: 3-12 items. Imperative, behavior-facing, free of historical clutter. Not a narrative log.

## Support file map

- `references/data_model.md` — Event, MicroLesson, BehaviorShift, Debrief schemas
- `references/lesson_rules.md` — when to extract lessons, when not to
- `references/runtime_rules.md` — runtime brief format and injection rules
- `references/debrief_templates.md` — debrief structure and tone

## Storage layout

```
.praxis/
  config.json
  events.jsonl
  lessons.jsonl
  shifts.jsonl
  debriefs.jsonl
  decisions.jsonl
  reports/
```

## Validation rules

- Every active shift traces to at least one event
- Active shift count does not exceed cap
- Runtime brief contains only active shifts
- Debriefs are plain-language and audit-friendly
