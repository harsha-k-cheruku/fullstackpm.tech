# Product Deep Dive Plan: Onboarding & Activation

**For:** Code Puppy | **Status:** Ready to implement | **Complexity:** Medium | **Build time:** 2 hours

---

## Quick Reference

**Q1 Analogy:** "The tour guide for your first visit."

**Q2 Mechanism:**
```
User Arrives → Welcome Flow → Feature Walkthrough → First Action → Habit Formation → Retention
```

**Q3 Cross-Model Variation:**

| Dimension | Social (Twitter) | SaaS (Slack) | Mobile (Uber) | Web (Figma) | Fintech (Wise) |
|-----------|-----------------|--------------|---------------|-------------|---|
| **Activation metric** | First tweet / first follow | First message sent | First ride completed | First design file created | First transfer completed |
| **Time-to-activation** | 5 min ideal | 30 min | 10 min | 15 min | 30 min (KYC) |
| **Onboarding friction** | Low (skip possible) | Medium (team import) | Medium (payment method) | High (software learning) | EXTREME (KYC/verification) |
| **Drop-off rate** | 40-60% after signup | 30-50% | 50-70% | 20-30% | 10-20% (mandatory) |
| **Retention driver** | Follower count, feeds | Team collaboration | Ride frequency | Project complexity | Transfer success |
| **Critical mass threshold** | 50 follows to get feed value | 3+ team members to use async chat | 1 ride to understand value | 1 project to see value | 1 successful transfer |
| **Recovery tactic** | Re-engagement campaigns (email) | Team admin reminders | Promo codes ($5 credit) | In-app tutorials | Email reminders |

**Q4 Metrics:**
- Sign-up to activation rate (% of users who complete activation)
- Time-to-activation (hours from signup to first action)
- Day-1 retention (% of activated users active on day 1)
- Day-7 retention (% who return on day 7)
- Onboarding completion rate (% who finish full tutorial)
- Activation funnel drop-off (where do users leave?)

**Q5 Hard Problems:**
1. **Pogo-sticking** — Users activate, try feature, don't see value, leave. How to show value faster?
2. **Feature overload** — Showing every feature = paralysis. What to show first?
3. **Motivation mismatch** — Why did user signup? Onboarding assumes motivation. Wrong assumption = dropout.
4. **Network effects** — User needs others on platform (Twitter needs followers). How to bootstrap without critical mass?
5. **Friction vs disclosure** — More onboarding = better informed but higher dropout. Less onboarding = faster activation but confused users.
6. **Mobile vs Web** — Different context, different friction points. Mobile = interrupt-driven, web = time-rich.

---

## Content Summary

### Section 1: What & Why
- Opening: "The tour guide for your first visit."
- Goal: Get users to their first "aha moment" (moment they realize value)
- Path: Signup → Welcome → Feature walkthrough → First action → habit
- Callout: "The user who doesn't activate on day 1 is gone. Day-1 retention is THE metric."

### Section 2: How It Works (7-node flow)
1. Signup (email/password/social)
2. Welcome screen (set expectations, explain value)
3. Profile setup (name, photo, preferences)
4. Feature walkthrough (highlight 1-3 key features)
5. Guided first action (hand-hold through first real task)
6. Celebration moment (success! show progress)
7. Re-engagement loop (email, notifications, prompts to return)

### Section 3: Across Business Models
- 5-column table above
- Callout: "Fintech needs KYC (painful but mandatory). Mobile apps need payment method early (friction). SaaS needs team setup (blocker for value)."

### Section 4: Metrics (8 cards)
1. **Sign-up to Activation Rate** — % of signups who take first action. Benchmark: 40-80% depending on friction
2. **Time-to-Activation** — Hours from signup to first action. Benchmark: varies (Twitter 5min, Slack 30min, Wise 2 hours)
3. **Onboarding Completion Rate** — % of users who finish full tutorial. Benchmark: 30-70%
4. **Day-1 Retention** — % of activated users active on day 1. Benchmark: 80-95% (for most, day 1 = signup day)
5. **Day-7 Retention** — % of users active 7 days after signup. Benchmark: 30-60% depending on product
6. **Day-30 Retention** — % active 30 days after signup. Benchmark: 10-40%
7. **Activation Funnel Drop-off** — Where do users leave? Benchmark: track each step
8. **Re-engagement Campaign Effectiveness** — % of dormant users who return after email. Benchmark: 5-15% click rate

### Section 5: Architecture (4 layers)
1. **User Onboarding Flow** — Signup form, email verification, welcome screen templates
2. **Profile & Setup** — Profile form, preference collection, integration setup (for SaaS)
3. **Feature Education** — Tooltips, guided tours (overlay), video tutorials, help docs
4. **Activation Tracking** — Event tracking (which step reached), funnel analytics, re-engagement triggers

### Section 6: Challenges (6 cards)
1. **High Dropout Rate** — 40-60% dropout before activation. Solution: Simplify flow, reduce required fields, make value clear earlier
2. **Feature Overload Paralysis** — Too many features = confusion. Solution: Highlight 2-3 core features only, advanced features hidden
3. **Motivation Mismatch** — User signed up for wrong reason. Solution: Ask motivation in signup ("Why are you here?"), personalize flow
4. **Network Effects Chicken-Egg** — Need others to see value. Solution: Demo accounts, artificial followers, or async-first (email/messaging)
5. **Re-engagement Difficulty** — User activates but doesn't return. Solution: Email drip campaigns, push notifications, show progress
6. **Mobile vs Web Differences** — Mobile context is different (app store, interruptions). Solution: Separate onboarding flows, mobile-optimized

### Section 7: Patterns (4 companies)
1. **Slack** — Team-focused: workspace creation → invite team → first channel/message. Heavy on collaboration, not individual value.
2. **Twitter** — Interest-based: follow 5+ accounts → see feed. Low friction, but requires critical mass for value.
3. **Uber** — Action-based: add payment method → request first ride → complete. Value proven immediately (ride happens).
4. **Figma** — Feature-focused: create file → add shape → export. Hands-on learning, tutorial built into product.

---

## Build Instructions

**Files:** 11 total

**CSS Variables (Cyan/Sky for welcome):**
```css
--dd-ob-primary: #0891b2;     /* Cyan */
--dd-ob-secondary: #0369a1;
--dd-ob-accent: #06b6d4;
--dd-ob-bg: #ecf0f1;
--dd-ob-border: #67e8f9;
--dd-ob-text: #164e63;
```

**Key sections:**
- S1: Value realization (aha moment)
- S2: 7-node onboarding pipeline
- S3: Slack, Uber, Twitter, Figma comparison
- S4: Day-1, Day-7, Day-30 retention metrics
- S5: Signup flow, profile setup, feature education, activation tracking
- S6: Dropout, feature overload, motivation mismatch, network effects, re-engagement, mobile vs web
- S7: Slack, Uber, Twitter, Figma patterns

**Route:** `/resources/product-breakdowns/onboarding-activation`
**Gallery slug:** `onboarding_and_activation.html`

