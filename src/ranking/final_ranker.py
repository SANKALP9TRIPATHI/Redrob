"""
Final ranking score.
"""

from src.ranking.fit_score import (
    compute_fit_score
)

from src.ranking.career_ranker import (
    compute_career_score
)

from src.ranking.founder_fit import (
    compute_founder_fit
)

from src.ranking.behavioral_ranker import (
    compute_behavioral_score
)

from src.integrity.integrity_checks import (
    compute_integrity_score
)


def compute_final_score(
    candidate,
    profile,
    role
):

    fit = compute_fit_score(
        profile,
        role
    )

    career = (
        compute_career_score(
            profile
        )
    )

    founder = (
        compute_founder_fit(
            profile
        )
    )

    behavior = (
        compute_behavioral_score(
            profile
        )
    )

    integrity = (
        compute_integrity_score(
            candidate
        )
    )

    base_score = (

        0.40
        * fit["fit_score"]

        + 0.20
        * career

        + 0.15
        * founder

        + 0.15
        * behavior

        + 0.10
        * integrity["score"]
    )

    final_score = (
        base_score
        * integrity["score"]
    )

    return {

        "final_score":
            round(
                final_score,
                4
            ),

        "fit_score":
            fit["fit_score"],

        "career_score":
            career,

        "founder_fit":
            founder,

        "behavior_score":
            behavior,

        "integrity":
            integrity
    }