---
title: "The Economics of P: Who Gets Paid What When D Gets Cheaper?"
date: 2026-03-31
author: "Harsha Cheruku"
tags: ["AI", "economics", "future-of-work", "product-management", "deterministic-probabilistic", "labor-market", "career"]
excerpt: "When AI automates the deterministic layer, the market for D skills reprices fast. What's less obvious is what happens to P — why the premium is real, why it has a ceiling D never had, and what the labor market looks like when both are true."
---

# The Economics of P: Who Gets Paid What When D Gets Cheaper?

D work has a price problem.

Not a supply problem. A price problem.

There's no shortage of people who can write code, analyze data, draft documents, synthesize research, build presentations. There never was. The bottleneck was always speed — how fast one person could execute the work.

AI just eliminated that bottleneck.

When a tool can draft the report faster than you can open a new document, the market for "person who can draft reports" shifts. Not immediately. Not cleanly. But inevitably, the way any market shifts when supply goes vertical and demand stays flat.

This is the economic story of the D/P transition. And most people are thinking about it wrong — focusing on whether AI will "replace" them, when the more interesting question is: **what happens to the price of the work you do?**

---

## 1) The D Labor Market Is Being Repriced in Real Time

Automation doesn't eliminate jobs all at once. It reprices them.

The historical pattern: when a category of work gets automated or commoditized, wages for that work first compress, then bifurcate.

They compress because supply explodes (now anyone can produce the output) while demand for the manual version stays flat or falls.

Then they bifurcate. A small group of workers whose skills are adjacent to or enhanced by the automation get more valuable — they're the ones who can direct the automated systems, catch its errors, and do the work the systems can't. Everyone else gets further commoditized.

We saw this with desktop publishing in the 1990s. Before Photoshop, graphic design was a specialized craft with high barriers to entry. After: the number of people who could produce professional-looking work exploded, wages for routine design work compressed, and the designers who thrived were the ones who could do what the software couldn't — creative direction, brand strategy, complex visual systems.

We're in the same inflection now. AI isn't eliminating D work. It's expanding access to D output so dramatically that the wage premium for D execution is collapsing.

What does that look like in practice?

- Junior data analyst roles that existed to pull metrics are being replaced by dashboards any PM can operate
- Entry-level content roles that existed to produce drafts are being replaced by AI that produces better first drafts faster
- Junior engineering tasks — boilerplate, documentation, test cases — are increasingly AI-generated, with humans reviewing rather than creating
- Paralegal research, contract drafting, first-pass legal review — all undergoing the same compression

This doesn't mean these roles disappear tomorrow. It means the market is repricing them. Slowly in stable industries, fast in competitive ones.

---

## 2) The P Work Premium: Why It's Real

As D wages compress, P wages diverge. This is the good news for people who are building genuine judgment skills.

The logic is simple: **P work is the thing AI can't reliably automate, and demand for it is growing.**

Here's why it's hard to automate P work:
- P work requires integrating context that isn't in the prompt
- P work requires knowing when you don't know — calibrated uncertainty rather than confident output
- P work carries responsibility — someone has to own the decision, and AI doesn't own consequences
- P work adapts to novel situations that weren't in the training distribution
- P work involves value judgment: not just "what's the answer" but "what should we optimize for"

None of those are impossible to automate in principle. Some of them will be automated eventually. But they're hard, and in the meantime, the humans who can do them consistently and well are scarce relative to demand.

The demand side is also growing because AI adoption creates P demand:
- Every AI deployment needs humans to specify what it should optimize for (P→D pattern)
- Every AI output in a high-stakes domain needs humans to verify it (D→P checkpoint)
- Every AI system in production needs humans to monitor whether it's drifting (P→P pattern)

More AI in the org = more judgment work required to deploy and manage it responsibly. The P premium isn't just about doing what AI can't — it's about being the human-in-the-loop that AI requires to function in the real world.

What this looks like in compensation:
- Senior PMs who can define AI product strategy and manage probabilistic outcomes are commanding higher salaries than equivalents five years ago
- "AI product manager" roles that didn't exist three years ago are paying 20-40% above equivalent non-AI PM roles
- Researchers and designers who specialize in evaluating AI outputs — AI red-teaming, alignment research, model evaluation — are seeing dramatic wage growth from a small base
- Senior engineers who can architect AI systems and define evaluation frameworks are significantly out-earning peers doing primarily D implementation

The P premium is real. It's visible in the labor data if you know where to look.

---

## 3) But P Has a Ceiling D Never Had

Here's where the economics get uncomfortable for people expecting P skills to be the new safe harbor.

D work scales.

A senior engineer who's great at building distributed systems can produce 10x the output of a mediocre engineer through better architecture choices, cleaner code, faster debugging. More importantly, their output can be productized and multiplied. They build the system once; it runs for years, serving millions of users.

P work doesn't scale the same way.

A senior PM who's exceptionally good at judgment can make better decisions — but they can only make so many decisions. Judgment is time-constrained, attention-constrained, and context-constrained. You can't run a judgment parallel pipeline the way you can run multiple code processes.

This has three economic implications:

### A) P work is fundamentally labor-constrained at the individual level

A great D engineer can leverage their skills through automation: build systems that multiply their output. A great P thinker is mostly limited by their own cognitive capacity. They can improve their decision speed and quality, but the underlying constraint — hours, attention, context — doesn't compress the same way.

### B) P wages hit an organizational ceiling

Because P work requires direct human judgment, organizations can't infinitely substitute capital for labor. There's a real limit to how much an organization will pay for judgment before it tries to reduce the judgment required — by building better rules, better processes, or eventually better AI.

This is already happening. The first wave of AI products is dedicated to systematizing P decisions that cost too much: AI underwriting models that replace human loan officers, AI triage systems that replace human intake decisions, AI pricing engines that replace revenue management teams.

As P gets more expensive, the pressure to systematize it increases. The best defense for P workers isn't to be indispensable as individuals. It's to keep moving to the P work that's genuinely novel and hard to systematize.

### C) P work will eventually face its own automation wave

The uncomfortable long arc: P will be automated. Not now, not soon for the hardest cases, but directionally.

The trajectory of AI capability is toward handling increasingly complex P tasks. Today it struggles with genuine strategic judgment. In five years, it will be better. In ten, better still. The timeline is uncertain. The direction isn't.

The people who understand this aren't panicking. They're accepting the reality that P skills have a longer runway than D skills, but not an infinite one. The advantage is the head start, not permanent immunity.

---

## 4) The New Job Categories in the P Layer

When D work gets automated, some people move up to P work. Others move sideways into the P infrastructure — the layer of work that makes AI deployments safe, accurate, and governable.

These roles are new enough that they don't have stable names yet. But they're emerging fast:

### AI Orchestrators

People who design and manage the multi-step AI workflows that execute complex processes. They're not AI engineers (they often can't train models). They're workflow architects: defining which steps are D (can be automated) and which are P (need human judgment), designing the handoff points, and managing the quality of the overall output.

These roles are currently being filled awkwardly by senior PMs, operations leaders, and occasionally engineers who discovered they liked product problems. They'll become their own job category within a few years.

### Checkpoint Designers

Specialists in deciding where human oversight should live in an AI-assisted process. This requires simultaneously understanding how the AI fails (hallucination, misunderstanding, drift) and how humans can most efficiently catch those failures without reviewing every output.

Right now this work is done poorly by almost everyone. Checkpoint placement is usually ad-hoc, underdocumented, and reverted under time pressure. The organizations that develop this as a genuine discipline will have significantly lower AI incident rates than their peers.

### Model Evaluators and P Work Auditors

People who assess whether AI outputs — especially in high-stakes P domains like medical, legal, financial — are meeting quality standards. This is upstream of deployment: red-teaming models, finding failure modes, stress-testing edge cases.

Distinct from traditional QA. The failures are subtle, not binary. You can't write a unit test for "gives a recommendation that sounds right but reverses the legal liability." You need domain expertise, adversarial creativity, and patient systematic investigation.

### Decision Designers

A combination of product, UX, and behavioral science applied to the interface between humans and AI-generated P outputs. When AI makes a recommendation, how does the human receive it? What information does the human need to verify, accept, or override it? How do you prevent automation bias (humans accepting bad AI recommendations because the AI is usually right) without adding so much friction that the human review becomes a rubber stamp?

This is a real specialization that's currently being practiced poorly by everyone building AI products. The organizations that develop genuine decision design expertise will have both better products and lower liability exposure.

---

## 5) What Happens to Great D Workers

Let's be honest about the group most affected by this transition: people who built their careers and identities on excellent D execution.

These are not bad workers. They may be exceptional workers. But excellent execution of work that AI now does comparably or better is a credential that's depreciating.

The paths forward are real but uneven:

### Path 1: Move Up — Become a P Worker

The most direct route. Use domain expertise from D work to develop genuine P skills in the same domain.

A great data analyst who understands the business deeply isn't just a query writer anymore — they're a signal interpreter. They know what the data means, which questions are worth asking, how to frame the analysis so it produces actionable insight rather than informative noise.

The transition is not automatic. Domain expertise is necessary but not sufficient. The additional skills — framing ambiguity, calibrated confidence, decision under uncertainty — don't develop on their own. They have to be deliberately practiced.

And not everyone wants to do P work. P work is more ambiguous, less validateable in the short term, and more cognitively demanding. Some excellent D workers know themselves well enough to know that concentrated P work would make them miserable. That's legitimate, and it should inform their career choices.

### Path 2: Move Sideways — Become AI Infrastructure

The second route is to stay close to D work — but in the layer that makes AI D work reliable.

AI needs training data. AI needs evaluation. AI needs fine-tuning for domain-specific applications. AI needs human oversight on its most consequential D outputs. None of that work goes away when AI automates D execution — some of it grows.

The challenge: this work is often less visible, less prestigious, and less financially rewarded than traditional D execution. Data labeling, model evaluation, and quality assurance for AI outputs are essential and often undervalued. This gap will close as AI incidents become more expensive and organizations realize the cost of poor oversight, but the equilibrium hasn't arrived yet.

### Path 3: Specialize in What AI Can't Do

Not all D work is easily automated. AI is better at D work that is textual, pattern-based, and operates on well-defined inputs. D work that requires physical embodiment, real-world sensing, or deeply tacit expertise (the kind that's hard to articulate and therefore hard to train on) is more durable.

A skilled electrician's D work isn't being replaced by AI in the near term. A master woodworker's craft isn't. Physical, embodied, tacit D work has a longer runway than digital, textual, rule-based D work.

Within knowledge work: niche domain expertise matters. AI is generalist. An AI that's trained on a broad medical corpus is good at general medicine and weak on rare disease patterns in specific populations. The domain expert who's spent twenty years with that population has knowledge the generalist AI lacks.

### Path 4: Retrain

The hardest path, and the most important to be honest about. Not everyone can smoothly transition from D to P work, AI infrastructure, or specialized craft. For some people, the skills they built over a career are genuinely being made redundant.

The honest economic reality: retraining is difficult, expensive, and frequently fails. It works best when people are early in their careers (more years to amortize the investment), when they're moving into adjacent domains (shorter skill gap to cross), and when they have financial stability to invest the transition time.

For people who are mid-career, financially constrained, and in industries with high AI adoption rates: this is a real problem without an easy policy answer. Pretending otherwise doesn't serve them.

---

## 6) The Bimodal Labor Market

The combined effect of D wage compression and P wage premium is a bifurcation in the knowledge worker labor market.

Not a binary — there's still a distribution. But the distribution is shifting from a classic bell curve (most people in the middle, tails at each end) toward something more bimodal: a group capturing a significant P premium, and a larger group competing on D execution at compressed margins.

The factors that determine which group you're in:

| Factor | Toward P Premium | Toward D Compression |
|--------|-----------------|---------------------|
| **Role type** | Strategic, judgment-heavy | Execution-focused, process-based |
| **Seniority** | Senior (more P accumulated) | Junior (mostly D execution) |
| **Domain complexity** | High (AI struggles more) | Low/medium (AI catches up faster) |
| **Industry** | Slow-moving, high-stakes | Fast-moving, competitive |
| **Skill development** | Deliberately building P skills | Primarily optimizing D execution |

The uncomfortable implication: many people who believe they're "safe" because they work in high-paying knowledge work are in the middle of this transition, not above it.

A marketing manager at a mid-size company who spends 80% of their time producing D outputs — reports, briefs, content calendars, campaign summaries — is in a more precarious position than they realize. Their title is senior. Their skills are largely deterministic. The value of those skills is compressing whether or not the org chart reflects it yet.

---

## 7) The Education and Training Gap

There's a mismatch building between what educational institutions produce and what the labor market is starting to reward.

Most education is still optimizing for D execution:
- Learn the knowledge base
- Apply it correctly in tests
- Demonstrate competence through output quality

That trains students to be good at the work AI is now absorbing. It doesn't train them in framing ambiguity, working under uncertainty, calibrated confidence, or judgment under pressure — the skills that constitute P work.

This isn't a criticism of educators. D skills are real and valuable. And education systems are slow to change — they respond to labor market signals with a 10-20 year lag. The market is just moving faster than the institutions.

The near-term implication: P work skills will largely be learned on the job, not in school. The organizations that build deliberate P skill development into their culture, onboarding, and advancement criteria will have a compounding talent advantage over the ones that assume these skills develop naturally.

Corporate training has the same gap. Most L&D is still about D upskilling: how to use new tools, how to follow new processes, how to execute new methodologies. None of it is about developing judgment in high-uncertainty environments.

The organizations that figure out how to systematically train P work — framing, calibration, checkpoint design, decision quality review — will have workforces that are structurally more capable than their peers, independent of AI tooling.

---

## 8) The Uncomfortable Endgame

The long-run economic logic runs something like this:

1. AI automates D, compressing D wages
2. P work becomes the premium, but P wages hit a ceiling due to the non-scalability of judgment
3. As P wages rise, pressure increases to systematize P decisions
4. AI capabilities improve and begin absorbing simpler P work
5. The frontier of "what AI can't do" shifts upward in complexity
6. Humans maintain premium only at the current capability frontier of AI — which keeps moving

There's a name for this pattern: the technology skill treadmill. Each wave of automation pushes humans to higher-skill work, then eventually follows them there.

The optimistic reading: each round of automation expands total economic output, and humans end up doing more interesting work at higher compensation. The historical data mostly supports this, over long time horizons.

The pessimistic reading: the transitions are painful, not everyone makes it across, and the speed of AI capability improvement is compressing the time available for adjustment in ways that previous waves didn't.

Both are probably true. The economic outcome will be distributed unequally — the people who adapt early, who invest in P skills deliberately, who position in the right domains and organizations will do well. The people who don't will face compressing wages in a market that no longer values their primary skills.

That's not novel as an observation. It's how every major technology transition has worked. What's novel is the speed, and the fact that this wave is reaching knowledge work — the category that largely sat out previous waves of automation.

---

## The Practical Point

If you're reading this and wondering what to actually do:

The most defensible move isn't to speculate about which skills will matter in ten years. It's to start tracking your own D/P ratio today.

Look at a typical week:
- How much of your work is executing known tasks with known methods?
- How much is making judgment calls under genuine uncertainty?
- How much of your compensation is justified by execution capacity vs. judgment quality?

If your D ratio is high and growing, that's a signal worth acting on. Not panicking — acting. Find the adjacent P work in your domain. Develop calibration discipline. Build judgment infrastructure around your decisions. Shift the mix.

The economics aren't in your favor if you're mostly executing D work well and expecting that to hold its value.

The economics are significantly more in your favor if you're doing what AI struggles with — making good decisions under genuine uncertainty, in novel situations, with real skin in the game.

That's not guaranteed to be safe forever. But it's a longer runway than the alternative.

---

*Part of the D/P Framework series. Previous: [Organizational Structures for P Dominance](/blog/organizational-structures-for-p-dominance).*
*Building in public at [fullstackpm.tech](https://fullstackpm.tech). Follow along on [X @fullstackpmtech](https://x.com/fullstackpmtech).*
