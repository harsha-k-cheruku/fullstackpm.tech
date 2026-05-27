# JoSAA Route Smoke Test

Manual quick checks:

1. Open `/tools/josaa-top-25`
2. Submit rank + year only -> should return results table
3. Add strict mode + institute filter -> still returns constrained table or empty state
4. Click `+ Shortlist` on 2-3 rows -> see bucket cards populate
5. Reload page -> shortlist persists (localStorage)
6. Click `Export Top 25 CSV` -> file downloads
