---
title: "When P Goes Wrong: Case Studies of Catastrophic Probabilistic Failures"
date: 2026-04-07
author: "Harsha Cheruku"
tags: ["AI", "product-management", "deterministic-probabilistic", "p-work", "risk-management", "case-studies", "failure"]
excerpt: "P work failures aren't like bugs. They're like slow leaks — coherent, confident, and compounding until something breaks at scale. Five case studies of what catastrophic probabilistic failure actually looks like, and what was missed."
---

# When P Goes Wrong: Case Studies of Catastrophic Probabilistic Failures

In 2018, Amazon reportedly scrapped an internal recruiting model after discovering it downgraded resumes containing signals associated with women. The model wasn't “glitching.” It wasn't throwing stack traces. It was doing exactly what it had been trained to do: optimize against historical hiring patterns.

That’s the whole danger.

The system looked coherent. The outputs looked plausible. Humans approved recommendations because the recommendations *looked like hiring logic* — until somebody looked closer and saw what the model had actually learned.

That is the shape of catastrophic P failure.

Not dramatic. Not noisy. Not immediate.

Accumulating.

**P failures don’t announce themselves. They accumulate.**

---

## 1) Why P Failures Are Different From D Failures

D failures are usually visible and bounded.

- API returns `500`
- deployment fails health checks
- ETL job dies
- test suite fails

You get a signal, a blast radius, and a rollback path.

P failures are different:

- the system runs
- outputs look valid
- humans keep approving
- damage compounds in the background

The model is “correct” against its optimization target. The target is wrong, incomplete, or misaligned to real-world goals.

### A) The anatomy of a P failure

Most catastrophic P failures share the same four-step sequence:

```text
1. Hidden assumption enters system design
2. System scales that assumption consistently
3. Human reviewers normalize output as “reasonable”
4. Harm becomes visible only after compounding
```

### B) Why they’re often discovered late

Because nothing “breaks.”

P failures hide behind success-shaped dashboards:

- conversion improves
- throughput improves
- latency drops
- approval rates stabilize

If your measurement system only tracks near-term surface metrics, you'll miss the damage curve until it's expensive.

---

## 2) Case Study 1: Amazon’s Recruiting Model (2018)

The reporting is now familiar:

- model trained on historical hiring data
- historical data reflected male-dominant technical hiring patterns
- model learned proxies that penalized women-associated resume signals
- tool was eventually scrapped

### A) What failed in P terms

The failure wasn’t “AI bias” as an abstract concept. It was a concrete P decision:

> “Historical outcomes are a reasonable training signal for future hiring quality.”

That assumption was never robustly challenged with structural fairness checkpoints.

### B) Checkpoint that was missing

A periodic distributional audit by demographic segment should have been standard.

Not one-time governance theater. Recurring operational checkpoint.

| Checkpoint | Present? | Why it mattered |
|---|---:|---|
| Training data representativeness audit | Partial | Would surface historical skew |
| Output parity monitoring | Weak | Would detect downstream discrimination patterns |
| Human override analysis | Unknown | Would show whether reviewers were correcting model bias |
| Periodic fairness review cadence | Missing/insufficient | Would catch drift/embedding over time |

### C) Recovery pattern

They dropped the system. That is operationally clean. Ethically, not clean.

People filtered out by the tool are mostly invisible in the record.

That’s another P pattern: the harmed population is often hard to reconstruct after the fact.

---

## 3) Case Study 2: Recommendation Rabbit Holes (Netflix-Style Pattern)

Across recommendation systems, a common optimization objective is engagement duration: watch time, session length, return frequency.

Reasonable objective. In isolation.

But optimizing for session depth often discovers emotionally activating content gradients faster than humans expect.

### A) The P failure

Not “the model is inaccurate.”

The failure is institutional framing:

> “If watch time rises, user value rises proportionally.”

That is often false beyond some threshold.

A user can spend more time and have a worse content diet.

### B) The missing checkpoint

Most teams instrument top-line engagement aggressively, but under-instrument trajectory quality.

What was often missing historically across recommender deployments:

- diversity trajectory over session depth
- extremity progression over repeated sessions
- regret / post-session dissatisfaction proxies
- long-horizon trust metrics

### C) The second-order lesson

This is a misunderstanding failure at scale (Article 5 territory):

- metric optimized correctly
- metric semantically incomplete
- system “wins” the local objective while degrading global objective

The model did what it was asked.

Leadership asked the wrong thing.

---

## 4) Case Study 3: A/B Success, Strategic Failure

Every product team has a version of this story.

- run test on onboarding flow
- boost activation by +6%
- ship confidently
- six months later retention curve sags
- team spends quarter “fixing churn” caused by the activation hack

### A) Why this keeps happening

Because teams quietly substitute proxy wins for goal wins.

They claim to test a long-horizon hypothesis but instrument only short-horizon behavior.

| Claimed goal | Actually measured | Hidden risk |
|---|---|---|
| Better user fit | Trial starts | Inflated low-intent signups |
| Better product value | Daily opens | Habit loop without utility |
| Better retention | Week-1 activation | Long-term trust erosion |

### B) Checkpoint that wasn’t there

Pre-test causal chain review.

Before test launch, require explicit mapping:

```text
Feature change -> behavioral change -> intermediate metric -> long-term business/user outcome
```

If that chain is hand-wavy, your “win” is probably fragile.

### C) Why this is catastrophic in slow motion

Local experiments stack.

Ten short-term optimizations can produce a strategically incoherent product, while each individual experiment still “won.”

---

## 5) Case Study 4: IBM Watson for Oncology (Deployment Generalization Failure)

IBM Watson for Oncology became a cautionary case in clinical AI deployment.

Widely reported concerns included:

- narrow training/curation context
- recommendations that did not generalize reliably across institutions/populations
- low trust and reduced adoption in practice

(Primary reporting included STAT investigations; subsequent commentary in medical circles reinforced generalization concerns.)

### A) P failure class: drift/distribution mismatch

The system could be coherent inside the context it learned.

Then fail outside that context while still sounding precise and confident.

That confidence is what makes this class dangerous in medicine.

### B) Checkpoint that should have been mandatory

External cohort validation before broad deployment.

Not “works at home institution.”

Works across:

- different patient populations
- different practice patterns
- different resource environments

### C) Domain-specific point

In clinical contexts, specificity language creates authority.

A wrong but specific recommendation can outperform a cautious human in persuasion power — exactly when it should not.

---

## 6) Case Study 5: Composite Enterprise Pricing Failure

A large retailer deploys a pricing recommendation engine to improve margin performance.

- model ingests historical sales, elasticity estimates, promo history
- recommendations look mathematically elegant
- teams approve because suggestions are “data-driven”
- within two quarters: margin erosion in specific categories, inventory distortion, supplier friction

### A) What actually happened

Model assumptions about elasticity remained stable while customer behavior shifted.

The system kept optimizing against stale relationships.

Humans trusted the precision veneer.

### B) Why it slipped through

- no category-level drift checkpoint with escalation threshold
- no enforced challenger model for high-impact recommendations
- no mandatory merchant override review on outlier deltas

### C) Common human trap

Teams close to the system get habituated to its language.

The model’s recommendations feel normal because the team has internalized its assumptions.

Familiarity can hide failure.

---

## 7) The Pattern Across All Five

Different domains. Same skeleton.

1. **System operated correctly against declared objective**
2. **Declared objective/assumptions were flawed**
3. **Failure remained invisible until scale exposed it**
4. **Missing checkpoint would have been operationally feasible**

That fourth point matters.

Most of these were not unsolvable technical mysteries.

They were governance and design misses:

- not resourcing audits
- not defining guardrail metrics
- not instrumenting long-horizon signals
- not revisiting assumptions on cadence

### A) The uncomfortable truth

Most organizations would not have caught these early either.

Not because teams are incompetent.

Because modern operating systems reward measurable throughput, while assumption auditing is slower, less visible, and politically harder.

---

## 8) How to Recover When P Goes Wrong

Unlike D incidents, P incidents rarely have a clean rollback.

You need a different playbook.

### A) Triage in two tracks

**Track 1: immediate containment**
- pause high-risk automated decisions
- narrow scope (segment, geography, use case)
- force high-friction human review for exposed paths

**Track 2: systemic diagnosis**
- identify failure class (hallucination, misunderstanding, drift)
- reconstruct assumption chain
- quantify affected population window

### B) Incident communication standard

“Model error occurred” is not enough.

Minimum credible disclosure internally (and externally where needed):

1. Which assumption failed?
2. How long was system operating under it?
3. Which populations were affected?
4. What corrective checkpoint is now in place?

### C) Fix checkpoint, not just output

If you only patch outputs, failure recurs.

You need to install the missing detector:

```text
Assumption register -> periodic audit -> anomaly trigger -> escalation owner -> stop/adjust decision
```

### D) Five-question response checklist

When a P failure surfaces, ask:

1. What exactly was optimized?
2. Which assumption made that optimization “valid”?
3. When did that assumption stop being true?
4. Which checkpoint should have detected the change?
5. What process change prevents repetition at similar scale?

---

## 9) Final Take

P failures are inevitable.

If you remove all P risk, you remove P value. No serious organization can operate that way.

So the objective isn’t “never fail.”

The objective is:

- fail with shorter detection latency
- fail with constrained blast radius
- fail once per class, not repeatedly

The teams that get this right don’t have magical models.

They have better checkpoints.

---

*Part of the D/P Framework series. Previous: [The Economics of P: Who Gets Paid What When D Gets Cheaper?](/blog/the-economics-of-p). Next: [The Ethics of the Human Checkpoint: Who's Responsible When AI Fails?](/blog/ethics-of-the-human-checkpoint).*  
*Building in public at [fullstackpm.tech](https://fullstackpm.tech). Follow along on [X @fullstackpmtech](https://x.com/fullstackpmtech).*