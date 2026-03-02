# LinkedIn Post: The D/P Framework

## Version 1: Main Post (Recommended - This is what to post)

---

**Your AI product isn't "AI-powered."**

It's a specific combination of deterministic (D) and probabilistic (P) steps. And the pattern you choose changes everything — reliability, cost, UX, where your guardrails need to go.

I've built AI products at Amazon, Verizon, and now at Walmart. The teams that shipped the most reliable AI features all shared one insight: they stopped thinking about "is this AI or not" and started thinking about "D or P at each step."

Here's the framework:

**Deterministic (D):** Same input → same output. Database queries. Form validation. If/else logic. You can unit test it.

**Probabilistic (P):** Same input → different output. LLM calls. Classifiers. Recommendations. You test for *properties*, not exact matches.

Most people think real AI products are P → P → P. Wrong.

**The real patterns:**

D → P: User input → LLM generates output (most "AI-powered" products). Risk: bad output feels like your bug.

P → D: AI classifies messy input → deterministic system handles it. Risk: wrong classification breaks downstream flow. **PM decision: confidence threshold?** 70% sure or 90%?

D → P → D: **THE SANDWICH.** Structured input → AI extracts/transforms → structured output. (Gmail smart reply, document OCR, invoice parsing). Safest. Most common in production.

P → P → P: Full AI (ChatGPT, Claude). Errors compound. Needs human checkpoints.

The insight that changes your product decisions:

Every boundary between D and P is a **design decision** you're already making — usually without realizing it.

D → P boundary? You're deciding: how much context to give the AI, what format to request, how to handle hallucination.

P → D boundary? You're deciding: what confidence score triggers the handoff, what happens when the AI is uncertain, do we escalate or fail gracefully.

The PMs who ship reliable AI products aren't the ones who understand transformers better than their engineers. They're the ones who *explicitly map their workflow as a sequence of D's and P's* and make each boundary decision intentional.

I wrote a deeper breakdown at fullstackpm.tech/blog if you want the 8 three-step patterns and real-world examples.

What pattern is your current AI product? D→P? P→D? The sandwich?

---

## Version 2: Thread Format (Alternative - Posts as 5 tweets)

---

1/ Your AI product isn't "AI-powered."

It's a specific sequence of deterministic (D) and probabilistic (P) steps stitched together.

The pattern you choose determines reliability, cost, UX, and where your guardrails need to go.

Here's the framework I use.

2/ Two definitions:

**Deterministic (D):** Same input → same output. Always. Database query. Form validation. Unit testable.

**Probabilistic (P):** Same input → different output. LLM call. Classifier. Confidence score. Test for properties, not exact matches.

3/ The four basic 2-step patterns:

D→D: Traditional software (no AI)
D→P: User input → LLM output (most "AI-powered" tools)
P→D: AI classifies messy input → deterministic system
P→P: Full AI (ChatGPT). Errors compound.

4/ The one people get wrong:

Most assume real AI products are P→P→P.

Wrong. The most reliable AI in production is:

**D→P→D: The Sandwich**

Structured input → AI transforms it → structured output

Gmail. Email parsing. Document OCR. Invoice extraction.

5/ The real insight:

Every D-to-P and P-to-D boundary is a PM design decision.

Confidence thresholds. Context windows. Hallucination handling.

Map your workflow as D's and P's. Make each boundary intentional.

That's how you ship reliable AI products.

Read the full breakdown: fullstackpm.tech/blog

---

## Version 3: Shorter Version (If you want to test)

---

I built AI products at Amazon, Verizon, and Walmart.

The most reliable ones share a pattern: they think in **deterministic (D) and probabilistic (P) steps**.

D = Same input, same output (database query, validation)
P = Same input, different output (LLM call, classifier)

**The 4 basic patterns:**

D→D: Traditional software
D→P: User input → LLM output ← Most "AI-powered" products
P→D: AI classifies → deterministic system routes it
P→P: Full AI (hardest to make reliable)

**The winner in production?** D→P→D (The Sandwich):
- Structured input
- AI transforms it
- Structured output

Gmail smart reply. Email parsers. Document OCR.

Why? Because every boundary between D and P is a **PM decision** about confidence thresholds, context, and error handling.

Map your workflow as D's and P's. Make each boundary intentional.

That changes how you ship reliable AI.

fullstackpm.tech/blog

---
