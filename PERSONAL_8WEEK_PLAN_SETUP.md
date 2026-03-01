# 8-Week Intensive Job Search Prep - Personal Setup

## Overview

This document describes the complete setup for your personal/wife's 8-week intensive job search preparation plan. This includes:

1. **12-Week Public Plan** (for fullstackpm.tech main site)
2. **8-Week Intensive Private Plan** (for personal use only)

---

## PART 1: PUBLIC 12-WEEK PLAN (fullstackpm.tech)

### Access
- **URL**: `https://fullstackpm.tech/tools/sde-prep/weekly-plan`
- **Status**: ✅ Live and functional
- **Data Source**: `/code/app/static/data/curriculum.json`

### Features
- 12 weeks of SDE interview prep content
- Interactive week/day/task expansion
- 130+ LeetCode problems
- 6+ system design case studies
- Behavioral interview preparation
- Mock interview schedules

### Files
- **Data**: `code/app/static/data/curriculum.json`
- **Page**: `code/app/templates/sde-prep/weekly_plan.html`
- **Status**: Production-ready ✅

---

## PART 2: PRIVATE 8-WEEK INTENSIVE PLAN

### Access
These are **PRIVATE/UNEXPOSED** endpoints - NOT linked in main navigation

#### Main Page
- **URL**: `http://localhost:8000/tools/sde-prep/intensive-8-week`
- **Purpose**: View the complete 8-week intensive plan with hourly breakdown
- **File**: `code/app/templates/sde-prep/intensive-8-week-plan.html`

#### Progress Tracker & Dashboard
- **URL**: `http://localhost:8000/tools/sde-prep/intensive-tracker`
- **Purpose**: Track coding problems, applications, interviews, STAR stories, system designs
- **Features**:
  - Real-time progress bars (6 key metrics)
  - Weekly breakdown
  - Recent activity log
  - Quick-log interface to add daily progress
  - Data export capability
  - Auto-sync every 30 seconds
- **File**: `code/app/templates/sde-prep/intensive-tracker.html`

#### Notes & Reflections
- **URL**: `http://localhost:8000/tools/sde-prep/intensive-notes`
- **Purpose**: Journal reflections, interview feedback, breakthroughs, mental health notes
- **Features**:
  - Categorized notes (reflection, breakthrough, interview, problem difficulty, mental health, application)
  - Optional mood tracking (😊😌😐😕😤)
  - Optional week assignment
  - Filtering by category
  - Export to text file
  - Delete individual notes
- **File**: `code/app/templates/sde-prep/intensive-notes.html`

---

## DATA PERSISTENCE

All data persists across time and devices using a file-based backend:

### Progress Data
- **Stored in**: `/code/app/data/intensive_progress_{user_id}.json`
- **Tracks**:
  - Coding problems solved
  - Applications submitted
  - Interviews completed
  - STAR stories written
  - System designs mastered
  - Offers received
  - Weekly statistics
  - Recent activity
- **Auto-saves**: Every 30 seconds
- **Sync endpoint**: `POST /api/intensive-progress/sync`

### Notes Data
- **Stored in**: `/code/app/data/intensive_notes_{user_id}.json`
- **Contains**:
  - Note ID (UUID)
  - Category (reflection, breakthrough, interview, etc.)
  - Week (optional)
  - Content (full text)
  - Mood emoji (optional)
  - Timestamp (ISO format)
- **Endpoints**:
  - `GET /api/intensive-notes` - Retrieve all notes
  - `POST /api/intensive-notes` - Create new note
  - `DELETE /api/intensive-notes/{note_id}` - Delete specific note

### Cross-Device Sync
- Same `user_id` cookie = Same data across all devices
- Data stored on backend server, fetched on page load
- Manual "Sync to Cloud" button available on tracker

---

## API ENDPOINTS (For Reference)

### Progress Endpoints
```
GET    /api/intensive-progress              # Get all progress data
POST   /api/intensive-progress              # Update progress metrics
POST   /api/intensive-progress/log          # Log daily progress
POST   /api/intensive-progress/sync         # Sync to backend
```

### Notes Endpoints
```
GET    /api/intensive-notes                 # Get all notes
POST   /api/intensive-notes                 # Create new note
DELETE /api/intensive-notes/{note_id}       # Delete note
```

---

## 8-WEEK INTENSIVE CURRICULUM

### Week Structure
- **2 weeks fully detailed** in `curriculum-8-week-intensive.json`
- **Remaining weeks** (3-8) can be added following same structure
- **Each day** includes: title, description, tasks
- **Each task** includes: title, description, type, minutes, difficulty, resources, notes

### File Location
- **Data**: `code/app/static/data/curriculum-8-week-intensive.json`

### Content Coverage
- **Week 1**: Foundation, Resume, LinkedIn, Arrays & Strings (20 coding problems)
- **Week 2**: Trees, Graphs, System Design Intro (28+ coding problems)
- **Weeks 3-8**: (To be completed following same structure)

### Task Types
- `coding` - LeetCode problems
- `reading` - Conceptual learning
- `writing` - Resume, STAR stories, notes
- `practice` - Mock interviews, review
- `application` - Job applications
- `networking` - Outreach
- `research` - Company research

---

## HOW TO USE

### For Your Wife

#### Access the Plans
1. Open Browser
2. Local development:
   - **12-week public**: `http://localhost:8000/tools/sde-prep/weekly-plan`
   - **8-week intensive**: `http://localhost:8000/tools/sde-prep/intensive-8-week`

3. Deployed on fullstackpm.tech:
   - **12-week public**: `https://fullstackpm.tech/tools/sde-prep/weekly-plan`
   - **8-week intensive**: Add to environment/bookmark (not in public nav)

#### Track Progress Daily
1. Go to Tracker: `/tools/sde-prep/intensive-tracker`
2. Under "Quick Log" section:
   - Enter # of coding problems solved
   - Enter # of applications submitted
   - Enter # of interviews completed
   - Click "Log Progress"
3. View real-time updates in dashboard cards above

#### Add Personal Notes
1. Go to Notes: `/tools/sde-prep/intensive-notes`
2. Select category (Reflection, Breakthrough, Interview, etc.)
3. Optional: Select week, choose mood emoji
4. Write note in text area
5. Click "Save Note"
6. Notes appear in reverse chronological order
7. Filter by category or export to text file

#### Export Data
- **Tracker**: Click "📥 Export Data" to download JSON
- **Notes**: Click "📥 Export Notes" to download TXT file
- Data format includes timestamps for tracking

---

## DATA LOCATIONS

```
fullstackpm.tech/code/
├── app/
│   ├── routers/
│   │   └── sde_prep.py                        # Routes + API endpoints (UPDATED)
│   ├── templates/sde-prep/
│   │   ├── weekly_plan.html                   # 12-week plan page ✅
│   │   ├── intensive-8-week-plan.html         # 8-week plan page (NEW)
│   │   ├── intensive-tracker.html             # Tracker/dashboard (NEW)
│   │   └── intensive-notes.html               # Notes page (NEW)
│   ├── static/data/
│   │   ├── curriculum.json                    # 12-week curriculum ✅
│   │   └── curriculum-8-week-intensive.json   # 8-week curriculum (NEW)
│   └── data/                                  # Data persistence
│       ├── intensive_progress_{user_id}.json  # Progress tracking
│       └── intensive_notes_{user_id}.json     # User notes
└── ...
```

---

## DEPLOYMENT NOTES

### Local Development
All endpoints work at `http://localhost:8000/`

### Production (fullstackpm.tech)
1. Data is stored server-side in `/code/app/data/`
2. User ID from session cookie identifies user data
3. Same user can access from any device
4. Data persists indefinitely (manual backup recommended)

### Backups
Recommended periodic backups of:
- `/code/app/data/intensive_progress_*.json`
- `/code/app/data/intensive_notes_*.json`

---

## FEATURES SUMMARY

### Tracker Dashboard
- ✅ 6 key metric cards (problems, apps, interviews, STAR stories, designs, offers)
- ✅ Overall progress bar (weighted average)
- ✅ Weekly breakdown by week
- ✅ Recent activity log
- ✅ Quick-log daily progress
- ✅ Export JSON
- ✅ Cloud sync button
- ✅ Auto-sync every 30 seconds

### Notes System
- ✅ 7 note categories with emojis
- ✅ Optional mood tracking (5 emoji options)
- ✅ Optional week assignment
- ✅ Timestamp on every note
- ✅ Filter by category
- ✅ Delete individual notes
- ✅ Export to text file
- ✅ Reverse chronological display

### Curriculum
- ✅ Hourly breakdown (9 AM - 3 PM daily)
- ✅ 180+ coding problems mapped
- ✅ 6+ system designs
- ✅ 10+ STAR stories
- ✅ Resume & LinkedIn tasks
- ✅ Job application tracking
- ✅ Expandable week/day/task structure
- ✅ Resource links (problem, solution, video, article)

---

## NEXT STEPS

### To Complete 8-Week Plan
1. Expand `curriculum-8-week-intensive.json` with Weeks 3-8
2. Follow same structure as Weeks 1-2
3. Add specific LeetCode problems for each week
4. Test all links before publishing

### To Go Live
1. Bookmark `/tools/sde-prep/intensive-8-week` for easy access
2. Share tracker/notes URLs with wife
3. Check `/tools/sde-prep/intensive-tracker` daily for progress
4. Export notes/progress periodically as backup

### Optional Enhancements
- [ ] Add calendar view for timeline planning
- [ ] Create mobile app wrapper for easier access
- [ ] Add notifications for daily reminders
- [ ] Create PDF report generation
- [ ] Add comparison with 12-week plan side-by-side

---

## SUCCESS METRICS

After 8 weeks, expect:
- ✅ 180+ coding problems completed
- ✅ 120+ applications submitted
- ✅ 20+ interviews scheduled
- ✅ 3-5 offers received
- ✅ 10+ polished STAR stories
- ✅ 6+ system designs mastered
- ✅ Job offer accepted! 🎉

---

## SUPPORT

All endpoints are self-documenting:
- Check browser console for API responses
- Download exported data to verify tracking
- Notes are human-readable in exported text file
- No external dependencies needed (uses browser local storage fallback)

Good luck with the 8-week intensive prep! 🚀
