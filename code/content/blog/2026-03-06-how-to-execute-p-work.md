---
title: "The Three Types of P Work Failures and Where to Put Your Human Checkpoints"
date: 2026-03-06
author: "Harsha Cheruku"
tags: ["AI", "product-management", "deterministic-probabilistic", "p-work", "risk-management"]
---

# The Three Types of P Work Failures and Where to Put Your Human Checkpoints

In the last article, we diagnosed the problem: **as AI automates deterministic (D) work, you're left doing more probabilistic (P) work — and P work is cognitively expensive and dangerous.** You're making more decisions, with less structure, in more ambiguous contexts, with errors that compound in unpredictable ways.

But knowing you have a problem isn't the same as knowing how to fix it.

The real question is: **Where do you put the human to catch errors before they cascade?**

This article is diagnostic, not prescriptive. It's about understanding the three types of P work failures so you can place your human checkpoints where they'll actually catch errors. In the next article, we'll get operational and build the checklist.

---

## Part 1: Why P Work Is Dangerous (And Why Your Instincts Are Right)

Let's start with why P work feels different. You've probably noticed it—a bug in D work hurts in one place. A mistake in P work ripples.

### D Work Errors Are Localized

When your code has a bug, it's usually isolated. Your login function breaks logins. Your payment processor fails, it fails on that transaction. The blast radius is defined. You can roll back. You can hotfix. You can measure exactly what went wrong.

This is the gift of deterministic work: **errors are bounded.**

### P Work Errors Compound

P work errors don't stay put. They cascade.

Imagine you're a PM at an e-commerce company and AI recommends a product ranking algorithm. The algorithm looks good in testing: engagement up 8%, revenue up 3%. You approve it.

But there's a subtle bias in the algorithm—it surfaces products that get clicks but have poor reviews. Users click through, feel disappointed, trust the platform less. Repeat this across thousands of users. Now users stop checking recommendations. Engagement drops. You lose the 8% gain *and* destroy credibility you spent months building.

The error wasn't in the algorithm itself. It was in your judgment about *what to optimize for*. And that judgment error cascaded into multiple downstream failures: user trust, platform credibility, engagement metrics.

Here's another: AI flags a resume candidate as a "strong cultural fit" based on linguistic patterns. You interview them, they seem good. You hire them. Six months later, they're siloed from the team because the "cultural fit" was actually just linguistic similarity to existing team members. Your hiring decision cascaded into team dynamics issues, onboarding problems, potential turnover.

**The pattern:** P work errors don't have a clear boundary. They ripple across time, across users, across systems in ways you can't fully predict or measure.

### Errors Compound in Uncertainty

Here's the really insidious part: **when you're doing P work, you often don't know when you've made an error.**

With D work, you get feedback. The unit test fails. The database query returns wrong data. The API times out. Concrete feedback, clear signal.

With P work, the feedback is noise. The algorithm ranked products in an order that seemed right, but the downstream effect was subtle. The resume candidate had a linguistic pattern that looked like culture fit, but it was actually homogeneity. You *made a decision*, but you won't know if it was right for months—if ever.

This is why P work decisions feel like shooting in the dark. Not because you're bad at judgment, but because **judgment operates with fundamentally incomplete feedback loops.**

You approve the algorithm Tuesday. Revenue looks good Wednesday. But the user trust degradation doesn't show up until users have had 50 disappointments. By then, the decision was months ago. The causal link is invisible.

**This is the burnout engine:** You're making decisions in darkness, with no clear feedback, with errors that ripple unpredictably, and you're responsible for all of it.

---

## Part 2: The Three Types of P Failures (And How to Recognize Them)

Not all P work failures are the same. Understanding the type of failure tells you where to put your checkpoint.

### Type 1: Hallucination Failures

**The error:** The AI system confidently generates something that sounds right but is factually wrong.

**Example:** A Gen-AI tool reads a legal contract and summarizes the indemnification clause. The summary sounds plausible. It uses legal language. It flows naturally. But it's inverted the clause—it says the liability flows the opposite direction. A lawyer who doesn't read the original would approve it. Downstream: Your company signs a deal where they're liable when they shouldn't be. Contract law doesn't care that the AI sounded confident.

**Why it's dangerous:** Hallucinations don't feel like errors. They *feel* like knowledge. The system is coherent, confident, textured with detail. Your brain doesn't flag it as suspect.

**Type 1 failures are seductive.** They bypass your skepticism because they're *so well-formed*.

**Other examples:**
- AI generates a customer support response that's grammatically perfect but gives wrong information about a return policy
- Summarization AI condenses a research paper and invents a finding that didn't exist in the original
- Recommendation engine suggests a product combination that's technically incompatible but the description sounds like they'd work together

### Type 2: Misunderstanding Failures

**The error:** The AI system interprets the context or intent differently than you expected, leading to a technically correct output that's fundamentally wrong for your use case.

**Example:** You ask AI to optimize your email campaign for "engagement." It does—by recommending clickbait subject lines that generate clicks but tank conversion rates. The AI understood "engagement" as clicks. You meant "engagement leading to purchase." Same word. Different intent.

**Why it's dangerous:** Misunderstanding failures look like the system did what you asked. You asked for optimization—it optimized. But the proxy you chose (clicks) diverged from what you actually wanted (revenue + retention).

**This is the alignment problem in miniature.** The AI isn't broken. Your specification was incomplete.

**Other examples:**
- AI routes customer support tickets to agents based on historical response time (efficient), missing that faster responses came on simple tickets and the complex ones sat longer
- Hiring recommendation system suggests candidates with highest test scores (following your spec), but the test doesn't correlate with on-the-job performance
- Product recommendation system surfaces products that maximize *watch-time* (your metric), not satisfaction, because you didn't specify satisfaction

### Type 3: Drift Failures

**The error:** The AI system worked correctly in training, but the real-world context has shifted in ways the system wasn't designed for.

**Example:** Your churn prediction model was trained on pre-pandemic customer behavior. It predicted which customers would churn in 2019-2021. Now it's 2026. Customer priorities have shifted. What signals predicted churn then don't predict it now. The model doesn't know about new competitors. It doesn't know about the inflation that changed customer spending patterns. You're using 2019 logic in 2026 reality.

**Why it's dangerous:** Drift failures are *slow*. The model performs fine in Month 1 of the new context. Month 2, it's slightly off. Month 6, it's systematically wrong. But because the decay is gradual, you don't notice until you've made 50 decisions based on faulty predictions.

**Other examples:**
- Language model trained on 2024 data doesn't understand 2026 slang or cultural references
- Demand forecasting model trained on pre-supply-chain-crisis data doesn't account for new logistics constraints
- Fraud detection model trained on pre-sophisticated-attack-method data misses new fraud patterns

---

## Part 3: Finding Your Human Checkpoints

Now that you know the three failure types, the question is: **where do you put the human?**

Remember the D/P framework: Every workflow is a sequence of D and P steps. You can have D→D, D→P, P→D, P→P patterns.

**A checkpoint is a human decision point in that sequence.** It's where you say: "The AI did its work, but before we act on it, a human verifies/judges/approves."

The art is placing checkpoints where they'll catch errors *without* examining every output (which would be like doing the work yourself).

### Type 1: D→P Checkpoints (AI Makes Decision, Human Verifies)

**Pattern:** Deterministic input → AI generates probabilistic output → Human judges before action

**Example:**
- D: Extract keywords from a resume (deterministic)
- P: Decide if the candidate is a culture fit (probabilistic—requires judgment)
- Checkpoint: Human reviews the culture fit assessment before deciding to interview

**Why it works for hallucinations:** Hallucinations are seductive, but a human reader of the original + AI output can usually spot the divergence. You ask yourself: "Does the AI's summary match what I just read?" Most hallucinations fail this test.

**Where to place it:** Right after AI makes a judgment call, before you act on it.

**Cost:** You have to read/review the AI's judgment. But you don't have to do the original work (extract keywords, analyze resume, whatever). You're auditing, not executing.

**Risk it catches:** Hallucination failures (mostly), some misunderstanding failures (if the misunderstanding is obvious in the output).

### Type 2: P→D Checkpoints (Human Makes Decision, AI Executes)

**Pattern:** Human makes probabilistic judgment → AI executes deterministically on that judgment

**Example:**
- P: Decide what "engagement" means for your email campaign (human judges: is it clicks, or clicks-leading-to-purchase, or something else?)
- D: AI optimizes the email for that metric (deterministic)
- Checkpoint: Human defines the goal *before* AI optimizes

**Why it works for misunderstanding:** Misunderstandings happen when the AI interprets your spec differently. If the human makes the judgment call first (defining what you actually want), and then tells the AI to execute, the spec is clear. The AI can't misunderstand because there's nothing to misinterpret.

**Where to place it:** Before AI starts, at the specification/judgment stage.

**Cost:** You have to make the probabilistic judgment call upfront. But you're not reviewing every output. You're specifying the direction once.

**Risk it catches:** Misunderstanding failures (mostly), some hallucination failures (if the misunderstanding was causing the hallucination).

### Type 3: P→P Checkpoints (AI Makes Decision, Human Checks Reasonableness)

**Pattern:** AI makes a judgment → Human asks: "Is this reasonable?" and makes a final judgment

**Example:**
- P: AI predicts if a customer will churn (probabilistic)
- P: Human reviews the prediction and decides if it's reasonable
- Checkpoint: Human doesn't necessarily reverse-engineer the decision, but asks: "Does this feel right given what I know about the customer?"

**Why it works for drift:** Drift failures happen when the real-world context has shifted from training. A human who's embedded in the current context can often sense when the AI's prediction feels off. "Wait, that doesn't match what I'm seeing in the customer base right now."

**Where to place it:** After AI makes judgment, before you act. But lighter-weight than D→P checkpoints (you're not reviewing the full reasoning, just asking "does this pass the sniff test?").

**Cost:** You have to review AI judgments and apply your intuition. It's cognitively lighter than D→P review (you're not fact-checking), but it's still review.

**Risk it catches:** Drift failures (mostly), some misunderstanding failures (if the misunderstanding makes the output obviously wrong).

---

## Putting It Together

Now you have the framework:

- **Hallucinations** (seductive lies) → Catch with **D→P checkpoints** (human verifies)
- **Misunderstandings** (wrong specs) → Catch with **P→D checkpoints** (human judges first)
- **Drift** (context shifts) → Catch with **P→P checkpoints** (human sniff tests)

The next step is deciding *where* and *how* to place these checkpoints operationally. That's the follow-up article: confidence thresholds, case studies of failed placements, and an actual checklist you can use.

For now, the diagnostic work is done. **You know what can go wrong, and you know which type of checkpoint catches which type of failure.**

That's the foundation. The rest is execution.

---

## Read the Operational Guide

Article 6b drops in 3 days with the tactical framework: confidence thresholds as PM decisions, real case studies of failed checkpoints, UX design patterns, and an operational checklist you can actually use.
