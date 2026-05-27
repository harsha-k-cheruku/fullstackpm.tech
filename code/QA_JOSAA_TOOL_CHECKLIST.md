# QA Checklist — JoSAA Top 25 Tool

## Manual
- Default run renders top 25 with probability and band.
- Branch/institute constraints reduce candidate pool and still rank correctly.
- No-result state is graceful and recoverable.
- Export CSV returns downloadable file.

## Suggested Playwright Cases
1. Default probability run
2. Constrained run
3. No-result state
4. Export CSV download

Use the skeleton provided by qa-kitten in the swarm session.
