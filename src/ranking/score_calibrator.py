"""
Final score calibration.
"""


def calibrate_score(

    fit_score,

    career_score,

    founder_fit,

    behavior_score,

    evidence_strength,

    availability_multiplier,

    integrity_score,

    risk_penalty
):

    base = (

        0.35 * fit_score
        + 0.15 * career_score
        + 0.15 * founder_fit
        + 0.10 * behavior_score
        + 0.15 * evidence_strength
        + 0.10 * integrity_score
    )

    base *= availability_multiplier

    base -= risk_penalty

    return round(
        max(base, 0),
        4
    )