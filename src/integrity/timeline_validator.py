"""
Timeline validation.
"""

from datetime import datetime


def validate_timeline(
    candidate
):

    flags = []

    history = candidate.get(
        "career_history",
        []
    )

    for role in history:

        start = role.get(
            "start_date"
        )

        end = role.get(
            "end_date"
        )

        if (
            start
            and end
            and start > end
        ):
            flags.append(
                "invalid_role_dates"
            )

    return flags