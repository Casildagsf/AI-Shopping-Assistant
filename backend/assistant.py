from backend.utils import clean_product_name, clean_review_summary
"""
Main AI Shopping Assistant.
"""

from backend.retrieval import (
    load_data,
    get_category_data
)

from backend.intent_router import identify_category
from backend.prompt_builder import build_prompt
from backend.generator import generate_answer
from backend.answer_builder import finalize_answer
from backend.models import load_model


# Load everything once
products, top_products, lowest_products, summaries = load_data()

tokenizer, model, device = load_model()


def answer_question(question):
    """
    Generate an answer for a shopping question.
    """

    category = identify_category(question)

    if category is None:

        return {
            "category": None,
            "answer": (
                "Sorry, I couldn't identify the product category. "
                "Try asking about Kindle, Fire Tablet, Echo, Fire TV, "
                "or Amazon accessories."
            )
        }

    category_data = get_category_data(
        category,
        top_products,
        lowest_products,
        summaries
    )

    recommended_product = clean_product_name(
        category_data["recommended_product"]
    )

    all_products = [
        {
            "name": clean_product_name(product["name"]),
            "rating": product["rating"],
            "reviews": product["reviews"],
        }
        for product in category_data["all_products"]
    ]

    summary = clean_review_summary(category_data.get("summary"))

    prompt = build_prompt(
        question=question,
        recommended_product=recommended_product,
        category=category,
        rating=category_data["rating"],
        reviews=category_data["reviews"],
        summary=summary,
    )

    raw_answer = generate_answer(
        prompt,
        tokenizer,
        model,
        device
    )

    answer = finalize_answer(
        raw_answer,
        question=question,
        product=recommended_product,
        category=category,
        rating=category_data["rating"],
        reviews=category_data["reviews"],
        summary=summary,
    )

    return {
        "category": category,
        "recommended_product": recommended_product,
        "rating": category_data["rating"],
        "reviews": category_data["reviews"],
        "all_products": all_products,
        "llm_explanation": answer
    }