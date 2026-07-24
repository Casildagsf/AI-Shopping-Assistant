"""
Main AI Shopping Assistant.
"""

from backend.utils import clean_product_name, clean_themes
from backend.retrieval import load_data, get_category_data
from backend.intent_router import identify_category
from backend.prompt_builder import build_prompt
from backend.generator import generate_answer
from backend.answer_builder import finalize_answer
from backend.models import load_model


# Load everything once
clusters = load_data()

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

    category_data = get_category_data(category, clusters)

    if category_data is None:

        return {
            "category": None,
            "answer": "Sorry, I don't have data for that category yet.",
        }

    recommended_product = clean_product_name(
        category_data["recommended_product"]
    )

    loved_themes = clean_themes(category_data.get("loved_themes"), limit=5)
    complaint_themes = clean_themes(
        category_data.get("complaint_themes"), limit=4
    )

    all_products = [
        {
            "name": clean_product_name(product["name"]),
            "rating": product["rating"],
            "reviews": product["reviews"],
            "pct_positive": product.get("pct_positive"),
        }
        for product in category_data["all_products"]
    ]

    prompt = build_prompt(
        question=question,
        recommended_product=recommended_product,
        category=category,
        rating=category_data["rating"],
        reviews=category_data["reviews"],
        loved_themes=loved_themes,
        recommend_rate=category_data.get("recommend_rate"),
        pct_positive=category_data.get("pct_positive"),
        quote=category_data.get("quote"),
    )

    raw_answer = generate_answer(prompt, tokenizer, model, device)

    evidence = {
        "category": category,
        "rating": category_data["rating"],
        "reviews": category_data["reviews"],
        "loved_themes": loved_themes,
        "recommend_rate": category_data.get("recommend_rate"),
        "pct_positive": category_data.get("pct_positive"),
        "quote": category_data.get("quote"),
    }

    answer = finalize_answer(
        raw_answer,
        question=question,
        product=recommended_product,
        evidence=evidence,
    )

    return {
        "category": category,
        "recommended_product": recommended_product,
        "rating": category_data["rating"],
        "reviews": category_data["reviews"],
        "pct_positive": category_data.get("pct_positive"),
        "recommend_rate": category_data.get("recommend_rate"),
        "loved_themes": loved_themes,
        "complaint_themes": complaint_themes,
        "quote": category_data.get("quote"),
        "all_products": all_products,
        "llm_explanation": answer,
    }
