---
title: "P Work Thresholds, Case Studies, and Your Implementation Checklist"
date: 2026-03-08
author: "Harsha Cheruku"
tags: ["AI", "product-management", "deterministic-probabilistic", "p-work", "confidence-thresholds", "operational"]
---

# P Work Thresholds, Case Studies, and Your Implementation Checklist

Three days ago, I shared the diagnostic framework: **hallucinations, misunderstandings, and drift** — the three types of P work failures, and which checkpoint types catch each one.

But diagnosis without treatment is useless.

This article is the operational part. It's about **setting confidence thresholds strategically** (they're PM decisions, not math problems), **learning from real failures**, and **actually implementing checkpoints** without turning them into bottlenecks.

---

## Part 1: Confidence Thresholds as PM Decisions

Here's the shift in thinking: **Confidence thresholds aren't ML engineer decisions. They're PM decisions.**

A confidence threshold is the point where you say: "If the AI is confident above X%, I act automatically. Below X%, I get human review."

**Example:** Your recommendation algorithm surfaces products. If it's 85%+ confident the user will buy, show the recommendation. If it's 60-85% confident, show it but mark it as "experimental." If it's <60% confident, don't show it.

### The Three-Number Framework

As a PM, you're making three decisions:

**Decision 1: Cost of False Positives**
- What does it cost if the AI is confident but wrong?
- Recommendation algorithm shows wrong product → customer wastes time (low cost, user just ignores it)
- Fraud detector flags legitimate transaction as fraud → customer can't buy, loses revenue (high cost)
- Resume screening filters out qualified candidates → lose hiring opportunity (medium-high cost)

**Decision 2: Cost of False Negatives**
- What does it cost if the AI is not confident and you skip the opportunity?
- Don't show recommendation → missed cross-sell opportunity (medium cost: lost revenue)
- Don't flag fraud → fraud happens (very high cost: financial loss + trust damage)
- Don't flag candidate for review → miss qualified hire (medium cost: lost hire)

**Decision 3: Cost of Human Review**
- What does it cost to have a human verify the AI?
- Recommendation review: takes 2 seconds per item, costs ~$0.01 in labor
- Fraud review: takes 30 seconds per item, costs ~$0.15 in labor
- Resume review: takes 3 minutes per item, costs ~$1.50 in labor

### Setting Your Threshold

Your threshold should balance these costs:

**If False Positives Are Cheap, Set Threshold Low**
- Example: Recommendation algorithm where a wrong recommendation just means the user ignores it
- Threshold: 60%. Let it run, show recommendations, prioritize coverage over precision

**If False Positives Are Expensive, Set Threshold High**
- Example: Fraud detection where false positives block customers
- Threshold: 95%. Only flag transactions you're very confident about, accept some fraud leaks to avoid blocking good transactions

**If Human Review Is Cheap, Lower the Threshold**
- Example: Your customer support team can review AI-generated responses in 30 seconds
- Threshold: 70%. Let AI generate more responses, review low-confidence ones, save a few seconds per review

**If Human Review Is Expensive, Raise the Threshold**
- Example: Your engineering team costs $300/hour and reviewing each AI decision takes 10 minutes
- Threshold: 90%. Let AI run with high autonomy, only escalate when truly uncertain, minimize interruption to expensive engineers

### The Key Insight: Thresholds Aren't Absolutes

Here's what most teams miss: **You adjust thresholds based on context, not based on math.**

A 70% confidence recommendation from your algorithm might be a perfect showstopper in one context (recommending high-risk financial products to new customers) and a green-light in another context (recommending low-cost add-ons to loyal customers).

Your job as PM is to say: "In this context, with these stakes, and this cost of human review, the threshold is X."

You're not running logistic regression on confidence scores. You're making a judgment call about acceptable risk.

---

## Part 2: When Checkpoint Placement Failed — Real Cases

Theory is useful. Examples are better. Let's look at real cases where checkpoints were placed wrong—and what happened.

### Case 1: ChatGPT Medical Advice (No D→P Checkpoint)

**What happened:**
- ChatGPT generated medical advice that was confidently wrong
- Users trusted it because it sounded authoritative
- Some followed the advice and were harmed

**Why the checkpoint failed:**
- OpenAI deployed the model with no D→P checkpoint
- No human doctor verified the medical outputs before they were shown to users
- The hallucinations were seductive: they sounded medical, used clinical language, had structure
- A human review (D→P checkpoint) would have caught most of them

**The lesson:**
When your AI is operating in high-stakes domains (medicine, law, finance), **you need a D→P checkpoint.** Someone has to verify the output before the user acts on it. The more seductive the hallucination, the more critical the checkpoint.

**Cost vs. Benefit:**
- Cost: A doctor reviewing every medical response (expensive, slows down the feature)
- Benefit: You don't give your users dangerous advice
- The right answer: You deploy with the checkpoint, or you don't deploy to the medical domain

### Case 2: Amazon Alexa's "Skill" Recommendations (No P→P Checkpoint)

**What happened:**
- Amazon recommended Alexa "skills" (mini-apps) to users based on user behavior patterns
- The algorithm was supposed to surface skills the user would find useful
- But it surfaced skills based on spurious correlations: if you played jazz music, it recommended a skill for checking sports scores (because some users who played jazz also checked scores)
- Users installed useless skills, engagement dropped, many users disabled skill recommendations

**Why the checkpoint failed:**
- No P→P checkpoint between algorithm decision and user exposure
- The AI made judgments (this user wants this skill) without human validation
- A human who understood the current user base could have sensed that the recommendations were off: "Wait, why is the algorithm recommending sports to jazz fans?"

**The lesson:**
For P→P decisions, you need a sniff test. Someone embedded in the domain needs to ask: "Does this feel right?" Not because the AI is broken, but because P decisions often drift from reality in subtle ways.

**The fix:**
Add a P→P checkpoint: Before recommending a skill to millions of users, have the PM team review top recommendations and ask: "Is this actually useful?" If not, retrain or adjust the algorithm.

### Case 3: Netflix Filter Bubbles (No P→D Checkpoint)

**What happened:**
- Netflix's algorithm optimized for "watch time"
- It surfaced shows users would watch for hours
- It did this so well that it created filter bubbles: users watching only their genre, only their culture, only their political perspective
- After months, some users felt the algorithm was limiting their exposure

**Why the checkpoint failed:**
- P→D checkpoint wasn't used to define the goal
- Netflix engineers and PMs said: "Optimize for watch-time"
- The AI did exactly that
- But the real goal was "optimize for long-term user satisfaction," which includes exposure diversity
- A human judgment call upfront (P→D checkpoint) saying "we want watch-time AND diversity" would have changed the optimization

**The lesson:**
For P→D checkpoints, the human has to make the judgment call *before* the AI runs. Not after. If you let the AI optimize without a clear, complete specification, the AI will find ways to hit the metric you gave it that you didn't intend.

**The fix:**
Add a P→D checkpoint: Before the algorithm launches, a PM decides what "success" really means. Not just "watch-time," but "watch-time weighted toward diverse content" or "watch-time + user satisfaction." Specify it in code. Don't let the AI guess.

### Case 4: Interview Scheduling System (Wrong Checkpoint Type)

**What happened:**
You implemented an AI system to schedule customer interviews based on calendar availability and timezone compatibility.
- The algorithm was technically correct (D work)
- But it placed P-level decisions (which customers to interview, in what order) on automatic
- After three weeks, you realized you'd been interviewing only from one customer segment (because the algorithm correlated calendar availability with company size)
- You'd missed interviews with small customers who'd been more flexible with timing

**Why the checkpoint failed:**
- This was a D→P situation masquerading as a P→P situation
- You placed a P→P checkpoint (human reviews scheduled interviews) when you should have placed a D→P checkpoint (human decides interview order before AI schedules)
- The sniff test (P→P) didn't catch the problem because scheduling decisions *looked* reasonable individually
- But the pattern (all large companies, no small ones) was invisible in individual reviews

**The lesson:**
Sometimes the checkpoint type matters more than the threshold. You can have a perfect P→P sniff test and still miss a systematic bias. If the decision is really P-level (the AI is making judgment calls about priority), use a D→P checkpoint. Make the human validate the decision before it's implemented, not after.

---

## Part 3: The UX of Uncertainty — Designing Checkpoints That Don't Slow You Down

Here's where most teams get it wrong: They place a checkpoint but design the UX terribly.

The AI makes a decision. The human reviews it. Then what?

### The Bad UX: Modal Override

**Bad approach:**
- AI recommends action X with confidence score 0.73
- Human sees the recommendation and must either "Approve" or "Override"
- If Human approves, action happens
- If Human overrides, action doesn't happen
- No room for nuance

**Why it sucks:**
- It's binary. But reality is ternary: "Yes, definitely do this," "Maybe, but with conditions," "No, don't do this"
- The human has to make a full decision, not just validate
- It's slow. The human has to actively approve every marginal decision
- It's exhausting. Humans get decision fatigue from reviewing every output

**Examples that fail with this UX:**
- Fraud detection: Every flagged transaction requires manual override approval. Your team spends all day approving fraud flags.
- Resume screening: Every resume below confidence threshold requires manual review. Your recruiting team is buried in marginal resumes.
- Content moderation: Every piece of content below confidence threshold requires human review. Your moderation team can't keep up.

### The Good UX: Tiered Actions

**Good approach:**
- AI makes recommendation with confidence score
- Threshold 1 (95%+ confidence): Auto-approve, no human in loop
- Threshold 2 (70-95% confidence): Queue for human review, but don't require approval—surface context and let human decide if they want to intervene
- Threshold 3 (<70% confidence): Don't surface to users, only show to PM for monitoring

**Why it works:**
- It's ternary: Yes, maybe, no—matching reality
- It's asynchronous: High-confidence decisions happen instantly. Marginal decisions get reviewed when someone has time.
- It's efficient: You're not reviewing every decision, only the marginal ones
- It has escape hatches: If a human disagrees with a high-confidence decision, they can override (though this surfaces an alert to your team: "Why is the human rejecting high-confidence decisions?")

**Example UX that works:**
- Recommendation algorithm: 90%+ confidence → show to user automatically. 70-90% → show to user but mark as "experimental." <70% → don't show.
- Resume screening: 85%+ confidence → auto-pass to next round. 60-85% → queue for recruiter review when they have time. <60% → archive, only surface if recruiter specifically digs.
- Fraud detection: 95%+ confidence → auto-flag transaction. 80-95% → queue for review, but don't block transaction (let it proceed while human reviews). <80% → monitor, don't flag or block.

### The Best UX: Contextual Thresholds

**Best approach:** Adjust thresholds based on context, not global rules.

**Examples:**
- Recommendation algorithm: For high-value customers, 85%+ confidence. For new customers, 75%+ confidence (you're willing to take more risk with them since you don't have much to lose).
- Resume screening: For in-demand roles, 70%+ confidence (you need candidates). For common roles, 80%+ confidence (you have plenty of candidates).
- Fraud detection: For small transactions, 90%+ confidence (low risk). For large transactions, 95%+ confidence (high risk).

**Why it works:**
- You're not using a one-size-fits-all threshold
- You're matching the threshold to the actual risk/reward in that context
- You're giving yourself flexibility to adjust without retraining the model

---

## Part 4: Your Implementation Checklist

Let's get tactical. You're starting a new P work project. The AI is going to make judgments that affect your users. Here's the checklist.

### Phase 1: Identify the Failure Modes (Pre-Launch)

**Question 1: What can go wrong?**
- Hallucination: Can the AI confidently generate plausible-sounding but wrong information?
- Misunderstanding: Can I specify what I want clearly enough? Are there hidden assumptions in my specification?
- Drift: Is the real-world context different from what the AI was trained on? Will it change during deployment?

**Question 2: What's the cost of each failure type?**
- Hallucination → costs X (wasted time, revenue loss, trust damage, legal liability?)
- Misunderstanding → costs Y
- Drift → costs Z

**Action:** List them. Explicitly. Don't assume they won't happen.

### Phase 2: Choose Checkpoint Types (Pre-Launch)

Based on failure costs, decide:

**For hallucination risks:** Use D→P checkpoint
- Human verifies AI output before it reaches users
- Cost: Slow (requires review)
- Benefit: Catches seductive lies

**For misunderstanding risks:** Use P→D checkpoint
- Human makes the specification before AI executes
- Cost: You make judgments upfront
- Benefit: Avoids divergence between intent and execution

**For drift risks:** Use P→P checkpoint
- Human reviews AI judgments for reasonableness
- Cost: Medium (requires sampling, not 100% review)
- Benefit: Catches context shifts

### Phase 3: Set Thresholds (Pre-Launch)

**For each checkpoint, decide:**
1. What's my false positive cost? What's my false negative cost?
2. What's my human review cost?
3. Based on those three numbers, what confidence threshold makes sense?

**Action:** Write it down. "For resume screening, threshold is 75%. Anything below 75% gets reviewed by a human. Anything above 75% goes to interviews."

### Phase 4: Design the UX (Pre-Launch)

**For each checkpoint, decide:**
1. Is this binary (yes/no) or ternary (yes/maybe/no)?
2. Who reviews? When? How do they surface decisions?
3. What happens if the human disagrees with the AI?

**Action:** Wireframe it or describe it. Don't let this be an afterthought.

### Phase 5: Monitor (Post-Launch)

**Monitor three things:**

1. **False Positive Rate:** How often is the AI wrong when it's confident?
   - Track this per confidence bucket (for 90%+ confidence decisions, how often is the AI actually right?)
   - If false positive rate is higher than expected, lower your threshold

2. **Human Override Rate:** How often do humans disagree with the AI?
   - If humans are overriding high-confidence decisions frequently, something's wrong (data shifted, AI broke, misalignment, etc.)
   - If humans are overriding <5% of low-confidence decisions, threshold is about right

3. **Downstream Impact:** Is the P work actually having the effect you intended?
   - Are users happy? Is revenue growing? Is churn decreasing? Are you seeing signs of drift?
   - Monitor the metric you *actually* care about, not the metric the AI is optimizing for

### Phase 6: Iterate (Ongoing)

Based on monitoring, adjust:
- **If false positives are high:** Lower threshold, add checkpoints, retrain the model
- **If false negatives are high:** Raise threshold, reduce checkpoints, review specification
- **If downstream impact is bad:** You probably have a P→D misunderstanding. Check your specification. Is the AI doing what you asked, or what you *wanted*?

---

## Part 5: The Bigger Picture — P Work as a System

Here's what you're really doing when you place checkpoints and set thresholds: **You're treating P work like a high-risk system.**

Because it is.

In manufacturing, high-risk systems have multiple levels of checkpoints. A plane has redundant systems. A nuclear plant has multiple safety barriers. A hospital has protocols, peer review, escalation paths.

Your P work should have these too.

**The checkpoint isn't a bottleneck. It's a safety mechanism.** It's there because P work errors compound, and you need to catch them early.

The human in the checkpoint isn't a rubber stamp. They're not approving everything the AI does. They're a sniff test. An error detector. A force that says: "Wait, does this actually make sense in this context?"

### The Anti-Burnout Message

Here's the thing: **Burnout happens when you feel responsible for errors you can't detect.**

If you're doing D work, errors are visible. The test fails. The query returns wrong data. You know something's wrong immediately.

But P work errors are invisible. You make decisions in darkness. You're responsible for outcomes you can't fully predict. That's what causes burnout.

**Checkpoints don't prevent P work—they prevent burnout.**

By placing checkpoints strategically, you're not adding work. You're *distributing* responsibility. You're saying: "I'm going to make judgment calls about what the AI should do, and what the output should be reviewed for. But I'm not going to review every single output. I'm not going to second-guess the AI on everything. I'm going to be smart about where the human judgment matters most."

That's not avoidance. That's systems thinking.

---

## Your One-Page Checklist

Print this. Fill it out before you ship P work. Don't skip it.

```
P WORK CHECKLIST

Project: [name]
Failure Type | Risk | Checkpoint Type | Threshold | Monitor
---|---|---|---|---
[Hallucination/Misunderstanding/Drift] | [Low/Medium/High] | [D→P/P→D/P→P] | [60%/70%/80%+] | [False positive rate / Override rate / Downstream metric]
[...] | [...] | [...] | [...] | [...]

Approval: Who reviews? How often? What happens if they disagree?

UX Design: [Binary or ternary? How do we surface decisions?]

Launch Plan: [What's success look like? How will we know if the system is working?]

Rollback Plan: [If this goes wrong, what's our emergency exit?]

Post-Launch Monitoring:
- Week 1-2: [Monitor this specific metric]
- Week 2-4: [Check this]
- Month 2+: [Look for drift]
```

---

## Next Steps

The D/P Framework is now complete for the "execute P work" arc.

You understand:
1. **Why P work is dangerous** (errors compound, feedback is invisible)
2. **The three failure types** (hallucination, misunderstanding, drift)
3. **Where to place checkpoints** (D→P, P→D, P→P)
4. **How to set thresholds** (balance costs, adjust for context)
5. **How to design UX** (ternary, asynchronous, contextual)
6. **How to implement and monitor** (the six-phase checklist)

The next article in the series will zoom out: **Building Teams for P Work.** How do you hire, structure, and manage people when judgment is the bottleneck?

But first, implement this checklist. Use it on your next P work project. See what breaks. See what works. Let the framework inform your decisions, not replace them.

You know what to do. Now do it.
