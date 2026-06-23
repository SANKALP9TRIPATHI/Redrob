"""
Evidence strength scoring.
"""


def compute_evidence_strength(
    capability_evidence
):

    total = 0

    for evidence in (
        capability_evidence.values()
    ):

        total += (
            len(
                evidence.skill_evidence
            )
            * 1.0
        )

        total += (
            len(
                evidence.role_evidence
            )
            * 2.0
        )

        total += (
            len(
                evidence.project_evidence
            )
            * 3.0
        )

    return min(
        total / 20,
        1.0
    )