"""
Intent routing for the AI Shopping Assistant.

This module determines which product category
is most relevant to the user's question.
"""

from typing import Optional

# ==========================================================
# Keywords for each category
# ==========================================================

CATEGORY_KEYWORDS = {
    "Fire Tablets": [
        "tablet",
        "fire tablet",
        "fire hd",
        "fire 7",
        "fire 8",
        "fire 10"
    ],

    "Kindle E-Readers": [
        "kindle",
        "ebook",
        "e-reader",
        "ereader",
        "reading",
        "book",
        "books",
        "paperwhite",
        "oasis"
    ],

    "Echo, Fire TV & Smart Home": [
        "echo",
        "alexa",
        "speaker",
        "smart home",
        "fire tv",
        "tv",
        "streaming",
        "stream",
        "netflix",
        "movies",
        "movie",
        "video",
        "prime video"
    ],
    

    "Accessories & Cables": [
        "charger",
        "charging",
        "cable",
        "adapter",
        "usb",
        "case",
        "cover",
        "accessory",
        "accessories"
    ]
}


# ==========================================================
# Category Identification
# ==========================================================

def identify_category(question: str) -> Optional[str]:
    """
    Identify the most relevant product category
    from a user's question.

    Parameters
    ----------
    question : str

    Returns
    -------
    str or None
    """

    question = question.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            if keyword in question:

                return category

    return None