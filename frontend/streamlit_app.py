"""
Streamlit frontend for the Amazon AI Shopping Assistant.

This is a single self-contained app: it loads the FLAN-T5 model and the
processed data directly (no separate API), so it can run for free on
Hugging Face Spaces.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Make sure the repo root is importable when Streamlit runs this file
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.assistant import answer_question


st.set_page_config(
    page_title="Amazon AI Shopping Assistant",
    page_icon="🛒",
    layout="centered",
)


@st.cache_resource(show_spinner="Loading the AI model (first run only)…")
def warm_up():
    """
    Trigger the one-time model + data load and cache it across reruns.
    Importing backend.assistant already loads the model; this just makes
    the loading state visible to the user on the first request.
    """
    return True


st.title("🛒 Amazon AI Shopping Assistant")
st.caption(
    "Ask a shopping question and get an AI-generated recommendation based on "
    "thousands of real Amazon customer reviews. Powered by FLAN-T5 — no paid APIs."
)

warm_up()

with st.expander("💡 Example questions"):
    st.markdown(
        "- I need a tablet for reading books\n"
        "- What's a good speaker with Alexa?\n"
        "- Recommend a device for watching Netflix\n"
        "- I'm looking for a charger for my Kindle"
    )

question = st.text_input(
    "Your question",
    placeholder="e.g. I need a tablet for reading books",
)

ask = st.button("Ask the assistant", type="primary")

if ask and question.strip():

    with st.spinner("Thinking…"):
        result = answer_question(question)

    if result.get("category") is None:
        st.warning(result["answer"])
    else:
        st.caption(f"📂 Category: **{result['category']}**")

        st.success(f"⭐ **Top pick:** {result['recommended_product']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Average rating", f"{result['rating']:.2f} / 5")
        col2.metric("Customer reviews", f"{result['reviews']:,}")

        if result.get("recommend_rate"):
            col3.metric("Would recommend", f"{result['recommend_rate']:.0f}%")
        elif result.get("pct_positive"):
            col3.metric("Positive reviews", f"{result['pct_positive']:.0f}%")

        st.subheader("Why other customers liked this product")
        st.write(result["llm_explanation"])

        loved = result.get("loved_themes") or []
        complaints = result.get("complaint_themes") or []
        if loved or complaints:
            good_col, bad_col = st.columns(2)
            with good_col:
                st.markdown("**👍 What customers love**")
                st.markdown(
                    "\n".join(f"- {t}" for t in loved) or "_No data_"
                )
            with bad_col:
                st.markdown("**👎 Common complaints**")
                st.markdown(
                    "\n".join(f"- {t}" for t in complaints) or "_No data_"
                )

        quote = result.get("quote")
        if quote and quote.get("text"):
            stars = "⭐" * int(round(quote.get("rating") or 0))
            helpful = quote.get("helpful") or 0
            st.markdown("**💬 In a customer's own words**")
            st.info(f"“{quote['text']}”")
            caption = " · ".join(
                part
                for part in [
                    stars,
                    f"{helpful} people found this helpful" if helpful else "",
                ]
                if part
            )
            if caption:
                st.caption(caption)

        options = result.get("all_products", [])
        if len(options) > 1:
            st.subheader(f"All options in {result['category']}")
            st.caption("Ranked by rating and how many customers reviewed it.")

            table = pd.DataFrame(options).rename(
                columns={
                    "name": "Product",
                    "rating": "Rating",
                    "reviews": "Reviews",
                    "pct_positive": "Positive",
                }
            )

            st.dataframe(
                table,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Product": st.column_config.TextColumn(
                        "Product", width="large"
                    ),
                    "Rating": st.column_config.NumberColumn(
                        "Rating", format="%.2f ⭐"
                    ),
                    "Reviews": st.column_config.NumberColumn(
                        "Reviews", format="%d"
                    ),
                    "Positive": st.column_config.NumberColumn(
                        "Positive", format="%.0f%%"
                    ),
                },
            )

elif ask:
    st.info("Please type a question first.")

st.divider()
st.caption("Built with FastAPI logic, Hugging Face Transformers & Streamlit.")
