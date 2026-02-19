---
title: SDE Interview Prep Tracker
slug: sde-prep-tracker
description: Comprehensive software engineering interview preparation tool with LeetCode tracking, system design topics, daily task planning, behavioral stories, and progress analytics.
status: live
featured: true
display_order: 1
github_url: "https://github.com/harsha-k-cheruku/fullstackpm.tech"
live_url: /tools/sde-prep
problem: "SDE candidates juggle multiple tools for interview prep: LeetCode for coding, Notion docs for system design, spreadsheets for tracking, video playlists for learning. This fragmentation kills focus, causes scattered progress tracking, and makes it impossible to see overall interview readiness."
approach: "Build an integrated, single-source-of-truth interview prep platform. Pre-seed with 60+ LeetCode problems, 15 system design topics, STAR-format behavioral stories, and a 12-week curriculum. Use HTMX for seamless real-time updates. Focus on clarity, not complexity."
solution: "A comprehensive prep tracker with dashboard analytics, LeetCode problem tracking (with Blind 75 flagging), system design topics with confidence levels, behavioral story manager, 12-week curriculum with daily tasks, and real-time progress visualization via Chart.js—everything pre-loaded and ready to use."
categories:
  - Tool
  - Education
  - Productivity
tech_stack:
  - FastAPI
  - SQLAlchemy
  - HTMX
  - Tailwind CSS
  - Chart.js
duration: 4 weeks
team_size: 1
role: Full Stack Developer
---

# SDE Interview Prep Tracker

## Overview

A comprehensive interview preparation tracking application designed to guide software engineers through a structured 12-week interview readiness program. Combining LeetCode problem tracking, system design preparation, behavioral story management, and daily task planning with real-time progress visualization.

## Key Features

### 📊 Dashboard
- Real-time progress tracking across 4 categories:
  - LeetCode problems (solved/total, Blind 75 subset)
  - System Design topics (confidence levels)
  - Behavioral stories (readiness status)
  - Current week progress
- Study streak tracking
- Interactive Chart.js visualizations:
  - Difficulty distribution (doughnut chart)
  - Weekly progress trends (bar chart)
  - Study hours analytics (line chart)

### 💻 LeetCode Tracker
- 60+ LeetCode problems seeded across all major categories
- Blind 75 problems flagged and tracked separately
- Advanced filtering: difficulty, category, status, Blind 75
- Per-problem tracking:
  - Status: Not Started → In Progress → Completed → Review
  - Attempt counter
  - Solution approach, time/space complexity notes
  - Practice session logging with timing
  - Direct links to problems

### 📅 Daily Plan
- 12-week structured study plan
- Week/day selectors with granular task lists
- 50+ seeded tasks covering:
  - Coding problems (with problem links)
  - System design topics (with topic links)
  - Behavioral prep
  - Reading and review
  - Networking activities
- Real-time completion tracking
- Task time estimates and actual time logging
- Progress bars with live updates

### 🏗️ System Design
- 15 curated system design topics
- Walmart-specific design challenges (Shopping Cart, Inventory, Pricing)
- Topic tracking with confidence levels
- Practice session counter
- Structured notes:
  - Key concepts
  - Common patterns
  - Resources and references
- Last practiced timestamps

### 🎭 Behavioral Stories
- STAR format story manager (Situation, Task, Action, Result)
- Story metadata:
  - Category (Leadership, Conflict, Failure, Technical, etc.)
  - Company relevance
  - Leadership principle alignment
  - Practice counter and readiness status
- Quick story editing and iteration

### 📈 Study Plan
- 12-week journey view
- Weekly goals tracking
- Completion percentages and checkpoints
- Week-specific notes and reflections
- Complete study roadmap visibility

## Technical Implementation

### Backend Architecture
- **Framework:** FastAPI with async/await
- **Database:** SQLite with SQLAlchemy ORM
- **7 Models:** LeetCodeProblem, PracticeSession, SystemDesignTopic, BehavioralStory, WeekPlan, DailyTask, DailyLog
- **Pattern:** RESTful API with HTMX integration for seamless updates

### Frontend
- **HTMX:** Real-time updates without page refreshes
- **Tailwind CSS:** Responsive design with Walmart brand colors
- **Chart.js:** Interactive data visualizations
- **Patterns:** Auto-save on blur, filter-based reloading, live progress updates

### Design System
- **Walmart Brand Colors:**
  - Primary Blue: #0053e2
  - Spark Yellow: #ffc220
  - Success Green: #2a8703
  - Error Red: #ea1100
- **Difficulty Color Coding:** Easy (Green), Medium (Amber), Hard (Red)
- **Tool-specific Navigation:** Secondary nav with branded styling

## Data Integrity

- 60+ LeetCode problems (all Blind 75 included)
- 15 system design topics with Walmart-specific challenges
- 12-week curriculum with 3-5 goals per week
- 50+ daily tasks with problem/topic linking
- Duplicate prevention in seed script
- Transaction-safe updates

## Interactions & UX

1. **Dashboard:** Load stats on page load, render charts dynamically
2. **Problem Tracking:** Filter → Click status → Update → Real-time DB sync
3. **Daily Tasks:** Select week/day → View tasks → Check off → Progress bar updates
4. **System Design:** Click topic → Edit notes → "Mark Practiced" increments count
5. **Behavioral:** New story → Fill STAR fields → Auto-save on blur → Mark ready
6. **Study Plan:** View all weeks → Check complete → Track progress

## Impact & Outcome

- **Comprehensive:** Covers all major SDE interview categories (coding, system design, behavioral)
- **Structured:** 12-week curriculum prevents overwhelm and provides clear progression
- **Trackable:** Real-time analytics show what's working and where to focus
- **Motivating:** Visual progress, streak tracking, and clear milestones encourage consistency
- **Efficient:** Integrated tool reduces context switching between multiple apps

## Success Metrics

- All 6 pages load without errors
- Dashboard charts render with real data
- HTMX interactions update database in real-time
- Filtering works across all major views
- 100% seed data seeded without errors
- Mobile responsive design maintains functionality
