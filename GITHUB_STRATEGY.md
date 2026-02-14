# GitHub Strategy: Projects + Personal Brand

**Goal:** Each project is discoverable + forkable + contributable

---

## 🏗️ Repository Structure

### Main Repos

You'll have **8 GitHub repositories:**

```
1. fullstackpm.tech (Main Portfolio Site)
   ├─ Live at: fullstackpm.tech
   ├─ Contains: All projects + blog + portfolio
   ├─ Language: Python/FastAPI + HTML/CSS
   ├─ Stars target: 1000+
   └─ Use: Main showcase + hub

2. pm-interview-coach (Standalone)
   ├─ Live at: fullstackpm.tech/tools/coach
   ├─ GitHub: [Standalone repo]
   ├─ Language: Python/FastAPI
   ├─ Stars target: 500+
   ├─ Use: Standalone tool (can be run locally)
   └─ Readme: How to run locally

3. pm-toolkit (Standalone)
   ├─ Live at: fullstackpm.tech/tools/toolkit
   ├─ GitHub: [Standalone repo]
   └─ ...

4. ab-test-analyzer (Standalone)
   ├─ Live at: fullstackpm.tech/tools/analyzer
   ├─ GitHub: [Standalone repo]
   └─ ...

5. ai-decision-system (Standalone)
6. pm-marketplace-dashboard (Standalone)
7. llm-prompt-evaluator (Standalone)
8. ai-bootcamp-case-study (Standalone)
```

### Architecture Decision

**Why two repos per project?**

```
Option A: Everything in one repo (fullstackpm.tech)
├─ PROs: Easier to manage, single deployment
├─ CONs: Hard to fork, can't use standalone, loses visibility

Option B: Standalone + integrated (RECOMMENDED)
├─ Main repo (fullstackpm.tech) - everything integrated
├─ Standalone repos - can fork/use independently
├─ CONs: Requires some duplication (minimal)
├─ PROs: Better visibility, fork-friendly, modular
```

**We choose Option B because:**
✅ Users can fork individual tools
✅ Better GitHub visibility (multiple repos)
✅ Can be used standalone or integrated
✅ Contributors can work on specific projects
✅ Each tool can have its own release cycle

---

## 📁 Standalone Repo Structure

### Example: pm-interview-coach

```
pm-interview-coach/
├─ README.md
├─ GETTING_STARTED.md
├─ requirements.txt
├─ .env.example
├─ docker-compose.yml (optional)
│
├─ app/
│  ├─ main.py
│  ├─ config.py
│  ├─ models.py
│  ├─ database.py
│  ├─ routers/
│  │  ├─ __init__.py
│  │  └─ coach.py
│  ├─ services/
│  │  ├─ __init__.py
│  │  └─ coach_service.py
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ practice.html
│  │  ├─ history.html
│  │  └─ dashboard.html
│  └─ static/
│     ├─ css/
│     │  └─ coach.css
│     └─ js/
│        └─ coach.js
│
├─ questions/
│  ├─ sample_questions.json
│  └─ QUESTIONS_FORMAT.md
│
├─ tests/
│  ├─ test_models.py
│  ├─ test_coach_service.py
│  └─ test_routes.py
│
├─ docs/
│  ├─ ARCHITECTURE.md
│  ├─ API.md
│  ├─ DEPLOYMENT.md
│  └─ CONTRIBUTING.md
│
├─ .github/
│  ├─ workflows/
│  │  ├─ test.yml (run tests on PR)
│  │  └─ deploy.yml (deploy on merge)
│  └─ issue_templates/
│     ├─ bug_report.md
│     └─ feature_request.md
│
├─ LICENSE (MIT)
└─ .gitignore
```

---

## 📝 README.md Template

### For Each Standalone Project

```markdown
# PM Interview Coach

AI-powered interview practice for product managers.

**Try it live:** [fullstackpm.tech/tools/coach](https://fullstackpm.tech/tools/coach)

## Features

- 💡 Practice with realistic PM interview questions
- 🤖 AI feedback on your answers
- 📊 Track improvement over time
- 🔄 Review past practice sessions

## Quick Start

### Option 1: Try Online (Recommended)
Visit [fullstackpm.tech/tools/coach](https://fullstackpm.tech/tools/coach)

### Option 2: Run Locally

**Prerequisites:**
- Python 3.11+
- SQLite3

**Installation:**
```bash
git clone https://github.com/YOUR_USERNAME/pm-interview-coach.git
cd pm-interview-coach
pip install -r requirements.txt
```

**Setup:**
```bash
# Create environment file
cp .env.example .env

# Edit .env and add your Claude API key
# ANTHROPIC_API_KEY=sk-...
```

**Run:**
```bash
uvicorn app.main:app --reload
# Visit http://localhost:8000
```

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for technical details.

## API

See [API.md](docs/API.md) for endpoint documentation.

## How This Was Built

Read the blog posts:
- [How I Built the PM Interview Coach](https://fullstackpm.tech/blog/how-i-built-pm-coach)
- [Lessons Learned](https://fullstackpm.tech/blog/pm-coach-lessons-learned)

## Deployment

**This tool is already deployed at:** fullstackpm.tech/tools/coach

To deploy your own instance, see [DEPLOYMENT.md](docs/DEPLOYMENT.md)

## Contributing

Want to contribute? See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

Ideas:
- [ ] Add more question types
- [ ] Support for practice with templates
- [ ] Export results as PDF
- [ ] Team features
- [ ] Integration with Slack

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Jinja2 + HTMX
- **AI:** Anthropic Claude API
- **Database:** SQLite
- **Styling:** Tailwind CSS

## License

MIT License - see [LICENSE](LICENSE)

## Author

[Your name](https://twitter.com/yourhandle)
Building PM tools in public 🚀

## Support

- 🐛 Found a bug? [Create an issue](https://github.com/YOUR_USERNAME/pm-interview-coach/issues)
- 💡 Have an idea? [Start a discussion](https://github.com/YOUR_USERNAME/pm-interview-coach/discussions)
- ❓ Questions? [Email me](mailto:your@email.com)

---

**Want similar built for your team?**
I'm available for consulting: [Get in touch](https://fullstackpm.tech/contact)
```

---

## 🔗 Linking Repos Together

### In Main Site Repo (fullstackpm.tech)

**In project page, link to GitHub:**

```html
<!-- templates/projects/detail.html -->

<div class="project-links">
  <a href="https://github.com/YOUR_USERNAME/pm-interview-coach"
     class="btn btn-secondary" target="_blank">
    View Source on GitHub ⭐
  </a>
  <a href="/tools/coach" class="btn btn-primary">
    Try It Now →
  </a>
</div>
```

### In Standalone Repos

**Link back to main site:**

```markdown
<!-- README.md -->

**This is part of:** [fullstackpm.tech](https://fullstackpm.tech) - A collection of PM tools

**All 7 tools:**
- [PM Interview Coach](https://fullstackpm.tech/tools/coach)
- [PM Toolkit](https://fullstackpm.tech/tools/toolkit)
- [A/B Test Analyzer](https://fullstackpm.tech/tools/analyzer)
- ... (and 4 more)

**See all repos:** [github.com/YOUR_USERNAME](https://github.com/YOUR_USERNAME)
```

---

## ⭐ GitHub Discovery

### How People Find Your Projects

**Discovery Paths:**

```
Path 1: fullstackpm.tech
└─ User visits main site
└─ Sees "View Source" button
└─ Clicks → lands on GitHub repo

Path 2: Browsing GitHub
└─ Search: "PM Interview Tool"
└─ Find repo: pm-interview-coach
└─ Click → GitHub repo
└─ See "Try online" link → back to site

Path 3: Twitter/Social
└─ See: "Built a PM coach with 100 stars"
└─ Search on GitHub
└─ Find repo

Path 4: ProductHunt/HackerNews
└─ Discover project on PH/HN
└─ Click → fullstackpm.tech
└─ "View Source" → GitHub
```

### Optimizing for Discovery

**GitHub Profile:**
```
Name: [Your Name]
Bio: "Building PM tools in public.
     7 tools, 1 mission: Help PMs think strategically.
     Check out my projects →"
Website: https://fullstackpm.tech
```

**README Badges:**
```markdown
# pm-interview-coach

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/pm-interview-coach?style=social)](https://github.com/YOUR_USERNAME/pm-interview-coach)

[Live Demo](https://fullstackpm.tech/tools/coach) •
[Blog Post](https://fullstackpm.tech/blog/how-i-built-pm-coach) •
[Docs](docs/) •
[Contributing](CONTRIBUTING.md)
```

---

## 📊 Syncing Between Repos

### Synchronization Strategy

**Question:** How do we keep code in sync (standalone repo + main site)?

**Answer:** Use Git subtrees or Git submodules

**Option A: Subtree (Recommended)**
```bash
# In fullstackpm.tech repo
git subtree add --prefix=app/projects/pm_interview_coach \
  https://github.com/YOUR_USERNAME/pm-interview-coach.git main --squash

# To pull updates
git subtree pull --prefix=app/projects/pm_interview_coach \
  https://github.com/YOUR_USERNAME/pm-interview-coach.git main --squash

# To push updates
git subtree push --prefix=app/projects/pm_interview_coach \
  https://github.com/YOUR_USERNAME/pm-interview-coach.git main
```

**Option B: Submodules**
```bash
# Add as submodule
git submodule add https://github.com/YOUR_USERNAME/pm-interview-coach.git \
  app/projects/pm_interview_coach
```

**Option C: Separate (Simpler)**
- Main repo (fullstackpm.tech) - integrated version
- Standalone repo - same code, can be run independently
- Manual sync when making changes (use git cherry-pick or manually copy)

**Recommendation:** Use Option C (Separate) for simplicity
- Easier to manage
- Standalone can evolve independently
- Both stay up to date manually

---

## 🚀 GitHub Actions Workflows

### For Each Standalone Repo

**File: `.github/workflows/test.yml`**
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

**File: `.github/workflows/deploy.yml`**
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## 📈 GitHub Growth Strategy

### Phases

**Phase 1: Foundation (Month 1)**
- 1 project repo (PM Coach)
- Main site repo
- Goal: 50 stars total

**Phase 2: Growth (Month 2-3)**
- 3 more projects live
- More GitHub activity
- Goal: 300 stars total

**Phase 3: Authority (Month 4-6)**
- 7 projects live
- Community contributions
- Goal: 1000+ stars total

### Getting Stars

✅ **Tactics:**
- Share on Twitter when launching
- Submit to ProductHunt
- Post on Reddit (/r/productmanagement, /r/programming)
- HackerNews (if relevant)
- Blog post in dev communities
- Include in "Awesome PM Tools" lists

✅ **Make it star-worthy:**
- Good README (people should understand instantly)
- Live demo link (clicking "Try Now" is easier than installing)
- Clear value prop (what problem does it solve?)
- Good docs (ARCHITECTURE.md, etc.)
- MIT license (people like open source)
- Active maintenance (respond to issues)

---

## 📝 Documentation in Each Repo

### Every standalone repo should have

```
docs/
├─ ARCHITECTURE.md
│  └─ How the tool works, design decisions
│
├─ API.md
│  └─ Full API documentation
│
├─ DEPLOYMENT.md
│  └─ How to deploy to production
│
├─ CONTRIBUTING.md
│  └─ How to contribute
│
└─ FAQ.md
   └─ Common questions
```

---

## 🔗 Example: Full Flow

### User discovers your work

```
1. User sees your tweet:
   "Built a PM Interview Coach with Claude API
    Try it: fullstackpm.tech/tools/coach
    Source: [link to GitHub]"

2. User visits fullstackpm.tech/tools/coach
   └─ Tries the tool
   └─ Gets impressed

3. User clicks "View Source on GitHub"
   └─ Lands on pm-interview-coach repo
   └─ Reads README + docs
   └─ Sees quality code + architecture

4. User clicks "How I Built This" blog link
   └─ Reads technical deep dive
   └─ Sees your thinking process

5. User is now a fan
   └─ Stars the repo
   └─ Follows on Twitter
   └─ Watches for future projects

6. (Optional) Later: User has similar problem
   └─ Remembers your work
   └─ Reaches out: "Can you build X for us?"
   └─ Consulting project starts
```

---

## ✅ Checklist: GitHub Setup

### For Main Site Repo (fullstackpm.tech)

- [ ] Repository created
- [ ] README with live link
- [ ] License (MIT)
- [ ] GitHub Actions (tests)
- [ ] Issues/discussions enabled
- [ ] Badges added
- [ ] GitHub profile links back

### For Each Standalone Repo

- [ ] Repository created
- [ ] Good README (with "Try online" link)
- [ ] ARCHITECTURE.md documented
- [ ] API.md documented
- [ ] DEPLOYMENT.md documented
- [ ] CONTRIBUTING.md documented
- [ ] License (MIT)
- [ ] GitHub Actions (tests)
- [ ] Badges added
- [ ] Link back to main site in README

---

## 💡 Git Workflow

### Day-to-Day

**You work locally:**
```bash
# Clone main site
git clone https://github.com/YOUR_USERNAME/fullstackpm.tech.git
cd fullstackpm.tech

# Create feature branch
git checkout -b feature/pm-coach

# Code Puppy implements, you integrate
# ... files copied to repo ...

# Commit
git add .
git commit -m "feat: Add PM Interview Coach endpoints"

# Push to GitHub
git push origin feature/pm-coach

# Create PR on GitHub
# ... review + merge ...

# Deploy to production
# (trigger on merge to main)
```

**For standalone repos:**
```bash
# Clone
git clone https://github.com/YOUR_USERNAME/pm-interview-coach.git
cd pm-interview-coach

# Sync with main site changes
# (manual: copy updated files)

# Commit
git add .
git commit -m "sync: Update from main site"

# Push
git push origin main
```

---

## 🎯 Success Metrics

**GitHub metrics showing this is working:**

✅ 1000+ stars across all repos
✅ 50+ forks (people using your code)
✅ 20+ PRs from community
✅ GitHub trending (for new projects)
✅ Featured on GitHub (if lucky)

**Brand metrics:**

✅ 5000+ followers on social
✅ High click-through from GitHub to site
✅ Consulting inquiries from GitHub visitors
✅ Speaking/sponsorship opportunities
✅ Featured in PM communities

---

**Status:** ✅ Strategy ready to execute
**Next:** Set up repos as you ship projects
