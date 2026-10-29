# ODIN plan (short context for coding agents)

ODIN = Observant Digital Intelligence Network. A personal voice assistant that talks first: it watches calendar/email/GitHub and speaks up on its own when something matters.

Rules:
- Pure Python. No LangChain or agent/assistant frameworks.
- The owner writes the code and must understand every line. Explain, review, and suggest. Do not write whole features unless asked.
- Every feature gets a measured number (latency, accuracy, false alarms).
- Silence is the default. Proactive messages must be rare and worth it.

Layout:
- odin/agent/      LLM loop: call model → run tool → feed result back → repeat
- odin/tools/      plain Python functions the model can call
- odin/memory/     facts about the user (SQLite, embeddings later)
- odin/watchers/   poll calendar/email/github, emit events
- odin/proactive/  score events: urgency × relevance × (1 − annoyance)
- odin/audio/      wake word, speech-to-text, text-to-speech
- bench/           latency and false-alarm benchmarks

Models: LLM = qwen3 via Ollama (localhost:11434, use /no_think). STT = Whisper. TTS = Piper or Kokoro. Wake word = small model trained by the owner.

Phases: 0 research → 1 text brain → 2 memory → 3 talks first + pushback → 4 voice → 5 wake word → 6 benchmarks.
Current phase: 0/1.
