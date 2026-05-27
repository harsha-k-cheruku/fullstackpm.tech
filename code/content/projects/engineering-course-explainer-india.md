---
title: "Engineering Course Explainer (India)"
description: "A curated guide to 12 high-interest engineering branches — what you study, what work it leads to, what students get wrong, and how to compare branches sensibly."
tech_stack: [FastAPI, Jinja2, Tailwind CSS, Python Dataclasses]
status: "live"
featured: true
display_order: 1
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/projects/engineering-course-explainer-india/explore"
problem: "Students making engineering branch decisions rely on relatives, Quora panic threads, coaching center rankings, and YouTube clickbait — none of which are designed to help them think clearly about actual work fit."
approach: "Curate 12 high-interest branches with honest, opinionated content — what you study, what work it leads to, what students get wrong, and how to compare. No giant fake-complete catalogs. No ranking theater."
solution: "A decision-quality resource with branch explainers covering ELI10, Reality Checks, Choose/Avoid guidance, Misconceptions, Real-World Examples, and a side-by-side comparison tool — all scoped to 12 branches that actually matter."
---

## What

A curated engineering branch explainer built for Indian students making JEE/JoSAA counselling decisions.

**12 branches, each with:**
- Explain It Like I'm 10 — simple, vivid explanation
- School Connection — "If you liked X in school, this extends that"
- Reality Check — honest assessment of what the branch actually demands
- Choose This If / Avoid This If — direct decision guidance
- What You Study — 5–6 specific topics, not vague one-liners
- Problems You'll Solve — concrete work examples
- Career Paths — specific roles, not generic "engineer" labels
- Trade-offs — what students underestimate or misunderstand
- Misconceptions — the 4 most common things students get wrong
- Real-World Examples — 5 specific projects graduates actually work on
- Good Fit Checklist — self-assessment questions
- Similar Branches — clickable links for comparison

**Compare Tool:**
Side-by-side comparison of any two Top 12 branches with Reality Check, Choose/Avoid, study content, and trade-offs displayed together.

## Why

**The Problem:**
Engineering branch selection in India is one of the most high-stakes, low-information decisions students make. The existing information landscape is:
- **Quora/Reddit** — opinions from anonymous users, often biased or outdated
- **YouTube** — optimized for views, not for decision quality
- **Coaching centers** — focused on rank optimization, not work-fit thinking
- **Relatives** — well-meaning but working with decades-old mental models

Students end up choosing branches based on cutoff rankings, peer pressure, or family expectations rather than understanding what the branch actually teaches and where it leads.

**Why This Matters:**
A student who picks CSE because "everyone says it's the best" but actually hates debugging will be miserable. A student who avoids Metallurgy because "it sounds old" might miss a career they would have loved. The cost of a bad branch decision is 4 years of friction and regret.

**Why This Approach:**
- **Curated scope** — 12 branches, not 180. Quality over fake completeness.
- **Decision-oriented** — every section is designed to help you decide, not just inform.
- **Honest tone** — includes trade-offs, misconceptions, and "avoid this if" guidance that most resources skip.
- **Comparison tool** — because branch decisions are usually between 2–3 options, not evaluated in isolation.

## How

**Architecture:**

```
Python dataclass per branch (12 total)
    ↓
CourseExplainerService (in-memory, no DB, no file I/O)
    ↓
FastAPI routes → Jinja2 templates
    ↓
Index (grid + decision helpers) / Detail (full explainer) / Compare (side-by-side)
```

**Key Design Decisions:**

1. **Hardcoded data, not a database** — 12 branches is small enough to keep in a Python file. No JSON loading, no DB queries, no file I/O at startup. This eliminates an entire class of deployment failures.

2. **Frozen dataclasses** — immutable data means no accidental mutation and no state bugs.

3. **Decision-first content structure** — every section exists because it helps a student decide, not because it fills a template. "Reality Check," "Choose/Avoid," and "Misconceptions" are the sections most guides skip — and the ones students need most.

4. **Compare tool scoped to Top 12 only** — prevents dropdown bloat and forces the comparison to be between branches worth comparing.

5. **School Connection field** — maps school subjects to branches, which is the most natural starting point for a student who does not yet know what "engineering branches" mean.

**Content Quality Bar:**
Each branch has 600–730 words of curated content across all sections. Every misconception, every example project, and every trade-off is written to be specific to the branch — not generic filler.

---

## What's Next

- Add more branches based on user interest signals
- Add a "branch finder" quiz that suggests branches based on school subject preferences
- Consider integrating historical JoSAA cutoff data for context
- Explore audio explainers for each branch (podcast-style)
