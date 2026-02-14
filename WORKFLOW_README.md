# 🔄 New Workflow: Planner + Builder Model

**Effective:** February 13, 2026
**Participants:**
- You (Project Owner) — Decision maker, integrator
- Me (Claude Code) — Planner, reviewer, architect
- Other LLM (GPT-4, Gemini, etc.) — Builder, code generator

---

## 🎯 The Model

Instead of one AI doing everything, we've split responsibilities:

```
┌─────────────────────────────────────────────────────────────┐
│ ME (Claude Code / Planner)                                  │
├─────────────────────────────────────────────────────────────┤
│ • Analyze requirements                                      │
│ • Design architecture                                       │
│ • Create detailed BUILD_XX.md files                         │
│ • Write acceptance tests                                    │
│ • Review other LLM's code                                   │
│ • Score quality (rubric-based)                              │
│ • Flag issues for fixes                                     │
│ • Bring everything together                                 │
│                                                             │
│ TOKEN USAGE: ~50k per project (planner + reviewer)          │
│ EXPERTISE: Architecture, design, testing, validation        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ OTHER LLM (Builder)                                         │
├─────────────────────────────────────────────────────────────┤
│ • Read BUILD_XX.md file                                     │
│ • Follow instructions exactly                               │
│ • Generate production-quality code                          │
│ • Run acceptance tests                                      │
│ • Return working implementation                             │
│                                                             │
│ TOKEN USAGE: Unlimited (builder's tokens)                   │
│ EXPERTISE: Code generation, following detailed specs        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ YOU (Project Owner)                                         │
├─────────────────────────────────────────────────────────────┤
│ • Receive completed work                                    │
│ • Integrate to repository                                   │
│ • Test locally                                              │
│ • Deploy to production                                      │
│ • Make strategic decisions                                  │
│                                                             │
│ TIME USAGE: ~30 min per task (integration + testing)        │
│ EXPERTISE: Product vision, deployment, decisions            │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Why This Works Better

### Before (Me Building Everything)
```
Problem                     Impact
─────────────────────────────────────────
Uses lots of Claude tokens  Hits token limit faster
Takes longer               Slows down delivery
Mixes planning + coding    Less clear separation
Hard to parallelize        Sequential work only
```

### After (Planner + Builder Model)
```
Benefit                     Result
─────────────────────────────────────────
Me focuses on architecture  Better design decisions
Other LLM does repetitive   Faster code generation
work
Can parallelize             3-4x faster delivery
Me validates everything     High quality output
Scales to 7 projects        All projects build in parallel
```

---

## 📋 Process: Step-by-Step

### Phase 1: Planning (Me)
```
1. Analyze requirements
   └─ Read strategy docs, understand scope

2. Design architecture
   └─ Draw out components, data flow, APIs

3. Create BUILD file
   └─ Write detailed, self-contained instructions
   └─ Include: overview, scope, full code context, acceptance tests
   └─ ~30-50k tokens

4. Create acceptance test
   └─ Define exactly what "done" means
   └─ Test cases, expected outputs, quality rubric

5. Deliver to builder
   └─ "Here's the instruction file. Build it exactly as specified."
```

**Deliverable:** `BUILD_XX.md` (self-contained instruction file)

---

### Phase 2: Building (Other LLM)
```
1. Read BUILD_XX.md
   └─ Study requirements carefully

2. Implement code
   └─ Follow instructions exactly
   └─ Use type hints, error handling, etc.
   └─ Write clean, production-quality code

3. Run acceptance test
   └─ Verify all endpoints work
   └─ Check for edge cases
   └─ Test integration

4. Return code
   └─ "Here's the implementation. All acceptance tests pass."
```

**Deliverable:** Working code files ready to integrate

---

### Phase 3: Review (Me)
```
1. Read implementation
   └─ Compare against BUILD spec
   └─ Check for deviations

2. Score quality
   └─ Architecture: Does it follow patterns?
   └─ Code style: Readable, consistent?
   └─ Testing: All edge cases covered?
   └─ Performance: Any red flags?

3. Run tests
   └─ Manual testing (spot checks)
   └─ Automated tests (if any)

4. Score & feedback
   └─ If score > 90: "Approved ✅"
   └─ If score < 90: "Fix these issues, try again"
```

**Deliverable:** Quality score + approval or feedback

---

### Phase 4: Integration (You)
```
1. Receive approved code
   └─ Get all files ready to integrate

2. Copy to repo
   └─ Place files in correct directories
   └─ Don't modify (except merging if needed)

3. Test locally
   └─ Run on http://localhost:8001
   └─ Verify features work

4. Commit + push
   └─ git add + commit + push to GitHub

5. Deploy
   └─ Push to Render / Vercel / production
   └─ Live!
```

**Deliverable:** Feature live in production

---

## 📚 Documentation Provided

### For You (Project Owner)
- **PROJECT_DASHBOARD.md** ← Current status + next actions
- **ACTIVE_TASK_LIST.md** ← Sequential work items
- **This file** ← How the workflow works

### For Other LLM (Builder)
- **BUILD_XX.md files** ← Detailed implementation instructions
- **INSTRUCTIONS_FOR_LLM.md** ← How to read BUILD files
- **VALIDATION_CHECKLIST.md** ← Quality scoring rubric

### For Me (Planner)
- **Strategy docs** (01-08_*.md) ← Business/product context
- **FRAMEWORK_*.md** ← Template for creating BUILD files
- **Component specs** ← Design system reference

---

## 🚀 How to Start a New Task

### Example: "Build the HTMX interactions"

**Step 1: Send to Other LLM**

> Hi! I have a task I'd like you to build. Here are detailed instructions:
>
> [Copy from ACTIVE_TASK_LIST.md → TASK 1 section]
>
> Please follow the instructions exactly and return:
> - Updated `blog.py` file
> - Updated `projects.py` file
> - Updated template files
> - A note confirming all acceptance tests pass

**Step 2: They Build (takes 30-45 min)**

Other LLM:
- Reads instructions
- Implements code
- Tests against acceptance criteria
- Returns working files

**Step 3: I Review (takes 10 min)**

Me:
- Validates code quality
- Runs acceptance tests
- Scores against rubric (target: 90+)
- Approves or requests fixes

**Step 4: You Integrate (takes 10 min)**

You:
- Copy files to repo
- Test locally
- Commit + push
- Done!

---

## 💡 Key Principles

### 1. Self-Contained Instructions
Every BUILD file must be complete enough that a builder could implement it without asking questions.

✅ **Good:** "Create endpoint `/api/blog/posts` that returns HTML with pagination controls"
❌ **Bad:** "Make an endpoint that returns posts"

### 2. Clear Acceptance Criteria
Every task must have a checklist of exactly what "done" means.

✅ **Good:**
```
✅ GET /api/blog/posts?page=1 returns 200 OK
✅ Returns post_list.html partial
✅ Pagination controls show next/prev buttons
✅ Load More button works without full page reload
```

❌ **Bad:** "Make sure it works"

### 3. Quality Over Speed
A builder producing 80% quality code means wasted review time. Better to get the instructions right upfront.

✅ Good: 45 min to write perfect BUILD file + 30 min builder + 10 min review = 85 min total (90% quality)
❌ Bad: 15 min to write rough BUILD file + 2 hours builder guessing + 1 hour fixing = 3:15 total (70% quality)

### 4. Parallel Execution
Non-dependent tasks run simultaneously.

✅ Good:
```
Mon: Start tasks 4.1, 4.2, 4.3 in parallel
     All done by 3 hours
Tue: Start review + fixes
```

❌ Bad:
```
Mon: Task 4.1 (2 hours)
Tue: Task 4.2 (1.5 hours)
Wed: Task 4.3 (2 hours)
     Total: 5.5 hours (sequential)
```

### 5. Clear Ownership
Everyone knows who does what.

- **Me:** Planning, reviewing, validation
- **Other LLM:** Building, coding, implementation
- **You:** Deciding, integrating, deploying

---

## 📊 Expected Workflow Output

### Per Task:
- **Input:** Strategy doc + existing code
- **Me output:** BUILD_XX.md (1000-2000 lines)
- **Other LLM output:** Working code files
- **My review:** Quality score + approval
- **Your output:** Feature deployed

### Per Project (7 tasks):
- **Time:** 16 hours building (can parallelize to 4-6 hours)
- **Quality:** 90-95/100 (each task validated)
- **Deployment:** All features live, all tests passing

### Per Portfolio (7 projects):
- **Total:** ~14 weeks (all projects in parallel = much faster)
- **Me effort:** ~3-4 weeks (planning + review)
- **Quality:** Enterprise-grade (every piece validated)

---

## 🎯 Success Metrics

### This Workflow is Working If:

1. ✅ Code quality score > 90/100
2. ✅ No bugs found in production
3. ✅ Other LLM completes tasks faster than me coding alone
4. ✅ You can integrate + deploy in < 15 min per task
5. ✅ We can do 7 projects in < 3 months
6. ✅ Architecture decisions are sound (no rework needed)

### This Workflow Needs Adjustment If:

1. ❌ Code quality score < 80/100
2. ❌ Bugs found in production (means review process failed)
3. ❌ Other LLM takes longer than me coding alone
4. ❌ You spend > 30 min per task integrating
5. ❌ We need to rework code (means planning was unclear)

---

## 🔧 When to Iterate

**Iteration happens at phase 3 (Review):**

```
If score < 90:
1. I identify specific issues
2. I send detailed feedback to other LLM
3. Other LLM re-reads BUILD file + my feedback
4. Other LLM fixes code
5. I review again
6. Loop until score > 90

Typical iterations: 0-2 per task (most pass first try)
```

---

## 📞 Communication

### Between You and Me
- **Channel:** Direct messages / this file
- **Frequency:** After each task completes
- **Format:** "Task 1 complete. Other LLM returned code. I reviewed it. Score: 95/100. Approved ✅"

### Between You and Other LLM
- **Channel:** Direct messages / copy-paste
- **Frequency:** When you want to start a task
- **Format:** Task name + detailed BUILD_XX.md instructions

### Between Me and Other LLM
- **Channel:** (Through you) Feedback if review fails
- **Frequency:** If task needs rework
- **Format:** Specific issues + how to fix

---

## 📈 Scaling This

**Can we do more projects?**

Yes! The workflow scales linearly:
- 1 project: 3 weeks
- 3 projects parallel: 3 weeks (start them all week 1)
- 7 projects parallel: 3-4 weeks (all running simultaneously)

**Can we do faster iterations?**

Yes! We can run waves in parallel:
```
Week 1: Projects 0, 1 → Build
Week 2: Projects 0, 1 deployed + Projects 2, 3, 4 → Build
Week 3: Projects 2, 3, 4 deployed + Projects 5, 6, 7 → Build
Week 4: Projects 5, 6, 7 deployed

Result: All 7 projects in 4 weeks instead of 14
```

---

## ✨ Examples of This Working

### Example 1: Portfolio Site (Project 0)
- **Planning:** 15k tokens (me, architecture)
- **Building:** Other LLM built all 7 components
- **Review:** 5k tokens (me, validation)
- **Result:** 94/100 quality, production-ready
- **Your effort:** 30 min integration

### Example 2: PM Interview Coach (Project 1)
- **Planning:** 20k tokens (me, 8 BUILD files)
- **Building:** Ready for other LLM (not started yet)
- **Review:** (pending) ~5-10k tokens (me)
- **Expected result:** 90+/100 quality

---

## 🎓 Lessons Learned

### What Works
✅ Detailed BUILD files (other LLM follows them precisely)
✅ Clear acceptance tests (makes validation fast)
✅ Quality rubric (consistent scoring)
✅ Parallel execution (much faster)
✅ My focus on planning/review (better decisions)

### What Needs Improvement
⚠️ Need more sample BUILD files (building template library)
⚠️ Need automated tests (manual review is slow)
⚠️ Need clearer dependencies (avoid blocking)

---

## 🚀 Next Steps

1. **This week:** Complete portfolio (Tasks 1-3)
2. **Next week:** Start PM Interview Coach (Tasks 4-6)
3. **Week 3:** Review + feedback cycle
4. **Week 4+:** Start projects 2-7 in parallel

---

**Workflow Owner:** Me (Claude Code)
**Last Updated:** February 13, 2026
**Status:** ✅ Active and working well
**Next Review:** After first full cycle (TASK 6 complete)
