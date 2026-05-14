---
title: "Project Narada — Daily Intelligence Brief"
description: "Fully automated daily podcast pipeline — SPY options education, global news, and PM analytics distilled into a 15-20 min audio brief every morning at 7 AM."
tech_stack: [Python, OpenAI TTS, Claude API, FastAPI, ffmpeg, launchd, RSS]
status: "live"
featured: true
display_order: 2
github_url: ""
live_url: "/resources/daily-brief"
problem: "❌ Staying current across SPY options, global markets, and PM content requires monitoring multiple sources daily — most people skip it because it takes too long."
approach: "💡 Fully automated pipeline: ingest (SPY + news RSS + FRED macro) → distill via LLM → script → OpenAI TTS → publish. Runs at 7 AM PT via launchd. No human involvement."
solution: "✅ A 15-20 min daily audio brief published to fullstackpm.tech with show notes, RSS feed for Apple Podcasts, and a pre-baked lesson curriculum on SPY options fundamentals."
---

## What

Project Narada is a fully automated daily intelligence pipeline named after the divine sage-messenger of Hindu mythology. In the Mahabharata and Puranas, Narada travels ceaselessly between the heavens and the mortal realm — never settling, always carrying information between worlds. This pipeline does the same: running before dawn, pulling from markets, news feeds, and macro data across continents, and distilling it into something you can hear while making coffee. The name felt right the moment it came up.

Every morning at 7 AM PT, it fetches live SPY options data, global news across 6 regions, and macro indicators — distills everything into a structured podcast script — and generates a 15-20 minute audio episode published to fullstackpm.tech and the Apple Podcasts RSS feed.

## Architecture

The pipeline runs in five stages, each modular and swappable:

**Ingest** — Three parallel ingestors: SPY price, IV rank, ATM options chain, and sector attribution via yfinance; global news from 20+ RSS feeds segmented by region; FRED macro data (CPI, Fed Funds, yield curve, mortgage rates).

**Distill** — Two LLM calls (Claude Haiku / GPT-4o-mini with fallback): news roundup with market connection chains, and daily market brief with sector attribution. SPY learning segment uses pre-baked lesson files — no LLM call on most days.

**Script** — One LLM call (Claude Sonnet) weaves all segments into a coherent podcast script with natural transitions.

**Audio** — OpenAI TTS (tts-1-hd) with daily voice rotation across 5 male/female pairs. Background ambient music mixed via ffmpeg. Intro sting generated programmatically.

**Publish** — MP3 copied to fullstackpm.tech, episodes.json updated, git push triggers Render auto-deploy. RSS feed updates for Apple Podcasts.

## SPY Learning Curriculum

A 9-module, 47-lesson curriculum on SPY options fundamentals (Greeks, implied volatility, iron condors, macro factors, trade management). Lessons are pre-generated and served as static audio — reducing daily pipeline runtime from ~90 minutes to ~10 minutes and dropping TTS cost from $0.23 to $0.08 per episode.

## Content Features

- **Guided reasoning** embedded in SPY lessons (Phase 1 teaching mode — host models the thinking, not tests the listener)
- **India/emerging market relevance filter** — only stories with plausible market impact (no cultural/political noise)
- **Sector attribution** — "Technology (XLK) fell 1.4%, the biggest drag on SPY today"
- **Catalyst calendar** — hardcoded BLS CPI release dates, FOMC dates; pipeline adjusts framing based on whether a release has already happened that morning
