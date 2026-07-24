"""
Utility functions.
"""

import re


def clean_product_name(name: str) -> str:
    """
    Simplify long Amazon product titles for display.
    """

    if not isinstance(name, str):
        return ""

    # Remove repeated commas
    name = re.sub(r",+", "", name)

    # Keep only the text before the first dash
    name = name.split(" - ")[0]

    # Drop a trailing ASIN tag like "[B01J2G4VBG]".
    name = re.sub(r"\[[^\]]*\]", "", name)

    # Evidence-pack names are long marketing titles; cut boilerplate tails.
    for tail in ("Includes Special Offers", "Special Offers"):
        idx = name.lower().find(tail.lower())
        if idx != -1:
            name = name[:idx]

    name = re.sub(r"\s+", " ", name)

    return name.strip(" ,-")


def clean_themes(themes, limit=5):
    """
    Tidy a list of one-word review themes: drop duplicates and near-duplicates
    (e.g. keep "reading", drop "read"), preserving order, up to `limit`.
    """

    kept = []

    for theme in themes or []:
        t = str(theme).strip().lower()
        if not t:
            continue

        # Skip if it is a stem/plural variant of something we already kept.
        if any(t == k or k.startswith(t) or t.startswith(k) for k in kept):
            continue

        kept.append(t)

        if len(kept) >= limit:
            break

    return kept


def clean_review_summary(summary) -> str:
    """
    Return a review summary only if it reads like real prose.

    Some category summaries in the data are noise or garbled, repetitive
    fragments (e.g. "Kindle Paperwhite Kindle Paperwhite ..."). Feeding those
    to the model produces junk, so we keep a summary only when it is long
    enough and its words are varied enough to be a genuine sentence.
    """

    if not isinstance(summary, str):
        return ""

    text = summary.strip()

    if len(text) < 40:
        return ""

    words = [w.lower() for w in re.findall(r"[a-zA-Z']+", text)]

    if len(words) < 8:
        return ""

    # Reject repetitive / list-like fragments with few distinct words.
    unique_ratio = len(set(words)) / len(words)
    if unique_ratio < 0.6:
        return ""

    return text