"""
Functions for loading the processed data.
"""

import pandas as pd

from backend.config import (
    PRODUCTS_PATH,
    TOP_PRODUCTS_PATH,
    LOWEST_PRODUCTS_PATH,
    SUMMARIES_PATH,
)


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

    top = (
        top_products.loc[
            top_products["cluster_name"] == category
        ]
        .sort_values("mean_rating", ascending=False)
    )

    if category == "Kindle E-Readers":
        top = top[
            ~top["name"].str.contains(
                "Kindle Fire",
                case=False,
                na=False
            )
        ]

    best_product = top.iloc[0]

    return {
        "recommended_product": best_product["name"],
        "rating": best_product["mean_rating"],
        "reviews": int(best_product["n_reviews"])
    }