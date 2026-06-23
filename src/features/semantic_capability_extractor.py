"""
Semantic capability inference.
"""

import numpy as np

from src.retrieval.text_builder import (
    build_candidate_text
)

from src.retrieval.embedding_encoder import (
    encode_texts
)


def cosine_similarity(
    a,
    b
):

    return float(
        np.dot(a, b)
    )


def infer_semantic_capabilities(

    candidate,

    capability_embeddings,

    threshold=0.40
):

    text = build_candidate_text(
        candidate
    )

    candidate_embedding = (
        encode_texts([text])[0]
    )

    results = {}

    for (
        capability,
        capability_embedding
    ) in capability_embeddings.items():

        similarity = (
            cosine_similarity(
                candidate_embedding,
                capability_embedding
            )
        )

        if similarity >= threshold:

            results[
                capability
            ] = similarity

    return results