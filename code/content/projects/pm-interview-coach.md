---
title: "PM Interview Coach"
description: "AI-powered practice tool using real PM frameworks and Claude API"
tech_stack: [FastAPI, Claude API, HTMX, Tailwind CSS, SQLite]
status: "in_progress"
featured: true
display_order: 2
github_url: "https://github.com/hcheruku/pm-interview-coach"
live_url: ""
---
## The Problem
PM interview prep is fragmented and often optimized for memorization instead of real practice. Candidates rarely get structured feedback on their reasoning, prioritization, or trade-offs, which leaves gaps that show up in live interviews.

## The Approach
Build an AI-powered coach that simulates realistic PM interviews using Claude. The product should mirror how interviewers evaluate answers: clear framing, structured prioritization, and measurable impact.

## The Solution
The web app lets users pick a question type (product design, estimation, strategy, behavioral), receive a realistic prompt, and submit a response. The system scores the answer against frameworks like CIRCLES, RICE, and HEART, highlighting strengths, gaps, and suggested improvements. Users can iterate quickly and track their progress over time.

## Technical Details
- **FastAPI** backend serving prompt sessions and feedback results
- **HTMX** to stream AI feedback in real-time
- **SQLite** for storing interview sessions and scoring history
- **Tailwind CSS** for a clean, responsive UI
