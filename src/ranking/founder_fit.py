"""
Founder-fit ranking.
"""


def compute_founder_fit(
    profile
):

    score = 0.0

    title = (
        profile.features.current_title
        .lower()
    )

    capabilities = (
        profile.capability_scores
    )

    if (
        capabilities.get(
            "PRODUCT_ENGINEERING",
            0
        )
        > 0.5
    ):
        score += 0.35

    if (
        capabilities.get(
            "RANKING_SYSTEMS",
            0
        )
        > 0.5
    ):
        score += 0.25

    if (
        capabilities.get(
            "EMBEDDING_RETRIEVAL",
            0
        )
        > 0.5
    ):
        score += 0.25

    if (
        "lead" in title
        or "staff" in title
        or "senior" in title
    ):
        score += 0.15

    return round(
        min(score, 1.0),
        4
    )