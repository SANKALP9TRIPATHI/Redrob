"""
Risk penalties.
"""


def compute_risk_penalty(
    integrity_result
):

    penalty = 0.0

    flags = integrity_result.get(
        "flags",
        []
    )

    penalty += (
        len(flags) * 0.05
    )

    return min(
        penalty,
        0.25
    )