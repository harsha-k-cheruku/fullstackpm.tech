"""Pipeline config — paths, model selection, prompt versions."""
import os
import sys
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PIPELINE_ROOT.parent
CODE_ROOT = PROJECT_ROOT / "code"
DATA_DIR = PIPELINE_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_DB_PATH = DATA_DIR / "pipeline.db"

# Where published JSON lands (read by Render at boot)
PUBLISH_DIR = CODE_ROOT / "content" / "feed"
PUBLISH_DIR.mkdir(parents=True, exist_ok=True)

# Env wiring before app modules import
os.environ.setdefault("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Make app/ importable
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

# Stage-specific knobs
ANALYSE_MODEL = os.environ.get("PIPELINE_ANALYSE_MODEL", "claude-haiku-4-5-20251001")
REWRITE_MODEL = os.environ.get("PIPELINE_REWRITE_MODEL", "claude-haiku-4-5-20251001")

ANALYSE_PROMPT_VERSION = "analyse-v1"
REWRITE_PROMPT_VERSION = "rewrite-v1"

# How many articles get the editorial rewrite per run
REWRITE_TOP_N = int(os.environ.get("PIPELINE_REWRITE_TOP_N", "12"))

# Min score for an article to qualify for rewrite + publish
MIN_PUBLISH_SCORE = int(os.environ.get("PIPELINE_MIN_PUBLISH_SCORE", "6"))

# How many articles to extract+analyse per run (cost guardrail)
MAX_ANALYSE_PER_RUN = int(os.environ.get("PIPELINE_MAX_ANALYSE", "60"))

# Extraction config
EXTRACT_TIMEOUT_SECONDS = 15
EXTRACT_USER_AGENT = "Mozilla/5.0 (compatible; fullstackpm.tech editorial pipeline)"
