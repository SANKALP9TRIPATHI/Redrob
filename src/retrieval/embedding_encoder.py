"""
Embedding utilities.
"""

from sentence_transformers import (
    SentenceTransformer
)

MODEL_NAME = (
    "BAAI/bge-small-en-v1.5"
)

_model = None


def get_model():

    global _model

    if _model is None:

        _model = SentenceTransformer(
            MODEL_NAME
        )

    return _model


def encode_texts(texts):

    model = get_model()

    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )