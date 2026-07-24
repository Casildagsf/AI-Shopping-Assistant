"""
Build prompts for the AI Shopping Assistant.
"""


def build_prompt(
    question,
    recommended_product,
    category,
    rating,
    reviews,
    loved_themes=None,
    recommend_rate=None,
    pct_positive=None,
    quote=None,
):
    """
    Build an instruction-style prompt grounded in real review evidence so the
    model answers the customer's actual question instead of parroting facts.
    """

    facts = [
        f"- Recommended product: {recommended_product}",
        f"- Category: {category}",
        f"- Average rating: {rating:.2f} out of 5 from {reviews} reviews",
    ]

    if recommend_rate:
        facts.append(f"- {recommend_rate:.0f}% of reviewers recommend it")
    elif pct_positive:
        facts.append(f"- {pct_positive:.0f}% of reviews are positive")

    if loved_themes:
        facts.append("- What customers love: " + ", ".join(loved_themes))

    if quote and quote.get("text"):
        facts.append(f'- A real customer review: "{quote["text"]}"')

    facts_block = "\n".join(facts)

    prompt = (
        "You are a helpful Amazon shopping assistant. Using the review evidence "
        "below, answer the customer's question in 2 or 3 complete sentences. "
        "Recommend the product and explain, in your own words, why customers "
        "like it. Do not just repeat the product name or the facts.\n\n"
        f"Customer question: {question}\n\n"
        f"Review evidence:\n{facts_block}\n\n"
        "Helpful answer:"
    )

    return prompt
