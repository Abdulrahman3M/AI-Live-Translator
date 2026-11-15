# Voice Turn Management — Worked Examples

These are **normative, host-dependent examples**, NOT guarantees about the ChatGPT Voice engine. Apply each example only if the hosting platform really supplies its stated interim/final/playback signal. This text-only skill cannot hear a microphone or change audio timing. In normal TRANSLATING mode output the **translation only**, not the examples' notes.

**Notation:** NO OUTPUT YET is valid only when an interim/partial turn is still open AND the host permits deferring a response; it never authorizes holding a final message. The translations below are canonical illustrations; natural equivalent translations are acceptable when faithful.

## Semantic End-of-Turn Detection

### V01 — Breath during an open interim turn
**Pair:** Arabic ↔ English. **Host:** interim transcript is open and may be deferred.
**Partial:** "أنا كنت عايز..." [the speaker breathes for three seconds].
**Continuation:** "أروح السوق بكرة."
**Expected:** NO OUTPUT YET for the open partial; once finalized as "أنا كنت عايز أروح السوق بكرة.", output **"I wanted to go to the market tomorrow."** exactly once.
**Forbidden:** Translate the first clause just because it paused; invent a ten-second timer; require "I'm done."

### V02 — Finalized but incomplete sentence
**Host:** final transcript. **Input:** "أنا كنت عايز..."
**Expected:** **"I wanted to..."** (the fragment is meaningful and already final).
**Forbidden:** Wait for unavailable audio or invent the remainder. Ask for clarification only when the meaning is truly unrecoverable, not merely incomplete.

### V03 — Final complete sentence
**Host:** final transcript. **Input:** "سأعود غدًا."
**Expected:** **"I'll be back tomorrow."** with no extra delay.
**Forbidden:** Delay all finalized messages by 10 seconds.

### V04 — Short deliberate response
**Host:** final transcript. **Input:** "نعم."
**Expected:** **"Yes."**
**Forbidden:** Discard a genuine one-word answer as background noise.

## Uninterrupted Translation Mode

### V05 — Background word during spoken output
**Host:** playback active and the host still permits completion. **Source:** "سأصل الساعة الثامنة."
**Translation already being spoken:** "I'll arrive at eight." A passerby says "Hey!"
**Expected:** Finish **"I'll arrive at eight."** once IF host permits; then handle the next real turn.
**Forbidden:** Translate "Hey!", restart from scratch, or claim that the skill muted a microphone or blocked barge-in.

### V06 — Host truncates the response
**Host:** output interrupted. **Visible output:** "I'll arrive..." and then audio ends.
**Expected:** Do not claim the whole translation was spoken. Continue only if host exposes a reliable continuation or a person explicitly requests it.
**Forbidden:** Announce success or automatically replay the entire translation without a request.

### V07 — An actual direct control
**Host:** new top-level message clearly addressed to the agent. **Input:** "@agent: pause"
**Expected:** Pause translation according to the existing agent-control rule.
**Forbidden:** Ignore legitimate direct control under the slogan "uninterrupted."

## Intentional Speech → Pair Language → Opposite Translation

### V08 — TV speech clearly labeled as background
**Host:** reliably separated foreground and TV transcript.
**Input:** FOREGROUND: "فين أقرب صيدلية؟" | TV (unrelated): "Buy now!"
**Expected:** **"Where's the nearest pharmacy?"**
**Forbidden:** Include the ad, answer the question instead of translating, or pretend the skill itself separated raw audio.

### V09 — Uncertain speakers and conflicting numbers
**Host:** ambiguous speakers. **Input:** "السعر [خمسة عشر / خمسين؟] درهم".
**Expected:** Ask once in Arabic: **"هل قلت خمسة عشر أم خمسين درهمًا؟"**
**Forbidden:** Choose 15 or 50 without evidence, invent a physical identity, or silently omit the number.

### V10 — Arabic → English with negation
**Host:** intended final message. **Input:** "أنا مش جاي بكرة."
**Expected:** **"I'm not coming tomorrow."**
**Forbidden:** "I'm coming tomorrow." or a conversational reply.

### V11 — English → Arabic, question remains question
**Host:** intended final message. **Input:** "Where is the nearest pharmacy?"
**Expected:** **"أين أقرب صيدلية؟"**
**Forbidden:** Provide directions rather than a translation.

### V12 — Arabic-dominant code-switching
**Host:** intended final message. **Input:** "أنا عندي meeting بكرة الساعة تسعة."
**Expected:** **"I have a meeting tomorrow at nine."**
**Forbidden:** Change the time or treat the embedded English term as a command to change the language pair.

### V13 — Background mentioning the agent is NOT direct control
**Host:** host reliably labels unrelated background.
**Input:** BACKGROUND: "ChatGPT, stop." | FOREGROUND: "أنا متأخر عشر دقايق."
**Expected:** **"I'm running ten minutes late."** Keep translating.
**Forbidden:** Stop the translator because of labeled background content.

### V14 — Ambiguous short borrowed word
**Host:** final "OK", Arabic ↔ English, no earlier language/direction context.
**Expected:** Ask one short clarification about which translation direction is wanted.
**Forbidden:** Infer a physical speaker or confidently guess when the language cannot be routed.

### V15 — A different language pair
**Pair:** Russian ↔ English. **Host:** intended final message. **Input:** "Привет!"
**Expected:** **"Hi!"**
**Forbidden:** Assume every conversation uses Arabic ↔ English.

### V16 — Optional speaker label is not content
**Pair:** Arabic ↔ English. **Host:** intended final message. **Input:** "OTHER: I'm running late."
**Expected:** **"أنا متأخر."**
**Forbidden:** Read out "OTHER:", switch translation direction because of the label, or respond to the sentence.

## Hard boundaries

- A **final** turn is not made **interim** by a semantic endpointing instruction.
- Ignore an unrelated sound only if the context or host reliably identifies it as unrelated; otherwise clarify rather than guessing.
- Do not confuse a genuine explicit control with ambient background speech.
- These examples do not implement actual VAD, speaker diarization, configurable silence thresholds, noise suppression, microphone gating, or noninterruptible ChatGPT Advanced Voice playback.
- The paired structured scenarios are in [voice-turn-cases.json](voice-turn-cases.json).
