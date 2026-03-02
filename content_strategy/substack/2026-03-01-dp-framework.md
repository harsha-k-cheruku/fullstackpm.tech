# Substack Format: The D/P Framework

## Option 1: Full Article (Repost the blog post)

Copy the entire article from fullstackpm.tech and paste it directly into Substack. Add this at the top:

---

**This is Part 2 of the AI-Native PM series.**

Part 1: [What Is an AI-Native PM? (And Why It's Not What You Think)](https://fullstackpm.tech/blog/what-is-an-ai-native-pm)

---

## Option 2: Excerpt + Link (Recommended - Drives traffic)

---

**Subject line:** The D/P Framework: Why Your AI Product Is a Mix of Deterministic and Probabilistic Steps

**Preview text:** How to think about workflow architecture so your AI products actually ship reliably.

---

I built AI products at Amazon (marketplace, fraud detection), Verizon (data analytics, ML), and now at Walmart (AI agents, analytics transformation).

The most reliable ones share one insight: they don't ask "is this AI or not?" They ask "**deterministic or probabilistic at each step?**"

Here's what that means:

**Deterministic (D):** Same input → same output, always. Database query. Form validation. If/else logic. You can unit test it.

**Probabilistic (P):** Same input → different output. LLM call. Classifier. Recommendation. You test for properties (length, format, no hallucination), not exact matches.

Once you see your workflow as a sequence of D's and P's, everything changes. Suddenly:
- You know where errors compound
- You know where to put human checkpoints
- You know which patterns actually work in production

**The four basic patterns (2 steps):**

1. **D → D:** Traditional software. No AI. (Click button → add to cart)
2. **D → P:** Most "AI-powered" products. (User input → LLM output). Risk: Bad output = your product's failure.
3. **P → D:** AI handles ambiguity upfront. (AI classifies ticket → route to queue). Risk: Confidence threshold decisions.
4. **P → P:** Full AI (ChatGPT, Claude). Errors compound. Needs explicit human checkpoints.

**But here's what production AI actually looks like:**

Not P → P → P.

**D → P → D. The Sandwich.**

Structured input. AI extracts/transforms. Structured output.

- Gmail smart reply
- Document OCR
- Email parsing (extract flight details into calendar)
- Invoice field extraction

Why does this pattern win?

Because you control the edges. The input is clean. The output is clean. The AI does the hard part in the middle.

**The insight that changes your PM decisions:**

Every boundary between D and P is a decision you're making — usually without realizing it.

*D → P boundary:* How much context? What format? How to handle hallucination?
*P → D boundary:* What confidence threshold triggers the handoff? What happens if the AI is unsure?

The PMs shipping reliable AI aren't the ones with the deepest ML knowledge. They're the ones who **explicitly map their workflow as D's and P's** and make each boundary decision intentional.

**I wrote a deeper breakdown with all 8 three-step patterns and real-world examples on the blog.**

[Read the full article on fullstackpm.tech](https://fullstackpm.tech/blog/deterministic-probabilistic-workflow-patterns)

---

**P.S.** This is Part 2 of the AI-Native PM series. Part 1 is "What Is an AI-Native PM? (And Why It's Not What You Think)" — it covers the 4 things that make PMs actually think differently about AI, not just use ChatGPT faster.

---

## Option 3: Newsletter Format (If you're sending weekly)

---

**[FULL STACK PM] March: D/P Framework for AI Products**

Hey there,

This month I've been thinking deeply about how to architect AI products so they're actually reliable.

I just published a framework I use: **deterministic vs probabilistic steps.**

It's simple but changes how you make PM decisions around AI.

---

**📖 WHAT I'M READING**

[Add 3-5 top reads from your reading stack]

---

**🔨 WHAT I'M BUILDING**

I shipped the D/P Framework post this week as Part 2 of the AI-Native PM series.

The insight: real AI products aren't fully probabilistic (P→P→P). The most reliable ones are D→P→D — structured input, AI in the middle, structured output. Gmail. Email parsers. Document extraction.

Once you see your workflow as a sequence of D's and P's, every boundary becomes a decision: confidence thresholds, context windows, error handling.

That's when you ship reliable AI.

---

**💡 ONE THING I BELIEVE**

Most PMs think "how do we add AI?" when they should think "at which step does AI make this better?" and "who decides when we trust the AI output?"

The framework helps you answer both.

---

That's it for this month.

→ [Read the D/P Framework article](https://fullstackpm.tech/blog/deterministic-probabilistic-workflow-patterns)

— Harsha
@fullstackpmtech | fullstackpm.tech

P.S. Part 1 on what makes a PM "AI-native" hit differently than I expected. If you missed it, it's worth reading before this one.

---
