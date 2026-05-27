# Swarm Plan — JoSAA Top 25 Tool

## Goal
Ship a production-ready JoSAA Top 25 predictor inside fullstackpm.tech with strong UX, rule-aware scoring, and QA-backed stability.

## Agents
- planning-agent: orchestration, task sequencing, acceptance gating
- code-puppy: implementation and bug fixing
- qa-kitten: browser QA, defect reporting, regression confidence

## Scope
1. Core predictor flow (rank -> shortlist)
2. Constraint-aware ranking (branch/institute hard filters)
3. Explainability (probability, gap-to-close, banding)
4. Rule-aware mode (basic vs strict)
5. Preference weighting and shortlist builder UX
6. Export + session persistence
7. QA automation and release signoff

## Work Phases

### Phase 1 — Core Build Hardening
- Finalize service logic and deterministic ranking
- Add strict-mode rule hooks
- Add preference weighting
- Improve empty/error UX

### Phase 2 — UX Completion
- Build shortlist workspace (safe/target/aspirational buckets)
- Add export CSV
- Add clear “filters applied” and result rationale

### Phase 3 — QA + Stabilization
- Playwright smoke and interaction tests
- Close high/critical issues
- Final release notes and rollback notes

## Acceptance Criteria
- Returns valid top 25 for supported inputs
- Deterministic output for same input
- Constraint behavior: filter first, rank second
- No critical rendering or interaction bugs
- Export works and matches on-screen data
