# ODIN spec: what every part is supposed to do

This file describes **what** each part does, how it behaves, and how to tell when it's done. It doesn't say **how** to code it. That's my job.

Each part has:
- **Purpose:** why it exists
- **What it does:** behavior in plain words
- **Input → output:** what goes in, what comes out
- **Example:** what it looks like in real life
- **Done when:** the test that says it's finished

---

# Part 1: the core (what nobody else has)

## Phase 0: research
**Purpose:** understand every model and idea before using it.

**What it does:** for each component, fill in its section of [RESEARCH.md](RESEARCH.md): what it is, how it works inside, the options, what I picked and why, and what I measured.

**Done when:** I can explain to a friend, without notes, how an LLM picks its next word, how a tool call works, and why thinking mode made lantern slow.

---

## Phase 1: the brain (text only)

### 1.1 Model client: `odin/agent/model.py`
**Purpose:** the one place that talks to the LLM.

**What it does:** sends the conversation so far to Ollama and returns the model's reply. The reply is either plain text or a request to call a tool.

**Input → output:** list of messages + list of available tools → reply text **or** tool call (name + arguments)

**Example:** send `[{"role": "user", "content": "hi"}]` → get `"Hey! What's up?"`

**Done when:** a reply comes back in under 2 seconds for a short message, with thinking turned off.

### 1.2 Tool registry: `odin/tools/`
**Purpose:** a list of things ODIN is allowed to do.

**What it does:** each tool is a normal Python function plus a short description (name, what it does, what arguments it takes). The registry turns those descriptions into the format the model needs, and runs a tool by name when asked.

**Input → output:** tool name + arguments → result as text

**Example:** `run("get_time", {})` → `"It's 3:42 PM on Wednesday, Oct 28."`

**First tools:**
| Tool | Does |
|---|---|
| `get_time` | Current date and time |
| `open_app` | Opens a Mac app by name |
| `music` | Play, pause, or skip in Spotify/Music |

**Done when:** I can add a new tool by writing one function, with no other code changes.

### 1.3 Agent loop: `odin/agent/loop.py`
**Purpose:** ODIN's thinking cycle. Everything else plugs into it.

**What it does:**
1. Take the user's message.
2. Ask the model what to do.
3. If it asks for a tool → run it → give the result back to the model → go to step 2.
4. If it answers in text → that's the final reply.
5. Stop after a max number of steps (for example 5) so it can never loop forever.
6. If a tool errors, give the error to the model so it can try again (lantern's path-fix moment).

**Input → output:** user message → final reply

**Example:** "what time is it?" → model calls `get_time` → gets "3:42 PM" → replies "It's 3:42."

**Done when:** it handles a 2-tool request, like "open Spotify and tell me the time."

### 1.4 CLI chat: `odin/cli.py`
**Purpose:** a way to test everything by typing before voice exists.

**What it does:** a loop: type → ODIN replies → repeat. `/quit` exits.

**Done when:** I can hold a 10-message conversation and it remembers earlier messages in that session.

---

## Phase 2: memory (basic)

### 2.1 Fact store: `odin/memory/store.py`
**Purpose:** ODIN knows me across days, not just one chat.

**What it does:** saves facts as records: the fact, when it was learned, where it came from (I said it, or it was read from an email), and a topic.

**Example record:**
```
fact: "Has class at 2pm on Mondays and Wednesdays"
learned: 2026-10-28
source: user said it
topic: schedule
```

### 2.2 Memory tools
| Tool | Does |
|---|---|
| `remember(fact)` | Save a fact. Triggered by "remember that…" or when ODIN notices something important |
| `recall(query)` | Find facts related to the current message |
| `forget(fact)` | Delete a fact |
| `what_do_you_know()` | List everything, grouped by topic |

### 2.3 Auto-recall
**What it does:** before each reply, ODIN looks up the few facts most related to the message and slips them into the model's context.

**Example:** "should I go to the gym at 2 Monday?" → recalls "class at 2pm Mondays" → "You have class then. How about 4?"

**Done when:** it remembers a fact after restarting ODIN, and "forget that" actually deletes it.

---

## Phase 3: talks first ⭐

### 3.1 Event format: `odin/watchers/event.py`
**Purpose:** one shared shape for "something happened," whatever the source.

**Every event has:** source (calendar, email…), what happened, when, related people, deadline (if any), and a unique ID (so the same thing is never announced twice).

### 3.2 Calendar watcher: `odin/watchers/calendar.py`
**What it does:** every few minutes, reads my Google Calendar and emits events:
- A meeting starts soon ("starts in 20 min", "starts in 5 min")
- A meeting changed or was cancelled
- Back-to-back meetings with no break (for pushback)

### 3.3 Email watcher: `odin/watchers/email.py`
**What it does:** checks Gmail for new mail and emits an event when something likely matters: a reply from a recruiter, someone I emailed recently, words like "interview," "offer," "deadline," "confirm."

**Never:** reads every email out loud. Newsletters and promos are ignored.

### 3.4 GitHub watcher: `odin/watchers/github.py`
**What it does:** notices PR reviews, issue replies, failing CI, and "haven't pushed to X in N days."

### 3.5 Scorer: `odin/proactive/scorer.py`
**Purpose:** answer "is this worth saying out loud?"

**What it does:** gives every event a score from 0 to 1:
```
worth_saying = urgency × relevance × (1 − annoyance)
```
- **urgency:** how soon it matters (meeting in 5 min = high, newsletter = 0)
- **relevance:** how much it relates to me and my memory (a recruiter I'm talking to = high)
- **annoyance:** how much I've pushed back on this kind of message before

Above the threshold (for example 0.6) → pass to the moment checker. Below → drop it, or save it for a summary.

**Done when:** given 20 hand-made events, it picks the same ones I would.

### 3.6 Reason traces: `odin/proactive/trace.py`
**Purpose:** ODIN can always explain itself.

**What it does:** every time ODIN speaks first, it saves: the event, the three scores, the threshold, and the moment check result.

**Example:** "Why did you tell me that?" → "Wells Fargo replied, and you have a meeting with them Wednesday. Urgency 0.8, relevance 0.9. You weren't on a call."

### 3.7 Promise catcher: `odin/watchers/promises.py`
**Purpose:** catch things I said I'd do.

**What it does:** reads my **sent** emails (and later, messages I dictate) and pulls out commitments: **who**, **what**, **by when**. It turns "Sunday" or "end of week" into a real date and creates a reminder event before the deadline.

**Example:** I emailed "I'll email you on Sunday to set up a time" → Sunday 10 AM: "You told Travis you'd email him today."

**Done when:** on 50 of my real sent emails that I've labeled, it finds at least 80% of promises with few false ones.

---

## Phase 4: the right moment ⭐

### 4.1 Moment checker: `odin/proactive/moment.py`
**Purpose:** answer "is **now** a good time?"

**Signals it checks:**
| Signal | Meaning |
|---|---|
| Mic or camera in use / Zoom, Meet, FaceTime in front | On a call → **wait** |
| Typing fast for the last minute | Focused → wait unless urgent |
| Fullscreen app / Focus mode on | Do not disturb → wait unless urgent |
| Just stopped typing, meeting just ended, app switched | Natural break → **good time** |
| Quiet hours (for example 11 PM–8 AM) | Wait unless urgent |

**Output:** `speak_now`, `wait`, or `wait_unless_urgent`

### 4.2 Message queue
**What it does:** messages that passed the scorer but hit a bad moment wait in a queue. At the next good moment, ODIN delivers them together: "Two things: Wells Fargo replied, and your 4 PM moved to 4:30." Messages expire if they no longer matter (don't say "meeting in 5 min" after the meeting started).

### 4.3 Feedback learning: `odin/proactive/feedback.py`
**What it does:** logs how I react to every proactive message:
| My reaction | Effect |
|---|---|
| "Thanks" / I act on it | That topic's threshold goes **down** a little |
| "Not now" | Re-queue it; the moment checker learns |
| "Don't tell me about that" | That topic's threshold goes **way up** |
| I ignore it | Small step up |

**Done when:** after a week of use, it speaks noticeably less about things I don't care about.

### 4.4 Pushback
**What it does:** when a plan looks bad, ODIN says so once, then does what I decide.

**Examples:**
- Three back-to-back events with no food → "No lunch break today. Want me to move one?"
- "Schedule it at 11 PM" when I'm flying at 6 AM → "You fly at 6. Still want 11 PM?"

**Rule:** warn once, never nag, never refuse.

---

## Phase 5: proactive benchmark ⭐

### 5.1 Simulated days: `bench/days/`
**What it does:** fake but realistic days: a list of events with times plus what I'm doing at each moment (on a call, typing, idle). Each event is labeled **should speak now**, **should speak later**, or **should stay quiet**.

### 5.2 Benchmark script: `bench/proactive.py`
**What it does:** runs the scorer and moment checker over every simulated day and reports:
- **Precision:** of the times it spoke, how often it should have
- **Recall:** of the times it should have spoken, how often it did
- **Bad interruptions:** spoke during a call or focus when it wasn't urgent
- **Timing:** for "speak later" events, did it wait for a break?

**Done when:** there are at least 30 labeled days and the README shows the numbers. Targets: precision > 90%, recall > 80%, 0 non-urgent interruptions during calls.

---

## Phase 6: voice

### 6.1 Speech-to-text: `odin/audio/stt.py`
**What it does:** records while I hold a key (push-to-talk first), detects when I stop talking, and turns it into text with Whisper.

**Done when:** I'm understood correctly on 20 test sentences, in under 1 second after I stop.

### 6.2 Text-to-speech: `odin/audio/tts.py`
**What it does:** speaks ODIN's replies with Piper or Kokoro. It speaks **sentence by sentence** while the model is still writing, so it starts talking almost immediately.

### 6.3 Echo cancellation
**What it does:** stops ODIN from hearing its own voice through the mic and replying to itself.

### 6.4 Proactive voice
**What it does:** proactive messages are spoken out loud, starting with a soft chime so it doesn't feel like a jump scare.

**Done when:** end of my speech → ODIN's first spoken word takes under 1 second.

---

## Phase 7: wake word

### 7.1 Data: `recordings/` (not committed)
**What it does:** recordings of me saying "Odin" (100+ times, different rooms and tones), other words that sound close ("ocean," "going," "open"), other voices, and background noise.

### 7.2 Model: `odin/audio/wake.py`
**What it does:** a tiny model I train that listens nonstop using almost no CPU and fires only when it hears "Odin." It works anywhere in a sentence, not only at the start: "what time is it, Odin?"

**Done when:** it catches "Odin" at least 95% of the time and false-triggers under once per hour of normal room noise.

**🎬 Demo milestone:** ODIN talks first, out loud, at the right moment, with a wake word I trained. Record the video.

---

# Part 2: the complete assistant

## Phase 8: in the room

### 8.1 Rolling transcript
**What it does:** keeps a short, **temporary** transcript of the last few minutes of speech nearby. It's never saved to disk, and it's deleted as it ages out.

### 8.2 "Odin, what do you think?"
**What it does:** when I call ODIN mid-conversation, it uses the rolling transcript to understand what we were talking about.

**Example:**
> Me: We could have a picnic tomorrow.
> Friend: Depends on the weather.
> Me: Odin, what do you think?
> ODIN: Tomorrow's 72° and sunny until 4, so go early.

### 8.3 Auto-pause on calls
**What it does:** stops listening to the room automatically when a call starts (reuses 4.1's call detection). isair/jarvis needs a manual button for this.

**Done when:** it answers correctly in 8 of 10 test conversations, and never keeps transcript audio on disk.

---

## Phase 9: deep memory

### 9.1 Knowledge graph
**What it does:** upgrades Phase 2 facts into **things and links**: people, places, companies, plans, and how they connect.

**Example:** Travis → works at → LinkedIn; Travis → I promised → email Sunday; Wells Fargo → meeting → Nov 4 10:30.

### 9.2 Diary
**What it does:** at the end of each day, writes a short summary of what we talked about and what happened. "What did I do last Tuesday?" works.

### 9.3 Hybrid search
**What it does:** finds memories using both keyword matching and meaning (embeddings), combined. That's the same idea as my kestrel project.

### 9.4 Redaction
**What it does:** before anything is saved or sent to a model, strips passwords, card numbers, SSNs, and API keys.

### 9.5 Memory viewer
**What it does:** a page that shows everything ODIN knows, grouped by topic, with edit and delete buttons.

**Done when:** it answers 20 memory questions correctly, and none of my test secrets show up in storage.

---

## Phase 10: more tools
| Tool | Does |
|---|---|
| `web_search` / `fetch` | Searches the web and reads pages |
| `weather` | Forecast for where I am |
| `location` | Rough location (optional, off by default) |
| `read_screen` | Screenshot → text, so "what's this error?" works |
| `files` | Read and find files (writing asks first) |
| MCP client | Any MCP server plugs in: smart home, Slack, GitHub, and more |

**Done when:** each tool has at least 2 tests where the agent picks it correctly.

---

## Phase 11: everyday use
| Feature | Does |
|---|---|
| Dictation | Hold a key, speak, release → text gets typed into whatever app I'm in |
| Text chat window | Same conversation and memory as voice, but silent |
| Task queue | "Research Datadog's internship" → ODIN works in the background, tells me when it's done (proactively, at a good moment) |
| Low power mode | Smaller models and less listening when on battery |

---

## Phase 12: the app
| Feature | Does |
|---|---|
| Face/orb | A small on-screen shape that changes when ODIN is listening, thinking, speaking, or **has something to tell me** (glows instead of interrupting when the moment is bad) |
| Setup wizard | First launch: pick mic, download models, connect Google |
| Settings | Models, voices, quiet hours, thresholds, watchers on or off |
| Mac app | Double-click to run, lives in the menu bar |

---

## Phase 13: prove it
| Benchmark | Measures |
|---|---|
| Reply evals | Answers well, picks the right tool, doesn't make things up |
| Proactive benchmark | Precision, recall, bad interruptions (from Phase 5) |
| Latency | Every stage: wake → STT → model → first spoken word |
| Wake word | Catch rate, false triggers per hour |
| Memory | Recall accuracy, redaction leaks (should be 0) |

**Done when:** all numbers are in the README, updated every release.

---

## The one-sentence version
Other assistants wait to be asked. **ODIN notices what matters, waits for the right moment, tells you, explains why, and learns when to stay quiet.** Then it does everything else a great assistant does.
