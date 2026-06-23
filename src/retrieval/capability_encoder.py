"""
Capability embeddings.
"""

from src.retrieval.embedding_encoder import (
    encode_texts
)

from src.configs.capability_descriptions import (
    CAPABILITY_DESCRIPTIONS
)


def build_capability_embeddings():

    names = list(
        CAPABILITY_DESCRIPTIONS.keys()
    )

    texts = [

        CAPABILITY_DESCRIPTIONS[name]

        for name in names
    ]

    embeddings = encode_texts(texts)

    return {

        name: embedding

        for name, embedding
        in zip(names, embeddings)
    }