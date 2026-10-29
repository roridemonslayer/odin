# ODIN

**O**bservant **D**igital **I**ntelligence **N**etwork

A personal voice assistant that **talks first**.

Most assistants wait for you to speak. ODIN watches your calendar, inbox, and projects, and speaks up when something matters: *"Your 1:1 is in 20 minutes and it's across the building."*

Built from scratch: no LangChain, no assistant frameworks. The agent loop, tool system, memory, audio pipeline, and wake word model are all written here, and every model it uses is studied and documented in [RESEARCH.md](RESEARCH.md).

> 🚧 Work in progress. See the [roadmap](#roadmap).

---

## What makes it different

| | Typical voice assistant | ODIN |
|---|---|---|
| **Who starts** | Waits for you | **Speaks up on its own** when something matters |
| **Pushback** | Does whatever you say | Tells you when a plan is a bad idea, then helps anyway |
| **Memory** | Forgets you, or hides what it stores | Remembers you in a file you can read and edit |
| **Speed** | "Feels fast" | Latency measured and published every release |
| **Wake word** | Someone else's model | Trained here, on my own voice |
| **Understanding** | Black box | Every model and component explained in RESEARCH.md |

### 1. Proactive: it talks first
The core feature. A background loop checks your **watchers** (calendar, email, GitHub, and so on) on a schedule. When something changes, ODIN decides whether it's worth interrupting you. If it is, it says so out loud.

The hard part isn't speaking. It's knowing **when to stay quiet**. Every proactive message gets a score:

```
urgency × relevance × (1 − annoyance)
```

ODIN only speaks when the score passes a threshold. You can tell it "not now" or "don't tell me about that again," and the threshold learns from that.

Examples:
- "Your Axon meeting starts in 20 minutes."
- "Wells Fargo replied to your email."
- "You said you'd email Travis on Sunday. It's Sunday."
- "You haven't pushed to kite in 3 days."

### 2. Pushback
ODIN has opinions. *"You have three events back to back with no lunch. Want me to move one?"* It warns, then does what you decide.

### 3. Memory you can see
Facts about you live in `memory/` as plain records (what, when learned, source). You can say "what do you know about me?" or open the file and delete anything.

### 4. Measured speed

| Metric | Target |
|---|---|
| Wake word → listening | < 200 ms |
| End of speech → first spoken word | < 1 s |
| Proactive false-alarm rate | < 1 in 10 |

### 5. Wake word I trained
A small model trained on my own recordings plus noise, not a downloaded one.

---

## How it works

```
                 ┌──────────── watchers (calendar, email, github…) ─┐
                 │                                                   ▼
mic → wake word → speech-to-text → ┌──────── agent ────────┐ ← proactive scorer
                                   │  LLM + tools + memory │
                                   └───────────┬───────────┘
                                               ▼
                                  text-to-speech → speaker
```

| Part | Folder | Notes |
|---|---|---|
| Agent loop | `odin/agent/` | Model picks a tool → run it → feed result back → repeat |
| Tools | `odin/tools/` | Plain Python functions: open apps, music, calendar, email |
| Memory | `odin/memory/` | SQLite first, embeddings later |
| Watchers | `odin/watchers/` | Each one polls a source and emits events |
| Proactive scorer | `odin/proactive/` | Decides whether an event is worth speaking about |
| Audio | `odin/audio/` | Wake word, speech-to-text, text-to-speech, streaming |
| Benchmarks | `bench/` | Latency and false-alarm measurements |

---

## Roadmap

Each phase starts with research (see [RESEARCH.md](RESEARCH.md)) and ends with notes on what I learned.

### Phase 0: research
- [ ] How LLMs generate text (tokens, context window, temperature)
- [ ] How tool calling works at the API level
- [ ] Pick and document the model for each part

### Phase 1: the brain (text only)
- [ ] Agent loop that calls a model and parses tool calls
- [ ] First tools: current time, open an app, play/pause music
- [ ] Command-line chat to test it

### Phase 2: memory
- [ ] Save facts ("remember I have class at 2")
- [ ] Recall relevant facts on each turn
- [ ] "What do you know about me?" and "Forget that."

### Phase 3: talks first ⭐
- [ ] Watcher interface plus a calendar watcher
- [ ] Email watcher
- [ ] Proactive scorer with a threshold
- [ ] "Not now" and "don't tell me about that" feedback adjusts the threshold
- [ ] Pushback rules
- [ ] Quiet hours

### Phase 4: voice
- [ ] Push-to-talk speech-to-text
- [ ] Text-to-speech replies
- [ ] Stream the reply into speech so it starts talking right away

### Phase 5: wake word
- [ ] Record my own samples
- [ ] Train a small wake word model
- [ ] Measure false triggers per hour

### Phase 6: measure and polish
- [ ] Latency benchmark script
- [ ] Publish numbers in this README
- [ ] Demo video

---

## Rules for this project
1. No agent or assistant frameworks. If it's core, write it.
2. No line I can't explain. If I don't understand it, it doesn't get merged.
3. Every feature gets a number (latency, accuracy, or false alarms).
4. Proactive messages must be rare and worth it. Silence is the default.
