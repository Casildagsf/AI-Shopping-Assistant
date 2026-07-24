"""
Load the evidence pack and retrieve per-category information.

The evidence pack (data/evidence_pack.json) is produced by the Amazon Review
NLP pipeline. For each category ("cluster") it holds a list of products already
ranked by a Bayesian (shrunken-mean) score, plus real review evidence: loved /
complaint themes, sentiment percentages and actual customer quotes.
"""

import json

from backend.config import EVIDENCE_PACK_PATH


def load_data():
    """
    Load the evidence pack and index its clusters by category name.

    Returns
    -------
    dict
        {category_name: cluster_dict}
    """

    with open(EVIDENCE_PACK_PATH, encoding="utf-8") as f:
        pack = json.load(f)

    return {cluster["cluster_name"]: cluster for cluster in pack["clusters"]}


def _best_quote(quotes):
    """
    Pick the most useful positive quote (most 'helpful' votes), if any.
    """

    if not quotes:
        return None

    # Prefer a concise, highly rated and helpful quote.
    def quote_key(q):
        text_len = len(q.get("text") or "")
        return (
            q.get("rating", 0) or 0,
            q.get("helpful", 0) or 0,
            -text_len,
        )

    best = max(quotes, key=quote_key)

    text = (best.get("text") or "").strip()
    if not text:
        return None

    return {
        "text": text,
        "rating": best.get("rating"),
        "helpful": best.get("helpful", 0) or 0,
    }


def get_category_data(category, clusters):
    """
    Retrieve the recommended product and supporting evidence for one category.
    Products in the evidence pack are already ranked (rank 1 = best), so we take
    them in order.
    """

    cluster = clusters.get(category)
    if cluster is None:
        return None

    products = cluster.get("products", [])
    if not products:
        return None

    best = products[0]

    all_products = [
        {
            "name": p["name"],
            "rating": float(p["mean_rating"]),
            "reviews": int(p["n_reviews"]),
            "pct_positive": p.get("pct_positive"),
        }
        for p in products
    ]

    return {
        "recommended_product": best["name"],
        "rating": float(best["mean_rating"]),
        "reviews": int(best["n_reviews"]),
        "pct_positive": best.get("pct_positive"),
        "recommend_rate": best.get("recommend_rate"),
        # Prefer product-level themes, fall back to the category's themes.
        "loved_themes": best.get("loved_themes") or cluster.get("loved_themes", []),
        "complaint_themes": (
            best.get("complaint_themes") or cluster.get("complaint_themes", [])
        ),
        "quote": _best_quote(best.get("quotes_positive", [])),
        "all_products": all_products,
    }
