"""
Behavioral twin separation.
"""


def behavioral_advantage_score(
    profile
):

    behavior = (
        profile.features
        .behavioral_features
    )

    score = 0

    if behavior.get(
        "open_to_work",
        False
    ):
        score += 0.30

    score += (
        behavior.get(
            "response_rate",
            0
        )
        * 0.30
    )

    score += (
        behavior.get(
            "interview_completion",
            0
        )
        * 0.20
    )

    notice = behavior.get(
        "notice_period_days",
        999
    )

    if notice <= 30:
        score += 0.20

    elif notice <= 60:
        score += 0.10

    return round(
        score,
        4
    )