"""
Application configuration.
"""

from pathlib import Path

# ==========================================================
# Base Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

# ==========================================================
# Data Files
# ==========================================================

# Rich per-product evidence (ranking, pros/cons themes, sentiment and real
# customer quotes) produced by the Amazon Review NLP pipeline (Project 3).
EVIDENCE_PACK_PATH = DATA_DIR / "evidence_pack.json"

# ==========================================================
# Model
# ==========================================================

MODEL_NAME = "google/flan-t5-base"