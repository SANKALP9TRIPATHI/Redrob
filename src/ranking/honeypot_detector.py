"""
Honeypot detection.
"""


def honeypot_score(
    candidate,
    integrity_flags
):

    penalty = 0

    penalty += (
        len(integrity_flags)
        * 0.20
    )

    total_exp = (
        candidate["profile"]
        .get(
            "years_of_experience",
            0
        )
    )

    if total_exp > 25:
        penalty += 0.20

    return min(
        penalty,
        1.0
    )