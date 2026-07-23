"""
Build prompts for the AI Shopping Assistant.
"""


def build_prompt(
    question,
    recommended_product,
    category,
    rating,
    reviews
):
    """
    Build a prompt for FLAN-T5.
    """

    prompt = f"""
You are an Amazon Shopping Assistant.

A customer asked:

{question}

You have already selected the best product.

Recommended product:
{recommended_product}

Category:
{category}

Average customer rating:
{rating:.2f}/5

Number of customer reviews:
{reviews}

Explain in 2 or 3 sentences why this product is a good recommendation.

Answer:
"""

    return prompt