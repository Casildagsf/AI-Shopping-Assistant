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

PRODUCTS_PATH = DATA_DIR / "product_clusters.csv"

TOP_PRODUCTS_PATH = DATA_DIR / "top_products.csv"

LOWEST_PRODUCTS_PATH = DATA_DIR / "lowest_products.csv"

SUMMARIES_PATH = DATA_DIR / "category_summaries.csv"

# ==========================================================
# Model
# ==========================================================

MODEL_NAME = "google/flan-t5-base"