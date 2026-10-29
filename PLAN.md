# ODIN plan (short context for coding agents)

ODIN = Observant Digital Intelligence Network. A personal voice assistant that talks first at the right moment: watchers (calendar, email, GitHub, promises the user made) emit events; a scorer decides if an event is worth saying; an interruptibility check decides if now is a good time (on a call? typing? just finished something?); every message keeps a reason trace; feedback ("not now") tunes the threshold.

What sets it apart from other Jarvis projects: they wait to be asked. ODIN decides whether AND when to interrupt, explains why, catches the user's promises, and publishes its proactive precision/recall.

Rules:
- Pure Python. No LangChain or agent/assistant frameworks.
- The owner writes the code and must understand every line. Explain, review, and suggest. Do not write whole features unless asked.
- Every feature gets a measured number.
- Silence is the default.

Layout:
- odin/agent/          LLM loop: call model → run tool → feed result back → repeat
- odin/tools/          plain Python functions the model can call
- odin/memory/         facts about the user
- odin/watchers/       calendar, email, github, promises.py
- odin/proactive/      scorer.py, moment.py (interruptibility), trace.py (why), feedback.py
- odin/audio/          wake word, speech-to-text, text-to-speech
- bench/               proactive precision/recall, latency, wake word false triggers

Models: LLM = qwen3 via Ollama (localhost:11434, use /no_think). STT = Whisper. TTS = Piper or Kokoro. Wake word = small model trained by the owner.

Phases: 0 research → 1 text brain → 2 memory → 3 talks first → 4 right moment → 5 proactive benchmark → 6 voice → 7 wake word (DEMO) → 8 in the room (rolling transcript, "Odin, what do you think?") → 9 deep memory (knowledge graph, diary, redaction) → 10 more tools (web, screen, files, MCP) → 11 everyday use (dictation, chat window, task queue) → 12 desktop app → 13 evals.
Do not copy code from other projects (e.g. isair/jarvis is non-commercial licensed). Reimplement ideas only.
Full behavior of every part: SPEC.md (read only the section for the current task; it is long).
Current phase: 0/1.
