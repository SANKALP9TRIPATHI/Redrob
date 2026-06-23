"""
Dense retrieval.
"""

import numpy as np


class DenseRetriever:

    def __init__(
        self,
        embeddings,
        candidate_ids
    ):

        self.embeddings = embeddings

        self.candidate_ids = (
            candidate_ids
        )

    def search(
        self,
        query_embedding,
        top_k=500
    ):

        scores = (
            self.embeddings
            @ query_embedding
        )

        indices = np.argsort(
            scores
        )[::-1][:top_k]

        return [

            (
                self.candidate_ids[i],
                float(scores[i])
            )

            for i in indices
        ]