"""
Capability ranking.
"""

from src.taxonomy.capability_taxonomy import (
    JD_PRIORITY_CAPABILITIES
)


def capability_fit_score(
    capability_scores: dict
):

    total_weight = 0
    weighted_score = 0

    for capability, weight in (
        JD_PRIORITY_CAPABILITIES.items()
    ):

        total_weight += weight

        weighted_score += (

            capability_scores.get(
                capability,
                0
            )
            *
            weight
        )

    return (
        weighted_score
        /
        total_weight
    )