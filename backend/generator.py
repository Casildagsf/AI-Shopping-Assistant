"""
Generate answers using FLAN-T5.
"""

import torch


def generate_answer(
    prompt,
    tokenizer,
    model,
    device
):
    """
    Generate an answer from a prompt.
    """

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=160,
            min_new_tokens=30,
            num_beams=4,
            no_repeat_ngram_size=3,
            repetition_penalty=1.4,
            length_penalty=1.0,
            early_stopping=True,
        )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer