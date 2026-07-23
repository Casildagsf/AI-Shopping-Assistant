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