"""
Behavioral ranking.
"""


def compute_behavioral_score(
    profile
):

    behavior = (
        profile.features
        .behavioral_features
    )

    score = 0.0

    if behavior.get(
        "open_to_work"
    ):
        score += 0.25

    response_rate = behavior.get(
        "response_rate", 0
    )

    score += (
        min(response_rate, 1.0)
        * 0.30
    )

    completion = behavior.get(
        "interview_completion", 0
    )

    score += (
        min(completion, 1.0)
        * 0.20
    )

    notice = behavior.get(
        "notice_period_days",
        999
    )

    if notice <= 30:
        score += 0.25

    elif notice <= 60:
        score += 0.15

    return round(
        min(score, 1.0),
        4
    )