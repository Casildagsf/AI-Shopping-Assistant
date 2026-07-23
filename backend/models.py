"""
Load the language model used by the Shopping Assistant.
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

from backend.config import MODEL_NAME


def load_model():
    """
    Load FLAN-T5 once when the application starts.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME
    )

    model.to(device)

    return tokenizer, model, device