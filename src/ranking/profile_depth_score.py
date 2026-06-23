"""
Profile depth scoring.
"""


def profile_depth_score(
    candidate
):

    history = candidate.get(
        "career_history",
        []
    )

    description_words = 0

    for role in history:

        description_words += len(

            role.get(
                "description",
                ""
            ).split()
        )

    project_count = len(
        candidate.get(
            "projects",
            []
        )
    )

    score = (

        min(
            description_words / 500,
            1.0
        )
        * 0.7

        +

        min(
            project_count / 5,
            1.0
        )
        * 0.3
    )

    return round(
        score,
        4
    )