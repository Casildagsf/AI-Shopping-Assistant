"""
Build prompts for the AI Shopping Assistant.
"""


def build_prompt(
    question,
    recommended_product,
    category,
    rating,
    reviews,
    summary=None,
):
    """
    Build an instruction-style prompt for FLAN-T5.

    The model is asked to answer the customer's actual question using the
    facts we have (recommended product, rating, review count and, when it is
    readable, a short summary of what reviewers say).
    """

    facts = [
        f"- Recommended product: {recommended_product}",
        f"- Category: {category}",
        f"- Average customer rating: {rating:.2f} out of 5",
        f"- Based on {reviews} customer reviews",
    ]

    if summary:
        facts.append(f"- What reviewers say: {summary}")

    facts_block = "\n".join(facts)

    prompt = (
        "You are a helpful Amazon shopping assistant. "
        "Answer the customer's question in 2 or 3 complete sentences, "
        "using the product information below. Recommend the product and "
        "explain why it is a good choice. Do not just repeat the product name.\n\n"
        f"Customer question: {question}\n\n"
        f"Product information:\n{facts_block}\n\n"
        "Helpful answer:"
    )

    return prompt
