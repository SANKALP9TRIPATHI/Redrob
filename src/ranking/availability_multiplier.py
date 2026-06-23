"""
Availability adjustment.
"""


def compute_availability_multiplier(
    behavioral_features
):

    multiplier = 1.0

    if behavioral_features.get(
        "open_to_work",
        False
    ):
        multiplier += 0.10

    response_rate = (
        behavioral_features.get(
            "response_rate",
            0
        )
    )

    multiplier += (
        response_rate * 0.10
    )

    notice = (
        behavioral_features.get(
            "notice_period_days",
            999
        )
    )

    if notice > 90:
        multiplier -= 0.10

    return max(
        0.75,
        min(multiplier, 1.25)
    )