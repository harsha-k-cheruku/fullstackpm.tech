---
title: "How I Built PM Multiverse in a Weekend"
date: 2026-02-25
tags: [product-management, ai, building-in-public, full-stack-pm, pm-multiverse]
excerpt: "I was tired of PM case studies that feel like homework. So I built a tool where 5 AI personas argue about real product problems — and you vote on who's right. Here's how."
author: "Harsha Cheruku"
---

Most PM case study resources have the same problem: they give you a scenario and then tell you the "right" answer.

That's not how product management works. In real life, smart people disagree. The VP of Product wants to ship fast. The research lead wants another round of discovery. The growth PM wants to run an experiment. The founder wants to bet on a wedge.

Nobody's wrong. They're just optimizing for different things.

I wanted to build something that captured that tension — the *disagreement* between experienced PMs — and let you form your own opinion first, before seeing theirs.

That's PM Multiverse.

---

## The Idea (Saturday Morning)

I was reading a Lenny Rachitsky post about YouTube's expansion into Brazil. Classic two-sided marketplace problem: you need creators to attract viewers, but creators won't show up without viewers.

And I thought: what would Marty Cagan say about this? He'd want to validate creator supply before spending a dollar. What about Teresa Torres? She'd want weekly touchpoints with Brazilian creators. Shreyas Doshi? He'd pick the sharpest wedge — maybe music — and go all in.

They'd all be right. And they'd all disagree.

What if you could watch them argue?

---

## The Core Bet

The insight was simple: **PM case studies are boring because they're passive. You read, you nod, you forget.**

What if instead:

1. You answer the hard questions *before* seeing any expert opinion
2. Five distinct PM voices each give their full take — strategy, MVP, metrics, roadmap
3. They disagree with each other openly (not politely)
4. You vote on whose approach you'd actually run
5. You see how your thinking compares to the crowd

That's not a case study. That's a simulation.

---

## The Five Personas

This was the creative core. I needed voices that felt distinct enough to genuinely disagree.

I built five personas, each representing a real school of PM thought:

| Persona | Philosophy | In One Line |
|---------|-----------|-------------|
| **Marty Cagan** 📚 | Outcome-first. Risk-driven. | "Prove your assumptions before you ship a single line." |
| **Teresa Torres** 🔭 | Continuous discovery. Evidence-driven. | "When's the last time you talked to a user? Not last quarter — last week." |
| **Shreyas Doshi** ⚔️ | Strategy-first. LNO framework. | "Find the sharpest wedge and pour everything into it." |
| **Lenny Rachitsky** 📈 | Growth loops. Benchmarks. Experiments. | "Personally recruit the first 100. Then build the referral loop." |
| **The Exec** ⚡ | Ship now. Fix later. Win the market. | "Two weeks. Ship it. Learn from live data." |

Each persona gets the same structure for every problem:
- A **spicy quote** (memorable, slightly snarky, in their real voice)
- Their **problem breakdown** (how they see the challenge)
- Their **solution** (what they'd actually do)
- Where they **disagree** with the others (the good part)
- A concrete **MVP** (4 steps)
- **Metrics** they'd track
- A **4-phase roadmap** with timelines
- A **scoreboard** rating them on Speed, Risk Management, Strategy, and Growth (1-10)

The disagreement section is the heart of PM Multiverse. When Cagan says "you'd be reckless to launch without validating creator willingness" and the Exec says "90 days of live data beats 90 days of research" — that's a real tension PMs face every week.

I didn't resolve it. The tool doesn't pick a winner. That's the point.

---

## The 6-Step Experience

### Step 1: Pick a Problem

Ten real PM problems arranged in a grid. YouTube Brazil, Spotify Discover Weekly, Netflix Podcasts, Amazon Prime Gift Cards, Slack Onboarding — each from a different domain so you can find one that matches your world.

### Step 2: Your Take First

Three rapid-fire questions. You answer before seeing any expert opinion.

This was a deliberate design choice. If I showed the persona takes first, everyone would just anchor on whichever expert they admire most. By forcing you to commit first, you actually think.

Each answer carries hidden persona weights — your choices map to the five personas without you realizing it.

### Step 3: Your PM DNA Reveal

After three questions, the tool calculates your PM DNA blend. Something like: 40% Cagan, 30% Doshi, 20% Torres. It names your archetype — "The Strategic Guardian" or "The Loop Engineer" — based on your blend.

There are 27 custom archetype names for different persona combinations. If you're a Cagan-Torres blend, you're "The Evidence Purist: You won't ship until the data says yes." If you're Lenny-Exec, you're "The Momentum Machine: You ship loops that compound before competitors finish their roadmap."

People screenshot this. It's the personality test mechanic — but instead of Hogwarts houses, it's PM decision-making styles.

### Step 4: The Arena

This is where it gets interesting. All five personas present their full case. You can tab between them or compare two side-by-side.

The top of the screen shows "The Split" — the core question where experts divide into 2-3 camps. For YouTube Brazil:

- **SHIP NOW** — Lenny + The Exec
- **VALIDATE FIRST** — Cagan + Torres
- **SHIP THE WEDGE** — Doshi (alone, naturally)

Below that, each persona's deep dive. Spicy quote. Breakdown. Solution. Where they disagree. MVP. Metrics. Roadmap. Scoreboard.

It's a lot of content. But it's structured so you can skim one persona in 30 seconds or spend 10 minutes comparing two.

### Step 5: Vote

One question: "Whose approach would you run?"

Five cards, one per persona. Pick one. After voting, you see how the community voted — the distribution across all five personas for that problem.

I seeded initial vote data so early users see realistic distributions. As real votes come in, they gradually replace the seeds.

### Step 6: PM DNA Card

Complete 3 problems and you unlock a shareable DNA card — a donut chart showing your persona blend, your archetype name, and a tagline.

Until you hit 3 problems, the card is blurred with a lock icon. Simple gamification, but it works. People come back to unlock it.

---

## The Technical Build

### Data Architecture: JSON Files, Not a Database

Each problem is a single JSON file. Here's the skeleton:

```json
{
  "id": "youtube-brazil",
  "title": "Launch YouTube in Brazil",
  "tags": ["Strategy", "Market Entry"],
  "prompt": "YouTube wants to expand to Brazil...",
  "yourTakeFirst": {
    "questions": [
      {
        "text": "What's your first move as PM?",
        "options": [
          {
            "label": "Deep discovery research",
            "personaWeights": { "cagan": 2, "torres": 3, "doshi": 1 }
          }
        ]
      }
    ]
  },
  "personas": {
    "cagan": { "spicyQuote": "...", "breakdown": [...], "mvp": [...] },
    "torres": { ... },
    "doshi": { ... }
  },
  "voteResults": { "cagan": 18, "torres": 12, "doshi": 35, "lenny": 22, "exec": 13 }
}
```

One file per problem. Easy to add new ones. Easy to version control. No migrations. No schemas. Just structured content.

Ten problems. Each file is around 300 lines of JSON. The entire dataset fits in the browser cache.

### Frontend: Vanilla JS, No Framework

No React. No Vue. No build step. Just a single `problem.html` file with inline JavaScript that:

1. Fetches the problem JSON
2. Renders each step as the user progresses
3. Calculates persona weights from quiz answers
4. Builds the DNA chart as SVG
5. Posts votes to the server

The entire frontend is one HTML file. Under 2,000 lines including the CSS.

Why no framework? Because this is a linear 6-step experience. There's no complex state. No routing. No component reuse. A framework would've added build complexity for zero benefit.

### State: localStorage First

All user progress lives in the browser:

```
pmm_done_youtube-brazil = "1"     // completed this problem
pmm_vote_youtube-brazil = "doshi" // voted for Doshi
```

No login. No accounts. No database queries for user state. Just localStorage.

The tradeoff: you lose your progress if you clear your browser. That's fine for now. The tool is about the experience, not long-term data retention.

### Votes: Hybrid Local + Server

Votes are the one thing that needs to be shared across users. So they go to the server:

```
POST /api/pmm/votes
{ "problem_id": "youtube-brazil", "persona": "doshi" }
```

The server stores votes in SQLite. When displaying results, it checks: if the database has votes, use those. If not, fall back to the seed data in the JSON file.

This means the tool works perfectly even if the server is down — it just shows seed data instead of live data. Graceful degradation.

---

## Design Decisions That Mattered

### Always-dark theme

PM Multiverse runs on a dark background (`#0b0d12`) with cyan accents (`#5ee4ff`). No light mode toggle. No dark mode toggle. Just dark.

Why? Two reasons. First, it creates visual separation from fullstackpm.tech (which has light/dark toggle). PM Multiverse should feel like its own product. Second, the persona colors — red, cyan, purple, yellow, green — pop dramatically on dark backgrounds.

### Animations as pacing

Every section fades up with a staggered delay. The quiz options slide in. The DNA chart builds itself. Score bars animate from zero.

These aren't decorative. They're pacing. PM Multiverse has a lot of content per problem. Animations create natural pauses that let users absorb each section before the next one appears.

### The "spicy quote" pattern

Every persona starts with a memorable one-liner. Cagan: *"You're about to pour millions into a market you haven't validated. That's not ambition — that's negligence."* The Exec: *"Six months of discovery for a product that needs to ship yesterday. Classic."*

These do two things: they immediately establish the persona's voice, and they make the user smile. Both matter for engagement.

---

## What Surprised Me

**Doshi wins a lot of votes.** Across problems, the "find the sharpest wedge" approach resonates with more people than I expected. PMs like the idea of focus over breadth.

**People spend real time in the Arena.** The average session isn't a quick click-through. Users actually read the persona breakdowns and compare scorecards. The content density works because the voices are distinct enough to be interesting.

**The DNA card drives repeat usage.** The 3-problem unlock is the single biggest factor in people coming back. It's a simple mechanic but the "personality test" instinct is powerful.

---

## What I'd Do Differently

**More problems, faster.** Ten is a solid start, but 20-25 would give users enough variety to find problems in their domain. I should've built a faster problem authoring pipeline from day one.

**Shareable DNA cards.** The "Share on LinkedIn" button is a placeholder right now. A proper share flow — generate an image, pre-fill a LinkedIn post — would be the single biggest growth mechanic.

**Email capture after the DNA reveal.** The moment someone sees their PM archetype is the highest-engagement moment. That's when you ask "Want new problems in your inbox?" I missed this.

---

## The Numbers

- **Build time:** One weekend (about 14 hours of actual work)
- **Problems:** 10 (targeting 20)
- **Personas per problem:** 5 (each with full strategy, MVP, metrics, roadmap)
- **Quiz questions per problem:** 3
- **Custom DNA archetypes:** 27 unique blend names
- **Lines of JavaScript:** ~1,200
- **Lines of CSS:** ~800
- **JSON data per problem:** ~300 lines
- **Framework dependencies:** Zero

---

## The Real Point

PM Multiverse isn't really about PM case studies. It's about a belief:

**The best way to learn product management is to sit in the disagreement.**

Not to hear one "right" answer. Not to memorize a framework. But to watch five smart people look at the same problem and reach different conclusions — and then figure out where you stand.

That's what real PM work feels like. Every day, in every room, with every stakeholder.

I just made a tool that simulates it.

---

**Try it:** [PM Multiverse on fullstackpm.tech](/projects/pm-multiverse)

**Have a problem you want to see in PM Multiverse?** Drop it in the comments or DM me on [LinkedIn](https://linkedin.com/in/harshacheruku) or [X/Twitter](https://x.com/fullstackpmtech).

Next up: I'm adding email capture, shareable DNA cards, and 10 more problems. Follow along at [fullstackpm.tech](https://fullstackpm.tech).
