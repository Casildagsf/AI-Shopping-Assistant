"""
Functions for loading the processed data.
"""

import numpy as np
import pandas as pd

from backend.config import (
    PRODUCTS_PATH,
    TOP_PRODUCTS_PATH,
    LOWEST_PRODUCTS_PATH,
    SUMMARIES_PATH,
)

# How much a large review count can lift a product's ranking score. The bonus
# is REVIEW_WEIGHT * log10(1 + n_reviews), so it rewards well-reviewed products
# without letting volume override a genuinely higher rating.
REVIEW_WEIGHT = 0.05


def load_data():
    """
    Load all processed datasets used by the shopping assistant.

    Returns
    -------
    tuple
        products,
        top_products,
        lowest_products,
        summaries
    """

    products = pd.read_csv(PRODUCTS_PATH)

    top_products = pd.read_csv(TOP_PRODUCTS_PATH)

    lowest_products = pd.read_csv(LOWEST_PRODUCTS_PATH)

    summaries = pd.read_csv(SUMMARIES_PATH)

    return (
        products,
        top_products,
        lowest_products,
        summaries,
    )


def get_category_data(
    category,
    top_products,
    lowest_products,
    summaries
):
    """
    Retrieve all information for one category.
    """

    # Rank by rating plus a confidence bonus for how many reviews back it up:
    #   score = mean_rating + REVIEW_WEIGHT * log10(1 + n_reviews)
    # A near-identical rating with far more reviews wins (e.g. 4.59 with 2814
    # reviews beats 4.60 with 30), while a real rating gap still dominates
    # (log grows slowly, so the volume bonus stays small).
    top = top_products.loc[
        top_products["cluster_name"] == category
    ].copy()

    top["score"] = top["mean_rating"] + REVIEW_WEIGHT * np.log10(
        1 + top["n_reviews"]
    )

    top = top.sort_values("score", ascending=False)

    if category == "Kindle E-Readers":
        top = top[
            ~top["name"].str.contains(
                "Kindle Fire",
                case=False,
                na=False
            )
        ]

    best_product = top.iloc[0]

    all_products = [
        {
            "name": row["name"],
            "rating": float(row["mean_rating"]),
            "reviews": int(row["n_reviews"]),
        }
        for _, row in top.iterrows()
    ]

    summary_rows = summaries.loc[
        summaries["cluster_name"] == category, "summary"
    ]
    raw_summary = summary_rows.iloc[0] if len(summary_rows) else ""

    return {
        "recommended_product": best_product["name"],
        "rating": best_product["mean_rating"],
        "reviews": int(best_product["n_reviews"]),
        "all_products": all_products,
        "summary": raw_summary,
    }