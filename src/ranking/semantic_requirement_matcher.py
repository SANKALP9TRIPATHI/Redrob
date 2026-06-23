"""
Semantic requirement matching.
"""

import numpy as np

from src.retrieval.embedding_encoder import (
    encode_texts
)


def semantic_match_score(
    candidate_text,
    jd_text
):

    embeddings = encode_texts([
        candidate_text,
        jd_text
    ])

    candidate_emb = embeddings[0]
    jd_emb = embeddings[1]

    score = np.dot(
        candidate_emb,
        jd_emb
    )

    return float(score)