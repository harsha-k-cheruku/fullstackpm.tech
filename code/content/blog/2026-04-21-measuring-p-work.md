---
title: "Measuring P Work: How Do You Know If Someone Is Good at Probabilistic Thinking?"
date: 2026-04-21
author: "Harsha Cheruku"
tags: ["AI", "product-management", "deterministic-probabilistic", "p-work", "performance-management", "calibration", "metrics"]
excerpt: "You can't measure P work with throughput metrics. Decision quality is hard to observe, slow to validate, and easy to confuse with confidence. Here's what actually works."
---

# Measuring P Work: How Do You Know If Someone Is Good at Probabilistic Thinking?

Performance review season. Two senior PMs.

PM A shipped 8 features, won 5 experiments, has beautiful dashboards.

PM B shipped 3 features, had mixed experiment outcomes, and spent a quarter stopping the org from shipping a strategically expensive mistake.

Who performed better?

Most organizations still answer with D-shaped metrics. More shipped work, more visible wins, more throughput.

That breaks when judgment becomes the bottleneck.

As we covered in [Building Teams for P Work](/blog/building-teams-for-p-work) and [Organizational Structures for P Dominance](/blog/organizational-structures-for-p-dominance), the value in P-heavy environments is not just output. It’s decision quality under uncertainty.

The problem: decision quality is harder to observe, slower to validate, and easier to fake with confidence theater.

So you need a different measurement stack.

---

## 1) Why Output Metrics Fail for P Work

Output metrics still matter. They just don’t capture what matters most in P-heavy roles.

### A) The timing problem

Many P decisions resolve slowly.

A strategic call made in Q1 may not reveal quality until Q3/Q4, if ever.

### B) The attribution problem

Great P work often prevents bad outcomes.

How do you score:

- “didn’t enter doomed market”
- “avoided retention cliff”
- “killed feature before reputational damage”

Nothing shipped. Value still real.

### C) The confidence illusion problem

At decision time, these can look identical:

- calibrated uncertain decision that is high quality
- overconfident weak decision packaged well

By the time outcomes resolve, promotion cycles often already moved.

### D) Why D metrics mislead in P contexts

| D metric | Why teams love it | Why it fails for P quality |
|---|---|---|
| Features shipped | easy to count | rewards activity, not judgment quality |
| Velocity/story points | operationally convenient | detached from decision framing quality |
| Number of experiments | signals learning posture | can reward low-information experiment spam |
| DAU/CTR lift snapshots | fast feedback | proxy can diverge from strategic objective |

This is exactly how you get organizations that look productive and make systematically weak bets.

---

## 2) Calibration: The Core Skill Most Orgs Ignore

Calibration is simple to define and hard to do well.

> If you claim 80% confidence repeatedly, you should be right about 80% of the time over a large enough set.

Most people are not well calibrated. Especially under status pressure.

### A) Why calibration beats charisma

A PM who says “90% confident” and lands at 60% hit rate is dangerous.

A PM who says “60% confident” and lands at 60% hit rate is trustworthy.

In P work, trustworthy uncertainty is more valuable than polished certainty.

### B) Tetlock’s lesson (practical reading)

Superforecasting research highlights a pattern:

Top forecasters are not always the loudest or most credentialed. They are often:

- better at probability estimates
- faster at updating beliefs
- less ego-attached to prior views

That maps directly to high-quality product judgment.

### C) Calibration is measurable

You don’t need complex infrastructure.

You need discipline:

1. record prediction
2. attach confidence level
3. revisit outcome
4. compute hit rate by confidence band

No record, no learning.

---

## 3) Leading vs Lagging Signals of P Quality

The trick is not abandoning outcomes. It’s combining slow outcome signals with faster process signals.

### A) Lagging (slow, noisy, still important)

- initiative success/failure
- long-term retention impact
- strategic bet ROI

Good for eventual truth, bad for real-time coaching.

### B) Leading (faster, process-grounded)

- framing clarity before execution
- assumptions explicitness
- confidence declaration quality
- pre-committed kill criteria
- update behavior when evidence shifts

### C) Poker analogy (because it works)

In poker, you can make a correct decision and lose the hand.

Outcome ≠ immediate proof of decision quality.

Same in product:

- good bet can lose
- bad bet can win temporarily

You need to evaluate process quality and outcome quality separately, then reconcile over time.

---

## 4) A Practical Rubric for P Work

Use this 4-dimension rubric quarterly for senior ICs/managers doing high-P work.

Score each 1–4.

### A) Framing quality

| Score | Behavior |
|---:|---|
| 1 | jumps to solutions, no explicit frame |
| 2 | problem stated, assumptions mostly implicit |
| 3 | clear frame, assumptions explicit, constraints named |
| 4 | includes second-order effects and mind-change triggers |

### B) Confidence calibration

| Score | Behavior |
|---:|---|
| 1 | consistently high confidence, rarely updates |
| 2 | uncertainty acknowledged inconsistently |
| 3 | confidence reasonably calibrated, updates with evidence |
| 4 | tracks predictions over time and audits calibration quality |

### C) Risk literacy

| Score | Behavior |
|---:|---|
| 1 | treats all bets similarly |
| 2 | distinguishes scale but not reversibility |
| 3 | names blast radius + reversibility explicitly |
| 4 | structures bets to cap irreversible downside proactively |

### D) Learning loop discipline

| Score | Behavior |
|---:|---|
| 1 | ships and moves on, no pre-defined criteria |
| 2 | criteria defined post-hoc |
| 3 | success criteria + review date set up front |
| 4 | pre-committed kill criteria + retrospective loop into next bets |

### E) How to use rubric without becoming bureaucratic

- run quarterly, not weekly
- require examples for each score
- tie scores to coaching plans, not punishment templates

Weaponized rubric = people game language.

Coaching rubric = people improve thinking quality.

---

## 5) Embedding This in Performance Management

If the rubric lives in a Notion page nobody uses, congrats, you built decorative process.

Make it operational.

### A) Decision journal as artifact

For major bets, capture:

```text
Decision:
Expected outcome:
Confidence (%):
Key assumptions:
What changes our mind:
Kill criteria:
Review date:
```

This creates auditability for judgment quality.

### B) Quarterly calibration retros

Ask:

- where were we overconfident?
- where were we underconfident?
- did updates happen fast enough?

### C) Performance write-up language shift

Managers should explicitly describe P contribution:

- avoided high-cost strategic error
- improved framing quality across team
- shortened assumption invalidation latency
- improved calibration over time

If you only write “shipped X,” you erase P value by default.

### D) Guardrail: do not turn this into HR weaponry

The moment people think this rubric is “a better way to build a case against me,” honesty collapses.

Use for growth first, comp/promo context second.

---

## 6) Org-Level P Metrics (Beyond Individual Reviews)

As argued in [The Economics of P](/blog/the-economics-of-p), org competitiveness in AI-heavy environments depends on judgment quality at scale.

So measure it at system level.

### A) Core metrics

Reuse and extend prior series metrics:

1. **Decision-to-signal time**
2. **Assumption invalidation latency**
3. **Pivot lag**
4. **Checkpoint compliance rate**
5. **Calibration accuracy rate** (new emphasis)

### B) Calibration accuracy rate (definition)

For all major bets with declared confidence in period:

- group by confidence band (e.g., 50–60, 60–70, etc.)
- compare predicted vs realized hit rates

If your 80% confidence band lands around 55%, you have systemic overconfidence.

That is fixable only if measured.

### C) Why most orgs don’t know this

Because they don’t record predictions.

No prediction log -> no calibration baseline -> no learning loop.

Then leadership mistakes confidence tone for decision quality.

---

## 7) Start Small: Minimum Viable P Measurement

If you implement one practice, do this for every major bet:

```text
Before execution:
1) What do we expect to happen?
2) Confidence level (%):
3) What would change our mind?
4) Kill criteria:
5) Review date:

At 90 days:
- compare predicted vs actual
- log calibration lesson
```

That single loop will outperform most dashboard-heavy “strategic governance” programs because it forces pre-commitment and post-hoc honesty.

---

## 8) What Good Looks Like in 12 Months

If this system is working, you should see:

- less decision theater in reviews
- clearer framing in roadmap debates
- faster invalidation of weak assumptions
- better confidence hygiene (fewer fake-precision claims)
- promotion write-ups that recognize judgment work explicitly

What you should *not* expect:

- immediate perfect calibration
- zero bad bets
- clean attribution in every case

P work remains probabilistic. Better measurement reduces error; it does not abolish uncertainty.

---

## Final Take

You can’t improve what you refuse to instrument.

In D-heavy environments, throughput metrics were enough.

In P-heavy environments, they are necessary but insufficient.

The best P workers are not the most certain people in the room.

They’re the people who:

- frame better
- calibrate honestly
- update faster
- and leave a decision trail rigorous enough to learn from

If your performance system can’t see that, it will reliably reward the wrong people.

---

*Part of the D/P Framework series. Previous: [The Ethics of the Human Checkpoint: Who's Responsible When AI Fails?](/blog/ethics-of-the-human-checkpoint). Next: [The Fate of D Work: What Happens to Everyone Doing Deterministic Tasks?](/blog/the-fate-of-d-work).*  
*Building in public at [fullstackpm.tech](https://fullstackpm.tech). Follow along on [X @fullstackpmtech](https://x.com/fullstackpmtech).*