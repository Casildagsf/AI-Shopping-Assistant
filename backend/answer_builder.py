"""
Post-process the language model output.

FLAN-T5 (base) is small and free, so it sometimes parrots the product facts
back instead of writing a real recommendation. We detect those low-quality
generations and fall back to an answer composed directly from the real review
evidence (recommend rate, sentiment, loved themes and a genuine customer
quote), so the user always gets a real, coherent recommendation.
"""


def _is_low_quality(answer, question, product=""):
    """
    Return True if the generated answer looks like a parrot of the input
    (copied facts, echoed question, or just the product name).
    """

    text = (answer or "").strip()
    low = text.lower()

    if len(text) < 25:
        return True

    prod = product.strip().lower()
    if prod:
        remainder = low.replace(prod, "").strip(" .,-")
        if len(remainder) < 15:
            return True

    fact_markers = [
        "category:",
        "average rating",
        "out of 5",
        "% of reviewers",
        "% of reviews",
        "recommended product",
        "review evidence",
    ]
    if any(marker in low for marker in fact_markers):
        return True

    instruction_markers = [
        "in your own words",
        "do not",
        "helpful answer",
        "what customers love",
    ]
    if any(marker in low for marker in instruction_markers):
        return True

    q = question.strip().lower().rstrip("?.! ")
    if q and low.startswith(q[: min(len(q), 25)]):
        return True

    if text.rstrip().endswith("?"):
        return True

    # A bare comma-separated list of keywords, not a real sentence.
    if "." not in text and text.count(",") >= 3:
        return True

    return False


def compose_answer(
    product,
    category,
    rating,
    reviews,
    loved_themes=None,
    recommend_rate=None,
    pct_positive=None,
    quote=None,
):
    """
    Build a real recommendation from the structured review evidence.
    """

    sentences = [
        f"Based on {reviews:,} customer reviews, the {product} is the top "
        f"choice in {category}."
    ]

    if recommend_rate:
        sentences.append(
            f"It rates {rating:.1f}/5 and {recommend_rate:.0f}% of reviewers "
            f"would recommend it."
        )
    elif pct_positive:
        sentences.append(
            f"It rates {rating:.1f}/5, with {pct_positive:.0f}% of reviews "
            f"being positive."
        )
    else:
        sentences.append(f"It holds an average rating of {rating:.1f}/5.")

    themes = list(loved_themes or [])[:3]
    if themes:
        if len(themes) == 1:
            joined = themes[0]
        else:
            joined = ", ".join(themes[:-1]) + " and " + themes[-1]
        sentences.append(f"Customers especially like its {joined}.")

    if quote and quote.get("text"):
        sentences.append(f'One reviewer said: "{quote["text"]}"')

    return " ".join(sentences)


def finalize_answer(raw_answer, question, product, evidence):
    """
    Return the model answer if it is good, otherwise a composed fallback built
    from `evidence` (the dict returned by retrieval.get_category_data).
    """

    if _is_low_quality(raw_answer, question, product):
        return compose_answer(
            product=product,
            category=evidence["category"],
            rating=evidence["rating"],
            reviews=evidence["reviews"],
            loved_themes=evidence.get("loved_themes"),
            recommend_rate=evidence.get("recommend_rate"),
            pct_positive=evidence.get("pct_positive"),
            quote=evidence.get("quote"),
        )

    return raw_answer.strip()
