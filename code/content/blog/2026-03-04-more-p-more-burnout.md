---
title: "More P = More Burnout: The Hidden Cost of AI Doing Your D Work"
date: 2026-03-04
tags: [product-management, ai, ai-native-pm, burnout, career]
excerpt: "AI is offloading your deterministic work. Great. But what's left is concentrated probabilistic work — the kind that exhausts humans and compounds risk exponentially across every layer of decision-making."
author: "Harsha Cheruku"
---

Here's something nobody warns you about when AI takes over your grunt work:

**You don't get less tired. You get differently tired.**

AI writes the first draft. AI summarizes the research. AI generates the test cases. AI pulls the data. You're "more productive" by every metric that matters to your manager.

And yet you're more exhausted than before.

That's not a paradox. That's the math of D/P rebalancing.

---

## The Concentration Effect

In [The D/P Framework](/blog/deterministic-probabilistic-workflow-patterns), I introduced the idea that every workflow is a mix of deterministic (D) and probabilistic (P) steps.

In [Life in D/P](/blog/life-in-dp), I showed this pattern is everywhere — not just in products.

In [Part 3](/blog/when-ai-masters-d-p-becomes-career-leverage), I argued that as AI absorbs D work, P work becomes your career leverage.

This post is the part I left out: **what concentrated P work actually does to you.**

Here's what a PM's day used to look like:

```
D — Pull metrics dashboard
P — Interpret what the metrics mean
D — Write the PRD section on requirements
P — Decide which requirements to cut
D — Set up the A/B test
P — Decide what "success" looks like
D — Summarize user research notes
P — Decide which user pain matters most
```

Notice the rhythm? D-P-D-P-D-P. The deterministic steps gave your brain a break. Writing a PRD section isn't intellectually demanding — it's structured, repeatable, almost meditative. It's the cognitive equivalent of a rest between sets at the gym.

Now remove every D:

```
P — Interpret what the metrics mean
P — Decide which requirements to cut
P — Decide what "success" looks like
P — Decide which user pain matters most
```

Same output. Half the time. Twice the cognitive load.

**You didn't remove work. You removed the rest.**

---

## P Work Is Calorically Expensive

This isn't hand-wavy. There's a real neurological reason P work exhausts you faster.

Deterministic work uses **procedural memory** — the part of your brain that handles routines. It's low-energy. You can write a status update while half-asleep because you've done it hundreds of times.

Probabilistic work uses **executive function** — the prefrontal cortex doing active reasoning under uncertainty. This is the most energy-expensive cognitive mode your brain has. It's why you feel drained after a 2-hour strategy meeting but fine after a 4-hour coding sprint where you knew exactly what to build.

When AI removes your D work, it doesn't free up time. It **compresses your day into wall-to-wall executive function.** Every hour is now a decision under uncertainty, a trade-off evaluation, a judgment call with incomplete information.

Your calendar looks lighter. Your brain is working harder than ever.

---

## The Compounding Risk Problem

Here's where it gets dangerous. More P work doesn't just mean more fatigue — it means **exponentially more risk**.

Every P decision carries uncertainty. That's the definition. But P decisions don't exist in isolation. They stack. And when they stack, the uncertainty multiplies.

### A simple example:

You're launching a new feature. At each layer, you make a P call:

| Layer | Decision | Confidence |
|-------|----------|------------|
| **Strategy** | "This market segment is worth entering" | 70% |
| **Product** | "This is the right feature for that segment" | 75% |
| **Design** | "This UX will resonate with these users" | 80% |
| **Engineering** | "This architecture will scale for this use case" | 85% |
| **Launch** | "This go-to-market approach will reach them" | 75% |

Each decision feels reasonable on its own. 70-85% confidence is solid.

But the combined probability?

**0.70 × 0.75 × 0.80 × 0.85 × 0.75 = 0.267**

You're at **27% confidence** by the time the feature reaches the user. And every single layer felt like a good bet.

That's the compounding problem. **P risk doesn't add across layers — it multiplies.** Five reasonable bets stacked together become a long shot.

---

## Why More Layers Make It Worse

In the old world, most of those layers had heavy D components that anchored the uncertainty:

- Strategy had market sizing models (D) feeding the market entry decision (P)
- Design had usability heuristics (D) constraining the UX choices (P)
- Engineering had proven patterns (D) reducing architecture risk (P)

The D steps acted as **guardrails on the P decisions**. They narrowed the uncertainty at each layer before passing it to the next.

Now picture the AI-accelerated version. AI handles the D work at each layer faster. Great. But if the P decisions at each layer stay the same quality — or get worse because the human is fatigued — the compounding effect is identical. You just arrive at 27% confidence faster.

**Speed without improved judgment compounds errors faster, not slower.**

And here's the insidious part: because each layer moves faster, you stack more P decisions in the same time period. More bets per quarter. More compounding. More risk — at higher velocity.

---

## The Exhaustion-Error Spiral

This is where burnout meets compounding risk, and they make each other worse.

**Step 1:** AI removes your D work. Your day becomes concentrated P.

**Step 2:** Concentrated P work exhausts your executive function faster.

**Step 3:** Fatigued executives make worse P decisions. Decision quality degrades — especially later in the day, later in the week, later in the quarter.

**Step 4:** Worse P decisions at any layer reduce confidence at that layer — say from 75% to 60%.

**Step 5:** Lower confidence at one layer multiplies through every downstream layer.

**Step 6:** Worse outcomes. More firefighting. More P decisions to make. More exhaustion.

**Repeat.**

This is a spiral, not a line. Burnout doesn't just make you feel bad. It degrades the quality of the most important work you do — the decisions that compound through every layer of your product, your team, your strategy.

And the cruel part? The people most affected are the senior leaders and PMs doing the most P-heavy work. The exact people whose judgment matters most are the ones most likely to be running on fumes.

---

## AI Has Its Own Version of This Problem

Humans aren't the only ones who suffer from concentrated P work. AI does too — just in a different currency.

**For humans, the cost of P is cognitive energy.** Decision fatigue, burnout, degraded judgment.

**For AI, the cost of P is tokens.** More uncertainty means more reasoning, more context, more chain-of-thought, more compute.

A deterministic task — "convert this CSV to JSON" — costs almost nothing. Minimal tokens, instant response, near-zero error.

A probabilistic task — "analyze this market and recommend a strategy" — costs orders of magnitude more. Longer prompts, more reasoning chains, more output tokens, higher hallucination risk.

And just like humans, AI's P quality degrades under load:

- **Longer contexts** → more hallucination risk (attention diffuses)
- **More complex reasoning** → more reasoning errors (chains break down)
- **Stacked P decisions** → same compounding math applies (each uncertain step multiplies through)

Tokens are AI's calories. And P work burns through them fast.

The parallel is almost exact: remove the easy D work, concentrate the hard P work, and watch quality degrade under the cognitive (or computational) load.

---

## The Uncomfortable Truth About Productivity

So here's the picture:

AI makes you faster at D. Undeniably.

But it also:
- **Concentrates** your work into wall-to-wall P decisions
- **Removes** the cognitive rest that D work provided
- **Accelerates** the rate at which P decisions stack and compound
- **Multiplies** the risk because more bets per quarter means more compounding
- **Degrades** your judgment because sustained P work exhausts executive function

The productivity gain is real. So is the burnout.

And they're not separate problems. **The productivity gain IS the burnout.** You're producing more by concentrating your effort into the hardest possible work with no breaks. That's not sustainable. It's a sprint pace on a marathon course.

---

## What Actually Helps

I don't have a clean answer for this — it's something I'm working through myself. But here's what I've noticed actually makes a difference:

### 1) Reintroduce D breaks deliberately

Your D work used to give you natural cognitive rest. AI took that away. Put it back — intentionally.

Between heavy P sessions, do something deterministic: organize your files, review a checklist, clean up a doc. Not because it's productive — because your prefrontal cortex needs the downtime.

### 2) Batch your P work

Don't spread decisions across the day. Cluster your hardest P calls into your peak cognitive hours (usually morning). Protect those hours. No meetings, no Slack, no context-switching.

Everything else — execution, communication, follow-ups — goes in the afternoon when your executive function is winding down.

### 3) Reduce layers where possible

Every layer you add multiplies risk. Before adding a new decision layer, ask: can we collapse two layers into one? Can we make a decision once that eliminates the need for a downstream decision entirely?

The best product decisions aren't the ones that create options. They're the ones that **eliminate future decisions**.

### 4) Build D rails around your P decisions

This was the key insight from Part 3. You can't eliminate P, but you can constrain it:

- **Pre-mortems** — define failure before it happens
- **Kill criteria** — decide in advance what would make you stop
- **Decision journals** — capture reasoning so you're not re-deciding the same thing under fatigue
- **Confidence thresholds** — explicitly state your confidence level so you can spot when compounding pushes you below acceptable risk

### 5) Recognize the spiral early

When you notice decision quality dropping — when you start deferring, overthinking, or making reactive choices — that's the exhaustion-error spiral starting.

The move isn't to push through. It's to stop making P decisions for the rest of the day. Seriously. Go do D work. Or go do nothing. The cost of a delayed good decision is almost always less than the cost of a fast bad one that compounds through five layers.

---

## The Equation Nobody Talks About

The AI productivity narrative says: **more output, less effort.**

The D/P reality says: **more output, different effort — and the new effort is cognitively unsustainable at the pace we're running.**

AI didn't eliminate your hard work. It distilled it.

What's left is the purest, most concentrated form of cognitive labor — the decisions that define outcomes, carry risk, and compound through every layer of everything you build.

That's incredibly powerful. It's also incredibly exhausting.

And until we start designing our work around that reality — instead of pretending AI just "frees up time" — the burnout will keep getting worse while the productivity dashboards keep looking better.

The numbers will say you're crushing it.
Your brain will know the truth.

---

*Part 4 of the AI-Native PM series. Part 1: [The D/P Framework](/blog/deterministic-probabilistic-workflow-patterns). Part 2: [Life in D/P](/blog/life-in-dp). Part 3: [When AI Masters D, P Becomes Career Leverage](/blog/when-ai-masters-d-p-becomes-career-leverage).*
*Building in public at [fullstackpm.tech](https://fullstackpm.tech). Follow along on [X @fullstackpmtech](https://x.com/fullstackpmtech).*
