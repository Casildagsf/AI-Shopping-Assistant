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

    return name.strip()


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