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

# Deep dive — multi-AI roundtable (Grok + GPT reserved for this; main pipeline = Claude only)
BELIEVER_PROVIDER = "openai"
BELIEVER_MODEL = os.environ.get("PIPELINE_BELIEVER_MODEL", "gpt-4o")
SKEPTIC_PROVIDER = "xai"
SKEPTIC_MODEL = os.environ.get("PIPELINE_SKEPTIC_MODEL", "grok-3")
REALIST_PROVIDER = "anthropic"
REALIST_MODEL = os.environ.get("PIPELINE_REALIST_MODEL", "claude-haiku-4-5-20251001")

DEEP_DIVE_PROMPT_VERSION = "deepdive-v1"
DEEP_DIVE_SEED = os.environ.get("PIPELINE_DEEP_DIVE_SEED")  # set for reproducibility

# Depth profiles — controls model tier AND conversation length per topic depth.
# Override individual models via env vars (e.g. PIPELINE_DEEP_BELIEVER=gpt-5).
DEEP_DIVE_DEPTH_PROFILES = {
    "light": {
        "min_turns": 6, "max_turns": 9,
        "believer_model": os.environ.get("PIPELINE_LIGHT_BELIEVER", "gpt-4o-mini"),
        "skeptic_model":  os.environ.get("PIPELINE_LIGHT_SKEPTIC",  "grok-3-mini"),
        "realist_model":  os.environ.get("PIPELINE_LIGHT_REALIST",  "claude-haiku-4-5-20251001"),
    },
    "standard": {
        "min_turns": 9, "max_turns": 15,
        "believer_model": BELIEVER_MODEL,
        "skeptic_model":  SKEPTIC_MODEL,
        "realist_model":  REALIST_MODEL,
    },
    "deep": {
        "min_turns": 12, "max_turns": 20,
        "believer_model": os.environ.get("PIPELINE_DEEP_BELIEVER", "gpt-4o"),
        "skeptic_model":  os.environ.get("PIPELINE_DEEP_SKEPTIC",  "grok-3"),
        "realist_model":  os.environ.get("PIPELINE_DEEP_REALIST",  "claude-sonnet-4-6"),
    },
}
DEEP_DIVE_DEFAULT_DEPTH = os.environ.get("PIPELINE_DEEP_DIVE_DEPTH", "standard")

# Closing-turn behavior. Avoids the Narada-style forced-synthesis problem
# where the AI always connects dots even when there isn't a clean takeaway.
#   force    — Realist MUST name a PM action
#   optional — Realist names one only if it's clean and non-obvious (default)
#   off      — no PM-action prompt; close with a sharp observation or question
DEEP_DIVE_PM_ACTION_MODE = os.environ.get("PIPELINE_DEEP_DIVE_PM_ACTION", "optional")

# How many articles get the editorial rewrite per run
REWRITE_TOP_N = int(os.environ.get("PIPELINE_REWRITE_TOP_N", "12"))

# Min score for an article to qualify for rewrite + publish
MIN_PUBLISH_SCORE = int(os.environ.get("PIPELINE_MIN_PUBLISH_SCORE", "6"))

# How many articles to extract+analyse per run (cost guardrail)
MAX_ANALYSE_PER_RUN = int(os.environ.get("PIPELINE_MAX_ANALYSE", "60"))

# Extraction config
EXTRACT_TIMEOUT_SECONDS = 15
EXTRACT_USER_AGENT = "Mozilla/5.0 (compatible; fullstackpm.tech editorial pipeline)"
