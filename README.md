# ODIN

**O**bservant **D**igital **I**ntelligence **N**etwork

A personal voice assistant that **talks first, at the right moment**.

Most assistants wait for you to speak. ODIN watches your calendar, inbox, and projects, and speaks up when something matters: *"Your 1:1 is in 20 minutes and it's across the building."* It also decides **when** you can be interrupted. It won't cut in while you're on a call or deep in focus, and it can always tell you **why** it spoke.

Built from scratch: no LangChain, no assistant frameworks. Every model it uses is studied and documented in [RESEARCH.md](RESEARCH.md). What every part does is in [SPEC.md](SPEC.md).

> 🚧 Work in progress. See the [roadmap](#roadmap).

---

## Prior work, and where ODIN fits

| Project | What it does well | What it doesn't do |
|---|---|---|
| [isair/jarvis](https://github.com/isair/jarvis) (2k★) | Local voice, joins room conversations, knowledge-graph memory, MCP tools, published evals | Proactivity is marked ❌ Missing in its own roadmap ([#386](https://github.com/isair/jarvis/issues/386)); meetings need a manual "Pause Listening" |
| [PanPenek/JarvisAi](https://github.com/PanPenek/JarvisAi) | Wake word, 31 tools, screen vision, memory | Waits for you to speak |
| [madcato/voicebot](https://github.com/madcato/voicebot) | Barge-in, ambient mode, proactive suggestions from screen captures | No interruption timing, no measured false-alarm rate |
| ChatGPT Pulse | Proactive daily briefing | Text cards once a day, cloud only, not real time, not voice |
| Gemini proactive assistant | Surfaces info before you ask | Cloud only, closed, no control over when it interrupts |

Local voice assistants with memory, tools, and wake words already exist. Proactive assistants from big companies already exist. **What's missing is an assistant that reasons about _when_ to interrupt you, explains why, learns from your feedback, and publishes how often it gets it wrong.** That's ODIN.

---

## What makes it different

### 1. It talks first ⭐
**Watchers** (calendar, email, GitHub, and so on) emit events. A **scorer** decides whether each event is worth saying out loud:

```
worth_saying = urgency × relevance × (1 − annoyance)
```

### 2. It picks the right moment ⭐
Deciding *whether* to speak isn't enough. ODIN also decides *when*. It checks **interruptibility signals** before speaking:
- Are you on a call? (Mic or camera in use, Zoom or Meet in front.) → wait
- Are you typing fast or in a focus app? → wait, unless it's urgent
- Did you just finish something? (Meeting ended, long pause in typing.) → good moment

Low-priority messages queue up and get delivered together at the next natural break.

### 3. It catches your promises
ODIN reads what you wrote (sent emails, notes) for commitments like *"I'll email you Sunday"* or *"I'll send it by Friday"* and reminds you before the deadline passes. You make promises and ODIN keeps track of them.

### 4. "Why did you tell me that?"
Every proactive message keeps a reason trace: which watcher fired, the score, and the interruptibility check. Ask "why?" and ODIN tells you exactly why it spoke.

### 5. It learns when to shut up
"Not now," "don't tell me about that again," and ignored messages all get logged. The threshold and timing adjust per topic.

### 6. Pushback
*"You have three events back to back with no lunch. Want me to move one?"* It warns you, then does what you decide.

### 7. Published false-alarm rate
ODIN ships with a **proactive benchmark**: simulated days of events, each labeled "should speak" or "should stay quiet." Every release reports precision and recall. As far as I can find, no open assistant publishes this.

| Metric | Target |
|---|---|
| Proactive precision (spoke and it mattered) | > 90% |
| Proactive recall (mattered and it spoke) | > 80% |
| Interruptions during calls/focus | 0 non-urgent |
| End of speech → first spoken word | < 1 s |
| Wake word false triggers | < 1 per hour |

### 8. Wake word I trained
A small model trained on my own recordings, not a downloaded "Hey Jarvis."

### 9. Memory you can see
Facts about you live in plain records you can read, edit, and delete.

### 10. Everything else a complete assistant does
ODIN also covers what the best local assistants do: it joins conversations in the room ("Odin, what do you think?"), keeps knowledge-graph memory and a daily diary, removes sensitive info before saving, uses web/screen/file/MCP tools, does dictation, has a text chat window and a task queue, and comes as a desktop app. All of it is reimplemented from scratch (see Phases 8–12).

---

## How it works

```
 watchers ─▶ events ─▶ scorer ─▶ interruptibility check ─▶ speak now / queue for next break
 (calendar,             (worth        (on a call? typing?          │
  email, github,         saying?)      just finished?)              │
  promises)                                                         ▼
mic → wake word → speech-to-text ─▶ agent (LLM + tools + memory) ─▶ text-to-speech → speaker
                                                  ▲
                                   feedback log ("not now", "why?") ──▶ scorer learns
```

| Part | Folder | Job |
|---|---|---|
| Agent loop | `odin/agent/` | Model picks a tool → run it → feed result back → repeat |
| Tools | `odin/tools/` | Plain Python functions: open apps, music, calendar, email |
| Memory | `odin/memory/` | Facts about you (SQLite, embeddings later) |
| Watchers | `odin/watchers/` | Poll a source, emit events |
| Promises | `odin/watchers/promises.py` | Find commitments in what you wrote |
| Scorer | `odin/proactive/scorer.py` | Is this worth saying? |
| Interruptibility | `odin/proactive/moment.py` | Is now a good time? |
| Reason traces | `odin/proactive/trace.py` | Why it spoke |
| Feedback | `odin/proactive/feedback.py` | Learn from "not now" |
| Audio | `odin/audio/` | Wake word, speech-to-text, text-to-speech |
| Benchmarks | `bench/` | Proactive precision/recall, latency, wake word false triggers |

---

## Roadmap

Each phase starts with research ([RESEARCH.md](RESEARCH.md)) and ends with notes on what I learned.

### Phase 0: research
- [ ] How LLMs generate text (tokens, context, temperature, quantization)
- [ ] How tool calling works in raw JSON
- [ ] Interruptibility research (see RESEARCH.md §7)

### Phase 1: the brain (text only)
- [ ] Agent loop that calls Ollama and parses tool calls
- [ ] Tools: current time, open an app, play/pause music
- [ ] Command-line chat

### Phase 2: memory
- [ ] Save, recall, and forget facts
- [ ] "What do you know about me?"

### Phase 3: talks first ⭐
- [ ] Event format plus a calendar watcher
- [ ] Scorer with a threshold
- [ ] Reason traces and "why did you tell me that?"
- [ ] Email watcher
- [ ] Promise catcher

### Phase 4: the right moment ⭐
- [ ] Interruptibility signals: call detection, typing rate, front app
- [ ] Queue low-priority messages for the next break
- [ ] Feedback log; threshold learns per topic
- [ ] Pushback rules

### Phase 5: proactive benchmark ⭐
- [ ] Simulated-day generator with labeled events
- [ ] Precision/recall script
- [ ] Publish results in this README

### Phase 6: voice
- [ ] Push-to-talk speech-to-text
- [ ] Text-to-speech, streamed sentence by sentence
- [ ] Speak proactive messages out loud
- [ ] Echo cancellation (so it doesn't hear itself)

### Phase 7: wake word
- [ ] Record samples, train a small model
- [ ] Say "Odin" anywhere in a sentence, not only at the start
- [ ] Measure false triggers per hour

**🎬 Demo milestone:** at this point ODIN talks first, out loud, at the right moment. Record the demo video here.

### Phase 8: in the room
- [ ] Short rolling transcript of nearby speech, temporary and never saved
- [ ] "Odin, what do you think?" uses the recent conversation as context
- [ ] Auto-pause listening when a call starts (reuses Phase 4 call detection)

### Phase 9: deep memory
- [ ] Knowledge graph: people, places, plans, and how they connect
- [ ] Daily diary summarizing conversations
- [ ] Hybrid search over memory: keyword + vector (from kestrel)
- [ ] Remove sensitive info (passwords, card numbers) before saving
- [ ] Memory viewer

### Phase 10: more tools
- [ ] Web search and fetch
- [ ] Weather, location
- [ ] Read the screen (screenshot → text)
- [ ] File access
- [ ] MCP client, so any MCP server plugs in (smart home, GitHub, Slack)

### Phase 11: everyday use
- [ ] Hold-a-key dictation into any app
- [ ] Text chat window that shares the voice conversation and memory
- [ ] Task queue: hand ODIN a long job and check back later
- [ ] Low power mode

### Phase 12: the app
- [ ] Desktop face/orb that reacts when ODIN listens, thinks, or wants to talk
- [ ] Setup wizard (pick models, mic)
- [ ] Settings window
- [ ] Packaged Mac app

### Phase 13: prove it
- [ ] Reply-quality evals (does it answer well, call the right tool)
- [ ] Proactive benchmark results (Phase 5) published side by side
- [ ] Latency numbers for every stage

---

## Rules for this project
1. No agent or assistant frameworks. If it's core, write it.
2. No line I can't explain. If I don't understand it, it doesn't get merged.
3. Every feature gets a number.
4. Silence is the default. Speaking has to earn it.
5. Learn from other projects, never copy their code. Ideas are free; code has licenses.
