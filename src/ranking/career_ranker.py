"""
Career ranking.
"""


def compute_career_score(profile):

    career = profile.features.career_features

    score = 0.0

    total_months = career.get(
        "total_months", 0
    )

    avg_tenure = career.get(
        "avg_tenure_months", 0
    )

    consulting_ratio = career.get(
        "consulting_ratio", 0
    )

    if total_months >= 60:
        score += 0.35

    elif total_months >= 36:
        score += 0.25

    if avg_tenure >= 18:
        score += 0.25

    elif avg_tenure >= 12:
        score += 0.15

    score += (
        0.4 * (1 - consulting_ratio)
    )

    return round(
        min(score, 1.0),
        4
    )