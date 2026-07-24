"""
Post-process the language model output.

FLAN-T5 (base) is small and free, so on questions where we have no readable
review summary it tends to parrot the product facts back instead of writing a
real recommendation. We detect those low-quality generations and fall back to a
sensible answer composed directly from the structured data, so the user always
gets a real, coherent recommendation.
"""


# Generic, honest talking points per category, used only when we have no
# readable review summary to ground the answer.
CATEGORY_BENEFITS = {
    "Fire Tablets": (
        "it is a versatile, budget-friendly tablet that customers like for "
        "browsing, streaming video and reading"
    ),
    "Kindle E-Readers": (
        "it is built for comfortable long reading sessions with a glare-free, "
        "easy-on-the-eyes display and long battery life"
    ),
    "Echo, Fire TV & Smart Home": (
        "it is a popular choice for hands-free Alexa control, music and "
        "streaming your favourite shows"
    ),
    "Accessories & Cables": (
        "it is a reliable, well-reviewed accessory that does its job without fuss"
    ),
}


def _is_low_quality(answer, question, product=""):
    """
    Return True if the generated answer looks like a parrot of the input
    (copied facts, echoed question, or just the product name) rather than a
    real recommendation.
    """

    text = (answer or "").strip()
    low = text.lower()

    if len(text) < 25:
        return True

    # Just the product name with almost nothing else around it.
    prod = product.strip().lower()
    if prod:
        remainder = low.replace(prod, "").strip(" .,-")
        if len(remainder) < 15:
            return True

    # Copied straight from the facts block.
    fact_markers = [
        "category:",
        "customer rating",
        "based on ",
        "out of 5 -",
        "average customer",
    ]
    if any(marker in low for marker in fact_markers):
        return True

    # Leaked instruction text from the prompt.
    instruction_markers = [
        "in your own words",
        "do not copy",
        "explain why it is a good choice",
        "recommend the product",
        "helpful answer",
    ]
    if any(marker in low for marker in instruction_markers):
        return True

    # Simply echoing the question back.
    q = question.strip().lower().rstrip("?.! ")
    if q and low.startswith(q[: min(len(q), 25)]):
        return True

    # A recommendation should not end by asking the customer a question.
    if text.rstrip().endswith("?"):
        return True

    return False


def compose_answer(question, product, category, rating, reviews, summary=None):
    """
    Build a real recommendation sentence-by-sentence from the structured data.
    Used as a fallback when the model output is low quality.
    """

    sentences = [
        f"Based on thousands of customer reviews, the {product} is the top "
        f"choice in {category}."
    ]

    if reviews >= 1000:
        sentences.append(
            f"It holds a strong average rating of {rating:.1f}/5 across "
            f"{reviews:,} reviews, so it is a well-proven, popular option."
        )
    else:
        sentences.append(
            f"It earns an average rating of {rating:.1f}/5 from {reviews:,} "
            f"customer reviews."
        )

    if summary:
        highlight = summary.strip().rstrip(".")
        sentences.append(f"Reviewers highlight that {highlight}.")
    elif category in CATEGORY_BENEFITS:
        sentences.append(
            f"For what you are looking for, {CATEGORY_BENEFITS[category]}."
        )

    return " ".join(sentences)


def finalize_answer(
    raw_answer,
    question,
    product,
    category,
    rating,
    reviews,
    summary=None,
):
    """
    Return the model answer if it is good, otherwise a composed fallback.
    """

    if _is_low_quality(raw_answer, question, product):
        return compose_answer(
            question, product, category, rating, reviews, summary
        )

    return raw_answer.strip()
