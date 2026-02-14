---
title: "PM Interview Coach"
description: "AI-powered practice tool using real PM frameworks and ChatGPT evaluation."
tech_stack: [FastAPI, OpenAI ChatGPT, HTMX, Tailwind CSS, SQLite]
status: "shipping"
featured: true
display_order: 2
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: "/tools/interview-coach"
problem: "PM interview prep is fragmented. Candidates memorize frameworks but don't know how to apply them under pressure. Feedback comes too late to iterate."
approach: "Build an AI coach that evaluates answers in real-time using the same frameworks interviewers use (CIRCLES, RICE, HEART, STAR). Make feedback immediate and actionable."
solution: "An interactive tool where users answer PM questions and get structured feedback on frameworks, clarity, and strategy. They iterate until they're confident."
---
## What

An AI-powered interview practice platform that gives you realistic PM questions and immediate, structured feedback on your responses.

**You get:**
- Real PM interview questions across 4 categories (Product Design, Strategy, Execution, Analytical)
- Instant AI evaluation on 4 dimensions: overall score, framework usage, structure, completeness
- Specific strengths and gaps highlighted in every answer
- Progress tracking to see improvement over time
- No API key required — everything runs server-side

## Why

PM interview prep has a fundamental problem: **feedback lag.**

You practice in a vacuum, memorize frameworks, and hope they stick. Then you hit the real interview and realize there's a gap between understanding CIRCLES and *using* CIRCLES under pressure.

I built this because:
- **Candidates need iteration, not just memorization.** Real learning happens when you answer, get feedback, adjust, and try again.
- **Interviewers look for reasoning, not perfection.** The tool evaluates how you think, not whether you're "right."
- **The best interview prep feels like the real thing.** Realistic questions, structured evaluation, honest feedback.

This tool bridges that gap. It's the coach who gives you feedback at 2am when no actual interviewer is available.

## How

**The flow is simple:**

1. **Pick a category** — Product Design, Strategy, Execution, or Analytical
2. **Read your question** — Realistic PM scenarios (e.g., "Design a feature to help users discover restaurants")
3. **Answer out loud** — Structure your thinking like you would in a real interview
4. **Get scored** — AI evaluates on frameworks, structure, and completeness
5. **See feedback** — Strengths, improvements, and suggested frameworks
6. **Practice again** — Pick another question and iterate

**Under the hood:**
- Questions are curated to reflect real PM interviews (not trick questions)
- OpenAI ChatGPT evaluates answers against PM frameworks (CIRCLES, RICE, HEART, STAR, etc.)
- Each evaluation is stored so you can track progress over time
- The AI gives specific, actionable feedback (not vague praise or criticism)

**Why no API key?**
All AI evaluation runs server-side. You don't need to set up OpenAI or worry about costs. Just practice.

## Technical Stack

- **Backend:** FastAPI (Python) — async, fast, built for real-time feedback
- **AI Engine:** OpenAI ChatGPT (gpt-4o-mini) — evaluates answers against frameworks
- **Database:** SQLite — stores your sessions and scores
- **Frontend:** HTMX + Tailwind CSS — interactive without JavaScript bloat
- **Deployment:** Render — single command deploy, auto-scales
