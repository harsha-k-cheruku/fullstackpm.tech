---
title: "The D/P Framework: Why Every AI Product Is a Mix of Deterministic and Probabilistic Steps"
date: 2026-03-01
tags: [product-management, ai, ai-native-pm, architecture, frameworks]
excerpt: "Your AI product isn't 'AI-powered.' It's a specific combination of deterministic and probabilistic steps — and knowing which is which changes every decision you make as a PM."
author: "Harsha Cheruku"
---

In my last post on [what makes a PM AI-native](/blog/what-is-an-ai-native-pm), I talked about how AI-native PMs design for probabilistic outputs instead of deterministic ones.

But here's what I didn't say: **no real product is fully probabilistic.** And no product worth building today is fully deterministic either.

Every AI product you've ever used is a *hybrid* — a specific sequence of deterministic (D) and probabilistic (P) steps stitched together. And the pattern you choose changes everything: the reliability, the cost, the user experience, and where your guardrails need to go.

This is the framework I use to think about it.

---

## Two Types of Steps

Let's define terms simply.

**Deterministic (D):** Same input, same output. Every time. A database query. A form validation. An if/else branch. You can write a unit test for it and it passes 100% of the time.

**Probabilistic (P):** Same input, *different* output. An LLM call. A recommendation engine. A classifier with a confidence score. You can't write a unit test that expects an exact string — you test for *properties* (length, format, absence of hallucination) and accept a pass rate.

Every step in a workflow is one or the other. And once you see it this way, the architecture of every AI product becomes a sequence of D's and P's.

---

## The Four Basic Patterns (Two-Step Workflows)

With just two steps, you get four combinations. Each one is a real product pattern.

### D → D: Pure Traditional

**Input is structured. Output is structured. No AI involved.**

*Example:* User clicks "Add to Cart" → item is added to cart. Form submitted → row inserted in database.

This is every CRUD app ever built. Nothing probabilistic. Nothing uncertain. Tests are easy. QA is straightforward. The PM's job is well-understood.

Still the backbone of most software. And that's fine — not everything needs AI.

### D → P: The AI Finisher

**Structured input feeds into an AI step that generates the output.**

*Example:* User types a search query (structured text) → LLM generates a natural language answer. User fills out a form with project details → AI generates a PRD draft.

This is the most common "let's add AI" pattern. You take an existing deterministic flow and replace the last mile with something generative. It's also the pattern most people mean when they say "AI-powered."

**PM decision:** How do you handle it when the AI output is wrong? The user gave you clean input — they expect clean output. If the PRD draft is nonsensical, that's your product's failure, not the user's.

### P → D: The AI Front Door

**AI processes messy input, then hands off to a deterministic system.**

*Example:* AI classifies an incoming support ticket (P) → ticket gets routed to the right queue and a template response is sent (D). AI extracts structured fields from an uploaded invoice (P) → data is saved to the database (D).

This is underrated and incredibly powerful. The AI handles the *ambiguity* at the top of the funnel, then everything downstream is reliable, testable, and predictable.

**PM decision:** What's the confidence threshold for the handoff? If the AI is 70% sure this is a billing ticket, do you route it? 90%? This threshold IS your product decision — and it's one most PMs don't even realize they're making.

### P → P: Fully Probabilistic

**AI in, AI out. No deterministic checkpoint.**

*Example:* AI reads a document and identifies key themes (P) → AI generates a summary based on those themes (P). AI interprets a user's vague request (P) → AI writes code to fulfill it (P).

This is the pattern behind ChatGPT, Claude, and most "magic" AI experiences. It's also the hardest to make reliable, because errors in step 1 compound in step 2. A misidentified theme becomes a wrong summary. A misinterpreted request becomes wrong code.

**PM decision:** Where do you insert the human checkpoint? Between step 1 and step 2 (show the themes before summarizing)? After step 2 (show the output for approval)? Or both? The answer depends on how expensive a mistake is.

---

## The Eight Three-Step Patterns

Real products usually have three or more steps. Here's where it gets interesting — and where PM intuition starts to matter.

### D → D → D: Pure Traditional
*Click button → validate input → write to database.*

Nothing to see here. It's the world we came from.

### D → D → P: AI Finish
*User uploads CSV → system validates format → AI generates insights report.*

The AI only touches the final output. Everything before it is rock-solid. This is low-risk AI integration — if the report is weird, the data is still safe and the user can regenerate.

**Real-world:** Stripe Radar. Transaction data (D) is processed through rules (D), then an ML model scores fraud risk (P).

### D → P → D: The AI Sandwich

*User uploads a document → AI extracts entities and fields → structured data is saved to database.*

**This is the most common pattern in production AI products.** Deterministic bookends with AI in the middle. The input is clean, the output is clean, and the AI does the hard part in between.

**Real-world:** Every "smart form" that reads a PDF. Every email parser that extracts flight details into a calendar event. Every OCR-to-database pipeline.

**Why PMs love this pattern:** You control the edges. If the AI step fails, you can fall back to manual input. The blast radius is contained.

### D → P → P: AI Takeover

*User writes a prompt → AI plans the approach → AI executes the plan.*

The user provides structured input, then it's AI all the way. This is the pattern behind AI coding assistants (user describes feature → AI plans implementation → AI writes code) and AI research tools (user asks question → AI decides what to search → AI synthesizes answer).

**PM decision:** Do you show the plan before execution? Claude Code does — it proposes changes before making them. That intermediate checkpoint between the two P steps is a *product design choice* that dramatically affects trust.

### P → D → D: AI Front Door

*AI classifies an incoming email → routes to correct department → sends templated acknowledgment.*

AI handles the ambiguity at entry, then everything is deterministic. This is behind every smart triage system, every auto-categorization feature, every "AI routing" you've seen.

**Real-world:** Gmail's priority inbox. AI classifies importance (P) → email is placed in the right tab (D) → notification rules apply (D).

### P → D → P: AI Bookends

*AI transcribes a meeting → transcript is stored and timestamped → AI generates action items and summary.*

Two different AI steps with a deterministic save in the middle. The transcript step and the summary step are independent — if the summary is bad, you still have the transcript. If the transcription has errors, the summary inherits them.

**Real-world:** Otter.ai, Fireflies, and every AI meeting assistant. The deterministic middle (storage, timestamps, speaker labels) is what makes the product useful even when the AI steps aren't perfect.

### P → P → D: AI Pipeline

*AI reads resumes and extracts skills → AI scores candidate-job fit → candidates are ranked and filtered by deterministic rules.*

Two AI steps feeding into a final deterministic sort. The AI does the understanding, the system does the deciding. This is common in ML pipelines where a model processes data, another model scores it, and business rules determine the output.

**Real-world:** LinkedIn job matching. Recommendation models process your profile (P) → scoring model ranks jobs (P) → business rules filter by location, salary, sponsorship (D).

### P → P → P: Pure AI-Native

*AI interprets user intent → AI reasons about the approach → AI generates the output.*

This is the frontier. No deterministic checkpoint at any stage. It's what happens when you talk to ChatGPT or Claude without any structured interface — just natural language in, natural language out, with reasoning in between.

**Real-world:** Open-ended AI chat. AI agents that plan and execute autonomously. This is where the most impressive demos live — and also where the most spectacular failures happen.

**PM decision:** If you're building here, your entire job is *designing the guardrails around a process you can't fully predict.* Confidence thresholds, output validation, human escalation paths, and graceful degradation are your product.

---

## The Pattern That Matters: Every Boundary Is a Decision

Here's the insight that makes this framework useful in practice:

**Every D→P boundary is a prompt design decision.** You're feeding structured data into something probabilistic. How you structure that handoff — what context you include, what format you use, what examples you provide — determines output quality.

**Every P→D boundary is a guardrail decision.** You're taking probabilistic output and feeding it into something that expects certainty. What's the confidence threshold? What happens when the AI is unsure? Do you reject, escalate to a human, or fall back to a default?

The more boundaries your workflow has, the more design decisions you're making. And most PMs don't realize they're making them.

---

## How to Use This Framework

Next time you're scoping an AI feature, try this:

1. **Map your workflow as a sequence of D's and P's.** Write it out. "User uploads file (D) → AI extracts data (P) → data is validated (D) → AI generates report (P)." That's D → P → D → P.

2. **Identify every boundary.** Each D→P and P→D transition is a design decision you need to make explicitly.

3. **Ask: where does the human go?** For every P step, decide whether the user sees intermediate output or not. More checkpoints = more trust, slower flow. Fewer checkpoints = faster, riskier.

4. **Design your fallbacks.** For every P step, what happens when it fails? Can you fall back to D? Can the user retry? Is the failure silent or visible?

5. **Count your P→P chains.** Every consecutive P step compounds uncertainty. If you have three P steps in a row, errors from step 1 cascade through steps 2 and 3. This is where you need the most robust evaluation and the clearest human escape hatches.

---

## Where This Is Going

I'm working on something that applies this framework directly: an AI agent that handles associate-level PM tasks. Some of those tasks are naturally deterministic (updating a tracker, sending a status template). Some are naturally probabilistic (drafting a PRD from a vague request, synthesizing user research). And some are hybrid.

The interesting product challenge isn't "can AI do PM work?" — it's "for each PM task, what's the right D/P pattern, and where does the human PM step in?"

More on that soon.

---

*This is Part 2 of the AI-Native PM series. Part 1: [What Is an AI-Native PM?](/blog/what-is-an-ai-native-pm) covered the four things that make a PM truly AI-native. This post digs into the architectural thinking behind designing AI workflows.*

*Building in public at [fullstackpm.tech](https://fullstackpm.tech). Follow along on [X @fullstackpmtech](https://x.com/fullstackpmtech).*
