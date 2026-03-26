---
name: build-working-memory
description: "Use this skill to set up or manage a working memory system for an AI agent project. Triggers include: any mention of 'agent memory', 'working memory', 'session memory', 'persistent memory', 'memory system', or requests to help an agent remember context across sessions. Also use when the user wants to add continuity, recall, or long-term memory to an agent, LLM app, or chatbot — even if they describe it as 'context management', 'state persistence', 'conversation history', or 'knowledge base for my agent'. If the user asks how to make an agent 'remember things', 'pick up where it left off', 'maintain context', or 'not forget between sessions', use this skill. Covers both initial setup (scaffolding the memory files and scripts) and ongoing operations (loading, writing, curating, and retrieving memory). Do NOT use for vector databases, RAG pipelines, or embedding-based retrieval — this skill is file-based and markdown-native."
---

# Working Memory System for AI Agents

A file-based memory architecture that gives AI agents continuous identity across sessions. Instead of flat context dumps, the system uses layered retrieval — the agent loads only what it needs, when it needs it, within a token budget.

## When to use this skill

- **Scaffolding**: The user wants to add a memory system to a new or existing agent project.
- **Customizing**: The user has a memory system and wants to modify the schema, retrieval logic, or curation workflow.
- **Debugging**: Memory loading is too slow, too expensive, or missing context.
- **Operating**: The user wants help writing session summaries, curating long-term memory, or managing threads.

## Architecture overview

```
project-root/
├── MEMORY.md                  # Curated long-term memory (active / fading / archived tiers)
├── memory/
│   ├── resumption.md          # First-person handoff note for next session
│   ├── threads.md             # Ongoing topics with state and momentum
│   ├── state.json             # Machine-readable ephemeral state (fast orientation)
│   ├── index.md               # Daily log index for retrieval at scale
│   ├── archive.md             # Demoted long-term memories
│   └── YYYY-MM-DD.md          # Raw session logs (episodic, journal-style)
├── loader.py                  # Four-phase retrieval (orient → anchor → context → deep recall)
└── writer.py                  # End-of-session persistence
```

Each file has a distinct role. Never collapse them — the separation is the system's core strength.

| File | Purpose | When loaded |
|------|---------|-------------|
| `state.json` | Fast machine-readable orientation (timestamps, flags, counters) | Always first, every session |
| `resumption.md` | First-person handoff note — subjective continuity bridge | Always second, every session |
| `MEMORY.md` | Curated long-term facts, patterns, preferences | Phase 3, when time gap ≥ 2h |
| `threads.md` | Active topics with position, decisions, open questions | Phase 3, matched to user's message |
| `YYYY-MM-DD.md` | Raw session logs — episodic, append-only | Phase 4, on-demand retrieval |
| `index.md` | Lookup table mapping dates to topics/threads | Phase 4, when daily logs exceed ~30 |
| `archive.md` | Demoted memories — searchable, recoverable | Phase 4, when archived topics resurface |

## Step 1: Scaffold the memory files

Run the scaffolding script. It creates the full directory structure with starter templates:

```bash
python <skill-path>/scripts/scaffold.py <project-root>
```

This creates all seven files with sensible defaults. The user can then customize the templates for their specific agent.

If the user already has a project and wants to add memory to it, the scaffold script is safe to run — it will not overwrite existing files.

## Step 2: Understand the retrieval workflow

The loader uses four phases with increasing cost. The goal is to stay in Phases 1–3 for 80% of sessions.

```
Phase 1: Orient       →  state.json                ~200 tokens, always
Phase 2: Anchor       →  resumption.md             ~300 tokens, always
Phase 3: Context      →  MEMORY.md + threads.md    ~1500 tokens, conditional
Phase 4: Deep Recall  →  daily logs + archive       variable, on-demand
```

**Phase 1** reads `state.json` and decides how much to load based on the time gap:
- < 2h → light (skip Phase 3, jump to conversation)
- 2–24h → standard (Phases 1–3)
- 1–7 days → full reload (add recent daily logs)
- 7+ days → deep reload (all phases, treat resumption as potentially stale)

**Phase 2** reads `resumption.md` as a first-person narrative. This is the continuity bridge — it's not parsed for data, it's absorbed as a mental starting state.

**Phase 3** branches based on the user's opening message:
- **Known thread** → load that thread + relevant MEMORY.md section (lean)
- **New/ambiguous topic** → load full MEMORY.md + all thread headers (broader)
- **Maintenance due** → load MEMORY.md + recent daily summaries for curation

**Phase 4** triggers mid-session when the user references something not in loaded context. Four strategies: targeted log lookup (by cross-reference), index search (by topic), archive recovery, or broad scan (last resort).

Read `references/RETRIEVAL.md` for the full specification including token budgets, mid-session triggers, and the loading decision flowchart.

## Step 3: Integrate into the agent loop

The two Python modules — `loader.py` and `writer.py` — handle the full lifecycle.

### Session start

```python
from loader import MemoryLoader

loader = MemoryLoader("/path/to/project-root")
context = loader.load_session_context(user_message="the user's first message")

# Inject into system prompt
system_prompt = f"""
<working_memory>
{context.text}
</working_memory>

{your_existing_system_prompt}
"""
```

The loader returns a `SessionContext` with:
- `.text` — the assembled memory block ready for prompt injection
- `.total_tokens` — approximate token cost
- `.metadata` — loading decisions for debugging (which phases ran, which branches taken)

### During session

```python
from writer import MemoryWriter

writer = MemoryWriter("/path/to/project-root")

# Capture observations as they happen
writer.note_decision("Chose X over Y", "reasoning here")
writer.note_open_question("Should we revisit Z?")
writer.note_pattern("User tends to ask for examples after abstract explanations")
writer.note_thread_touched("thread-project-alpha")
```

### Session end

```python
writer.end_session(
    session_summary="High-level summary of what happened",
    resumption_note="First-person handoff to next session self...",
    thread_updates={
        "thread-project-alpha": {
            "current_position": "Finished the API design. Moving to testing.",
            "new_open_questions": ["How to handle auth tokens?"],
            "closed_questions": ["Which framework to use?"],
        }
    },
    mood="focused, productive",
)
```

This persists to all five outputs: daily log, threads, state.json, resumption.md, and maintenance flags.

## Step 4: Customize the schemas

The templates from scaffolding are starting points. Here's what to customize per agent:

### MEMORY.md — long-term memory

The three tiers (Active / Fading / Archived) use decay logic:
- **Active**: reinforced through recall in the last ~7 sessions. Entries carry a session count and confidence level.
- **Fading**: not referenced in 7+ sessions. Will be archived if not recalled.
- **Archived**: moved to `archive.md` after 20+ sessions of neglect. Still searchable.

Customize the section headings under Active for your domain. The default has "About [User]", "About This Project", and "Working Style". Rename these to match what your agent needs to remember. Read `references/SCHEMAS.md` for the full schema with examples.

### threads.md — ongoing topics

Each thread is self-contained:
```
## Thread: [Title]
- **ID**: thread-[slug]
- **Status**: active | paused | closed
- **Started**: YYYY-MM-DD
- **Last touched**: YYYY-MM-DD
Key Decisions Made, Open Questions, Next Likely Steps, Related links
```

The critical design choice: threads carry enough state to resume without re-reading daily logs. If a thread's "Current Position" section isn't sufficient to jump back in cold, it needs more detail.

### resumption.md — the continuity bridge

This is the most unusual file. It's written in first person, addressed to the agent's next session self. It should include:
- Where we left off (not a summary — a position)
- What's likely to happen next (predictions)
- What to watch for (patterns, potential pivots)
- Tone calibration (match the user's current energy)

It is *not* a session summary. It's a handoff note. The difference matters — summaries are retrospective; resumption notes are prospective.

### state.json — machine-readable state

Keep this strictly ephemeral and machine-parseable. If a value requires interpretation, it belongs in a markdown file instead. The default schema covers:

- `last_session` (timestamp, duration, daily log path)
- `session_counter` (total, this week, since last memory review)
- `active_threads` (id, title, status, last_touched, priority)
- `pending_questions` (list of strings)
- `flags` (memory_review_due, threads_need_update, archive_candidates_exist)
- `context_hints` (mood hypothesis, conversation style, last topic position)

Read `references/SCHEMAS.md` for the full JSON schema.

## Memory curation workflow

Every ~5 sessions (or when the `memory_review_due` flag is set), the agent should curate MEMORY.md:

1. Load MEMORY.md + recent daily log summaries
2. **Promote**: patterns confirmed across multiple sessions → raise confidence, merge duplicates
3. **Demote**: entries not referenced in 7+ sessions → move to Fading
4. **Archive**: Fading entries not recalled in 20+ sessions → move to `archive.md`
5. **Merge**: consolidate entries that say the same thing differently
6. Update the Maintenance Log at the bottom of MEMORY.md

The curation is what prevents unbounded growth and keeps long-term memory useful. Without it, MEMORY.md becomes noise within weeks.

## Cross-referencing

Bidirectional links connect the system's files. Use lightweight refs:

```
[ref: memory/2026-03-20.md#decisions]
[ref: thread-wm-design]
[ref: MEMORY.md > About This Project]
```

Daily logs reference which threads they advanced. Threads reference which daily logs contain their key decisions. MEMORY.md entries reference where they were first established.

Without cross-references, retrieval degrades to full-text scanning, which is expensive and unreliable.

## Troubleshooting

**Memory loading uses too many tokens**: Check `context.metadata` from the loader — it shows which phases ran and how many tokens each consumed. Common fixes: tighten the Phase 3 branch (load thread-specific sections instead of full MEMORY.md), reduce daily log summaries to headers-only, lower the budget caps in `BudgetConfig`.

**Agent re-litigates settled decisions**: The decisions table in daily logs and the "Key Decisions Made" section in threads aren't being loaded. Ensure cross-references point to the right daily log sections, and that threads carry decision summaries.

**Resumption feels generic**: The resumption note is being written as a summary instead of a handoff. It should contain predictions, tonal guidance, and a specific "pick up from here" anchor — not a recap.

**Threads get stale**: Thread positions aren't being updated at session end. Make sure `writer.end_session()` is called with `thread_updates` that advance the "Current Position" field.

**Daily logs are too large to scan**: Enable the index file. Once you have 30+ daily logs, the loader's Phase 4 needs `index.md` to avoid broad scans. The index is rebuilt automatically when `daily_log_count % 5 == 0`.
