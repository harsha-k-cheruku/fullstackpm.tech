"""fullstackpm.tech local editorial pipeline.

Stages (each runnable independently):
  fetch   → RSS to DB
  extract → full text scraping
  analyse → Claude reads full text → structured analysis + score
  rewrite → top N → polished editorial in HC's voice
  publish → DB → JSON in code/content/feed/ → git push

DB: pipeline/data/pipeline.db (SQLite, gitignored)
Run from project root: python -m pipeline <stage>
"""
