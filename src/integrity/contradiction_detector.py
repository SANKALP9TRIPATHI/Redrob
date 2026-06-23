"""
Contradiction detection.
"""


def detect_contradictions(
    candidate
):

    flags = []

    total_exp = (
        candidate["profile"]
        .get(
            "years_of_experience",
            0
        )
    )

    total_months = sum(

        role.get(
            "duration_months",
            0
        )

        for role in candidate.get(
            "career_history",
            []
        )
    )

    if (
        total_exp * 12
        >
        total_months + 24
    ):
        flags.append(
            "experience_mismatch"
        )

    return flags