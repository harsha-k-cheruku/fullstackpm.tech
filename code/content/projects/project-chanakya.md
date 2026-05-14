---
title: "Project Chanakya — PM Interview Prep"
description: "PM interview prep pipeline that turns real interview questions into interactive learning episodes — Saraswati analysis, guided reasoning, decision-point exercises, and a reusable thinking framework per question type."
tech_stack: [Python, Claude API, OpenAI TTS, FastAPI, Playwright, ffmpeg, Jinja2]
status: "in_progress"
featured: true
display_order: 4
github_url: ""
live_url: "/resources/pm-prep"
problem: "❌ Most PM interview prep teaches answers. Candidates memorise frameworks but freeze when the actual question deviates. The prep doesn't build the judgment — it builds pattern-matching."
approach: "💡 Each question runs through Saraswati analysis (first-principles deconstruction), then becomes 3 audio episodes covering Product Thinking, Metrics, and Execution — with interactive decision points on the site."
solution: "✅ Live at /resources/pm-prep. First question: Redfin Hot Home feature. Each episode has decision points (mid/senior/staff level choices), calibrated feedback, and ends with a reusable framework for that question type."
---

## What

Project Chanakya (named after the ancient Indian strategist and author of Arthashastra) is a PM interview prep pipeline. One real PM interview question per week, broken into three focused episodes published every 3 days — Product Thinking, Metrics & Measurement, and Execution & Trade-offs.

Not frameworks. How to think.

## The Content Pipeline

**Saraswati Analysis** — Each question is deconstructed by the Saraswati agent:
- What is the interviewer actually testing (not the surface skill)?
- Where do standard prep answers fall short for this specific question?
- What would first-principles reasoning conclude?
- 3 guided questions with step-by-step reasoning
- The framework that applies to this class of question
- Seniority calibration: how mid vs senior vs staff answers differ

**Three Episodes** — Each covers one dimension:
1. Product Thinking — reframe the problem, identify users, locate the real tension
2. Metrics & Measurement — accuracy-first framework, north star, diagnostic tree
3. Execution & Trade-offs — prioritisation process, explicit cuts, the transferable pattern

**The Pattern** — Episode 3 ends with "The Pattern" — the reusable framework crystallised. Name, steps, seniority shift, and a transfer example showing it works on a different question.

## The Interactive Experience

Episodes are not passive. On the site, each episode renders as a native interactive exercise:

- **Decision points** — 3 choices per key fork in the reasoning (calibrated to mid/senior/staff thinking level)
- **Progressive reveal** — content unlocks as you commit to choices
- **Calibrated feedback** — warm, specific, never "wrong/right" before you click
- **Result summary** — "Senior-level thinking / Developing / Building the foundation" based on your choices
- **Teaching style** — Phase 1 is "watch how I think" (Socratic teaching, not testing)

## Source Material

Questions sourced from a 1,700+ question bank (PM Questions.xlsx) supplemented by 7 Munna kaka DOCX files covering product design, strategy, execution, and analytics. Classified by category, difficulty, and company archetype. Code Puppy processes the source files, runs Saraswati analysis, writes episode content, generates audio, and publishes.

## Audio

OpenAI TTS (tts-1-hd). Voice rotates per question — all 3 episodes for one question use the same voice (series consistency), different questions use different voices (onyx → echo → fable, cycling). Speed: 0.90x. Intro sting + low ambient background mixed via ffmpeg.
