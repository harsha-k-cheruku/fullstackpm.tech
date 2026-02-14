# Handoff Instructions

## What You're Asking the Other LLM to Do

Generate BUILD_02 through BUILD_08 for the PM Interview Coach project.

## Exact Prompt to Give the Other LLM

Copy-paste this into GPT-4, Gemini, Claude (web), or any other LLM:

---

**PROMPT START:**

I need you to generate 7 build instruction files for a PM Interview Coach project.

First, read these files in this exact order:

1. `/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/INSTRUCTIONS_FOR_LLM.md` - Your detailed instructions
2. `/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/FRAMEWORK_STRATEGY_TO_TASKS.md` - The template framework
3. `/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/02_PM_INTERVIEW_COACH.md` - Product strategy
4. `/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/BUILD_01_DATABASE_MODELS.md` - Reference example showing the exact format
5. `/Users/sidc/Projects/claude_code/fullstackpm.tech/code/app/static/css/custom.css` - Design system

After reading all 5 files carefully, generate these 7 files in the folder `/Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/`:

- `BUILD_02_BASE_TEMPLATES.md`
- `BUILD_03_QUESTION_LOADER.md`
- `BUILD_04_AI_EVALUATOR.md`
- `BUILD_05_PRACTICE_UI.md`
- `BUILD_06_LANDING_HISTORY.md`
- `BUILD_07_PROGRESS_DASHBOARD.md`
- `BUILD_08_HTMX_INTERACTIONS.md`

Each file MUST follow the exact same 8-section structure as BUILD_01. Study BUILD_01 carefully - match its format, tone, and level of detail.

Start with BUILD_02 and work through BUILD_08 in order. Generate all 7 files in a single response.

**PROMPT END**

---

## Alternative: One-at-a-Time Approach

If the LLM can't handle all 7 at once, ask it to generate them one at a time:

**For each task, give this prompt:**

```
Read these files:
1. /Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/INSTRUCTIONS_FOR_LLM.md
2. /Users/sidc/Projects/claude_code/fullstackpm.tech/strategy/build_tasks/pm_interview_coach/BUILD_01_DATABASE_MODELS.md

Then generate BUILD_0X_[NAME].md following the exact same format as BUILD_01.

[Paste the specific task details from INSTRUCTIONS_FOR_LLM.md for that task]
```

## What to Do with the Output

1. **Save each BUILD file** to the paths specified
2. **Send them back to Claude Code** for validation
3. I'll review each file and tell you:
   - Quality score (1-10)
   - What's missing or wrong
   - Which files are ready to use
   - Which need fixes

## Files Already Created ✅

- ✅ `README.md` - Task list and dependency graph
- ✅ `INSTRUCTIONS_FOR_LLM.md` - Detailed instructions for the other LLM
- ✅ `BUILD_01_DATABASE_MODELS.md` - Reference example (1000+ lines)
- ✅ `HANDOFF_TO_OTHER_LLM.md` - This file

## Files Needed ❌

- ❌ `BUILD_02_BASE_TEMPLATES.md`
- ❌ `BUILD_03_QUESTION_LOADER.md`
- ❌ `BUILD_04_AI_EVALUATOR.md`
- ❌ `BUILD_05_PRACTICE_UI.md`
- ❌ `BUILD_06_LANDING_HISTORY.md`
- ❌ `BUILD_07_PROGRESS_DASHBOARD.md`
- ❌ `BUILD_08_HTMX_INTERACTIONS.md`

## Expected File Sizes

- BUILD_02: ~400-500 lines
- BUILD_03: ~600-700 lines
- BUILD_04: ~900-1000 lines (most complex)
- BUILD_05: ~1000-1200 lines (most complex)
- BUILD_06: ~800-900 lines
- BUILD_07: ~900-1000 lines
- BUILD_08: ~700-800 lines

**Total:** ~6,000 lines across 7 files

## Token Estimate

If using GPT-4 or Claude (web):
- Input: ~15k tokens (reading all reference files)
- Output: ~40k tokens (generating 7 files)
- Total: ~55k tokens per attempt

If the LLM has a 128k context window, it should handle this in one shot.

## Quality Checks I'll Do

When you send the files back, I'll check:
1. All 8 sections present in correct order ✓
2. Color system pasted inline (not referenced) ✓
3. Typography pasted inline ✓
4. All referenced files included with full text ✓
5. Acceptance tests are concrete and runnable ✓
6. No external dependencies (React, npm, etc.) ✓
7. File paths match project structure ✓
8. Self-contained (no "see Task X" references) ✓

I'll give each file a score and tell you which ones are ready to hand to developers.

## Next Step

Copy the prompt above and paste it into your preferred LLM. Then send me the generated files for validation.
