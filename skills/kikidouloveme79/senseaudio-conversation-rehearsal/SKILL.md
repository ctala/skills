---
name: senseaudio-conversation-rehearsal
description: Use when a user wants to rehearse a high-pressure conversation such as a performance review, reporting meeting, promotion defense, difficult manager conversation, or stakeholder alignment session, using SenseAudio ASR for spoken rehearsal intake, SenseAudio TTS or an authorized cloned voice for the counterpart, and transcript-based debriefing on tone, structure, and communication risk.
---

# SenseAudio Conversation Rehearsal

## What this skill is for

This skill is for realistic conversation rehearsal in high-pressure situations:

- 汇报述职
- 向上沟通
- 绩效面谈
- 晋升答辩
- 难搞老板或强势同事沟通
- 需要脱敏的正式谈话

It is designed to simulate the **other person speaking back**, not just generate a script.

## Default stance

Use two voice modes:

- `proxy_voice`
  - Recommended default
  - Use a role-appropriate system voice and behavior style
- `authorized_clone`
  - Only use when the voice sample is explicitly authorized for rehearsal or internal training
  - Best official path: clone on the SenseAudio platform first, then pass the prepared clone `voice_id`
  - A prepared cloned voice id commonly looks like `vc-...`, and can be passed directly with `--prepared-clone-voice-id`

Do not default to cloning a real person's voice without clear permission.

## Workflow

1. Define the rehearsal:
   - scenario
   - counterpart role
   - relationship
   - talk topic
   - desired outcome
   - fear triggers
   - difficulty
2. Run `scripts/build_rehearsal_blueprint.py`.
3. Decide voice mode:
   - proxy voice
   - authorized clone
4. Run the live loop in your agent stack:
   - counterpart turn via TTS
   - user spoken reply via ASR
   - if you want faster perceived intake, enable stream ASR
   - agent judges tone, structure, and progress
   - use `scripts/build_counterpart_turn.py` to generate the next counterpart reply
   - use `scripts/senseaudio_counterpart_tts.py` to synthesize that reply
   - official clone chain: prepare the clone on the SenseAudio platform first and pass the resulting `voice_id`
   - if that `voice_id` is a clone id like `vc-...`, counterpart TTS now auto-routes to `SenseAudio-TTS-1.5`
   - optional experimental path: if an authorized platform token is available, use `scripts/senseaudio_clone_workspace.py` to inspect clone slots or attempt a rehearsal-only clone from an authorized sample
   - if the user wants to actually hear the counterpart turns in Feishu or PicoClaw, use `--send-feishu-audio` or run `scripts/send_rehearsal_counterparts_to_feishu.py`
5. After the session, run `scripts/analyze_rehearsal_transcript.py`.
6. Produce a debrief:
   - weak openings
   - over-explaining
   - vague asks
   - missing evidence
   - apologetic or defensive tone
   - better rewrites

## OpenClaw Or PicoClaw Trigger Pattern

Use this skill as a structured multi-turn rehearsal mode.

Recommended user trigger:

```text
开始演练，用 $senseaudio-conversation-rehearsal。
场景：manager_update
对方身份：strict_manager
主题：项目延期说明
目标：获得补救方案认可
害怕点：被打断，被质疑执行力
难度：medium
prepared clone voice_id：your_clone_voice_id
后面我发语音，和我进行多轮演练，最后给我复盘。
```

The agent should:

1. Collect the rehearsal slots first.
2. Build the blueprint.
3. Enter rehearsal mode.
4. For every user audio turn:
   - transcribe with `scripts/senseaudio_asr.py`
   - generate the next counterpart turn
   - synthesize that turn with proxy voice or the prepared clone `voice_id`
   - if the user says "直接发语音给我练" or "每轮都发语音", use `--send-feishu-audio` so the counterpart turns are sent as Feishu `audio` messages
5. End with `scripts/analyze_rehearsal_transcript.py` and return a concrete debrief.

If the user asks to "use the cloned voice", interpret that as:

- use a platform-prepared clone `voice_id` when available
- otherwise pause and ask for the clone `voice_id` or fall back to `proxy_voice`

## Design rules

- Prioritize behavior realism over exact voice likeness.
- Treat the public documented clone flow and the experimental workspace automation flow as separate paths.
- For scary-counterpart scenarios, structure the rehearsal in phases:
  - opening pressure
  - pushback
  - challenge question
  - close
- Evaluate both:
  - what the user said
  - how the user said it
- Keep debrief concrete and operational.

## Resources

- `scripts/build_rehearsal_blueprint.py`
  - Builds a structured rehearsal plan and counterpart persona
- `scripts/build_counterpart_turn.py`
  - Generates the next counterpart turn from rehearsal state and the user's latest reply
- `scripts/senseaudio_asr.py`
  - Transcribes user spoken rehearsal turns with the official SenseAudio HTTP ASR API
- `scripts/senseaudio_counterpart_tts.py`
  - Synthesizes a counterpart turn using a safe proxy voice or an explicitly authorized clone voice_id
- `scripts/run_live_rehearsal_session.py`
  - Runs a multi-turn live rehearsal session from user audio replies, counterpart generation, TTS, and automatic debrief
  - Supports `--stream-asr` and `--send-feishu-audio`
- `scripts/send_rehearsal_counterparts_to_feishu.py`
  - Reuses the Feishu voice delivery path to send the generated counterpart turns one by one as audio messages
- `scripts/senseaudio_clone_workspace.py`
  - Lists clone slots, lists available voices, and creates an authorized rehearsal clone through the official SenseAudio workspace endpoints, preferring a platform token and otherwise trying a logged-in Chrome browser session
- `scripts/senseaudio_platform_token.py`
  - Resolves a SenseAudio workspace platform token from env or a logged-in Chrome SenseAudio tab when Apple Events JavaScript is enabled
- `scripts/run_complete_rehearsal_service.py`
  - One entry point that builds the blueprint, optionally resolves a prepared clone `voice_id` or attempts experimental workspace clone automation, runs the live rehearsal session, and writes a summary bundle
  - Supports `--send-feishu-audio` so the rehearsal counterpart can proactively send voice turns to Feishu or PicoClaw-linked chats
- `scripts/analyze_rehearsal_transcript.py`
  - Scores a rehearsal transcript for tone and communication risks
- `references/live_rehearsal_loop.md`
  - A minimal multi-turn runtime pattern for OpenClaw or another agent orchestrator
- `references/rehearsal_design.md`
  - Product design, safety policy, and rollout plan
