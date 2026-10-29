# ODIN research

Everything ODIN depends on, what it is, how it works, and why I chose it. Each section gets filled in **before** that part is built.

For each component, answer:
1. **What is it?** One paragraph in my own words.
2. **How does it work inside?** The architecture, at a level I could whiteboard.
3. **What are the options?** At least 2–3, compared.
4. **What did I pick and why?** Size, speed, quality, runs offline or not.
5. **What did I measure?** Real numbers from my Mac.
6. **Sources.** Papers, docs, videos.

---

## 1. The brain: large language model
**Job:** understand what I said, decide which tool to call, write the reply.

**Candidates:** Qwen3 (4B/8B), Llama 3.x, Gemma, Phi, or a cloud model for speed.

**Questions to answer:**
- What is a token? What is a context window, and why is Qwen3 4B's 8k a limit?
- What is a transformer, in simple terms? What does "4B parameters" mean?
- What is quantization (Q4, Q8), and why does it let a model fit on a laptop?
- What does Ollama actually do? (Hint: it wraps llama.cpp.)
- What is "thinking mode," and why did it make lantern take 7 minutes?

**Key reading:** "Attention Is All You Need" (2017); Andrej Karpathy, "Let's build GPT" (YouTube); the Ollama and llama.cpp READMEs.

## 2. Tool calling
**Job:** let the model ask to run a function instead of answering in text.

**Questions:**
- What does a tool call look like in the raw JSON going to and from Ollama?
- How does the model "know" a tool exists? (It's just text in the prompt.)
- What happens when the model calls a tool wrong, and how do I recover?

## 3. Memory: embeddings and search
**Job:** remember facts about me and pull up the relevant ones each turn.

**Candidates:** plain SQLite keyword search first; then an embedding model like nomic-embed-text or all-MiniLM.

**Questions:**
- What is an embedding? Why are similar sentences "close" to each other?
- What is cosine similarity?
- When is keyword search good enough? (My kestrel project compares BM25, dense, and hybrid search, so reuse what I learned there.)

## 4. Ears: speech-to-text
**Job:** turn my voice into text.

**Candidates:** Whisper (tiny/base/small) via whisper.cpp or faster-whisper; Apple's on-device speech.

**Questions:**
- How does Whisper turn audio into text? (Spectrograms + an encoder-decoder transformer.)
- Tradeoff between model size, speed, and accuracy on my Mac.
- How do I detect when I stopped talking? (Voice activity detection.)

**Key reading:** the Whisper paper, "Robust Speech Recognition via Large-Scale Weak Supervision" (OpenAI, 2022).

## 5. Mouth: text-to-speech
**Job:** speak the reply out loud.

**Candidates:** Piper, Kokoro, macOS `say`.

**Questions:**
- How does neural TTS work? (Text → phonemes → audio.)
- How do I start speaking before the full reply is written? (Streaming by sentence.)

## 6. Wake word: the model I train myself
**Job:** hear "Hey Odin" and wake everything else up, while using almost no CPU.

**Questions:**
- What are MFCCs or mel spectrograms, and why do audio models use them?
- How do I build a dataset? (My recordings, other voices, background noise.)
- How do I measure false triggers per hour vs. missed wake-ups?
- What small model architecture works on-device? (Small CNN or GRU.)

**Key reading:** the openWakeWord and Picovoice Porcupine docs (to learn the approach; I train my own).

## 7. Proactive scorer and interruptibility: ODIN's core
**Job:** decide whether an event is worth saying, and whether now is a good time.

**Questions:**
- Start with rules: what makes something urgent?
- What signals predict that someone can be interrupted? (Typing, calls, app switches, time of day.)
- What is the cost of interrupting vs. the cost of waiting?
- How do I log my "not now" feedback and learn a threshold from it?
- How do I build a labeled benchmark of "should speak / should stay quiet"? What are precision and recall?

**Key reading:**
- Eric Horvitz's Microsoft Research work on attention and interruption (e.g. Horvitz & Apacible, "Learning and Reasoning about Interruption," 2003)
- Fogarty et al., "Predicting Human Interruptibility with Sensors" (2005)
- How ChatGPT Pulse and Gemini's proactive assistant work, and what they don't do

## 8. Promise catcher
**Job:** find commitments in what I wrote ("I'll email you Sunday") and remind me.

**Questions:**
- Can a small local LLM reliably extract "who, what, by when" from an email?
- How do I turn "Sunday" or "end of week" into a real date?
- How do I measure accuracy? (Label 50 of my own sent emails.)

---

## Learning log
Short dated notes as I go: what I learned, what confused me, what I measured.

| Date | Topic | Notes |
|---|---|---|
| | | |
