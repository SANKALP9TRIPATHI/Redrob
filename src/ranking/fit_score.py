"""
Overall fit scoring.
"""

from src.ranking.capability_ranker import (
    capability_fit_score
)

from src.ranking.requirement_coverage import (
    compute_requirement_coverage
)


def compute_fit_score(
    profile,
    role_contract
):

    capability_score = (

        capability_fit_score(
            profile.capability_scores
        )
    )

    coverage = (

        compute_requirement_coverage(
            profile,
            role_contract
        )
    )

    final_score = (

        0.7 * capability_score
        +
        0.3 * coverage[
            "coverage_ratio"
        ]
    )

    return {

        "fit_score":
            round(
                final_score,
                4
            ),

        "capability_score":
            capability_score,

        "coverage":
            coverage
    }