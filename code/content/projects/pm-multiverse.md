---
title: "PM Multiverse"
description: "Same problem. 5 PM brains. Where do the experts disagree — and which one thinks like you?"
tech_stack: [FastAPI, Vanilla JS, SQLite, SQLAlchemy]
status: "live"
featured: true
display_order: 1
github_url: "https://github.com/harsha-k-cheruku/pm-multiverse"
live_url: "/tools/pm-multiverse"
problem: "PM frameworks are taught in isolation. You read Cagan, Torres, or Doshi separately and absorb each worldview. But real PM judgment comes from understanding where smart people genuinely disagree — and being forced to pick a side before you see the answers."
approach: "Build an interactive experience where 5 expert PM personas (Cagan, Torres, Doshi, Lenny, Exec AI Monster) tackle the same 10 real product problems but explicitly disagree. Users commit to their own answers first, then discover where they align with each expert and why."
solution: "A 5-step interactive tool: answer 3 forced-choice questions first (no peeking), see your persona blend, explore where the 5 experts split on the key decision, cast your vote, and unlock your PM DNA card after 3 problems."
---
## What

An interactive PM thinking tool where 5 expert personas solve the same real product problems — and explicitly disagree with each other.

**10 problems. 5 personas. Zero consensus.**

- Answer 3 forced-choice questions before seeing any expert take
- Discover your PM DNA blend (e.g. "62% Doshi, 24% Torres")
- See exactly where Cagan, Torres, Doshi, Lenny, and the Exec AI Monster split
- Read each persona's full breakdown: problem framing, solution, MVP, metrics, roadmap, and spicy quote
- Cast your vote — see live community results
- Unlock your shareable PM DNA Card after 3 problems

## Why

Most PM education teaches frameworks in isolation. You study the Opportunity Solution Tree or Four Product Risks as standalone tools, not as competing lenses that smart people apply differently to the same problem.

The insight that makes PM Multiverse different: **the learning is in the disagreement.**

When Marty Cagan says "validate before you ship" and the Execution AI Monster says "you're already late — ship in 2 weeks," both are right in different contexts. The skill is knowing which one applies — and being honest about which instinct you default to.

By forcing you to answer first, you can't reverse-engineer your response from the expert answers. Your PM DNA is revealed by your instincts, not your knowledge.

## How

**The 5 Personas:**

| Persona | Voice | Default Instinct |
|---------|-------|-----------------|
| Marty Cagan | Outcome-first, risk-driven | Validate ruthlessly before building |
| Teresa Torres | Continuous discovery, evidence-led | Map the opportunity tree before committing |
| Shreyas Doshi | Strategy-first, LNO thinking | Find the sharpest wedge, pre-mortem everything |
| Lenny Rachitsky | Growth loops, experiments, benchmarks | Personally recruit the first 100, build the flywheel |
| Execution AI Monster | Ship now, fix later, win markets | Being live with 60% beats being right with 90% |

**The 10 Problems:**
YouTube Brazil launch, Spotify personalization decay, Meta SMB product, App Store launch strategy, Amazon Prime gifting, Meta Marketplace monetization, Redfin Hot Home badge, Netflix entering podcasts, OpenTable no-shows, Slack onboarding activation.

**Under the hood:**
- Each problem JSON has 3 quiz questions with per-persona weights, full persona deep-dives, The Split positions, MVP options, pre-mortem risks, and PM DNA blends
- Vote counts stored in SQLite — community results are real, not simulated
- localStorage tracks your votes, reactions, and completed problems across sessions
- PM DNA Card unlocks after 3 problems — shows your persona blend as a donut chart with your archetype name and tagline
