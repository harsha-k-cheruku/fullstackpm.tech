---
title: "Project Narada — Daily Intelligence Pipeline"
description: "A fully automated daily podcast that distills SPY options intelligence, global news, and PM analytics into a morning audio brief."
featured: true
status: live
tech_stack:
  - Python
  - Claude API
  - OpenAI TTS
  - FastAPI
  - yfinance
  - FRED API
  - ffmpeg
display_order: 2
github_url: ""
live_url: "https://fullstackpm.tech/podcast"
problem: "Staying current on markets and PM ideas is easy to want and annoying to do every single day."
approach: "Build a configurable morning pipeline that ingests, distills, scripts, narrates, and publishes one tight daily brief."
solution: "A modular provider-driven system that turns curated inputs into an episode, show notes, RSS, and portfolio artifact."
---

## The Problem

I wanted to build expertise in SPY options trading and stay current on PM and analytics frameworks, but I do not have the patience to manually curate that learning loop every morning.

The useful constraint is simple: I have audio time. Commute time, walk time, workout time. So the better product is not another dashboard. It is a daily brief that already knows what I am trying to learn.

## What It Does

Project Narada runs early in the morning and turns a messy pile of source material into one coherent episode.

1. **Ingests** SPY price data, options context, macro indicators, earnings events, global headlines, and PM or analytics writing.
2. **Distills** each domain into structured talking points with swappable LLM providers.
3. **Writes** a full conversational script instead of dumping four disconnected summaries.
4. **Generates audio** with voice-specific narration and light ambient mixing.
5. **Publishes** the final episode to `/podcast` with show notes and RSS support.

## The Learning System

The SPY segment follows a progressive curriculum. It starts with the Greeks, moves into volatility and spreads, and then layers in macro context and trade management. Each lesson is anchored to what SPY actually did that day, which makes the content more practical than generic finance explainers.

## Architecture

```text
INGEST (parallel)     DISTILL        AUDIO          PUBLISH
Yahoo Finance  ──┐
FRED API       ──┤→ Claude API ──→ OpenAI TTS ──→ fullstackpm.tech
Earnings Cal   ──┤    + providers      + ffmpeg      /podcast
RSS Feeds      ──┘                     mixing         RSS feed
```

## Why I Built It This Way

- **Automated** enough that I can just listen.
- **Modular** enough that providers can be swapped without rewriting orchestration.
- **Configurable** enough to steer topics and tags over time.
- **Useful twice** because the same system that teaches me also publishes a public artifact.
