"""
Keyword stuffing detector.
"""


def keyword_stuffing_score(
    candidate,
    capability_evidence
):

    skill_count = len(
        candidate.get(
            "skills",
            []
        )
    )

    evidence_count = 0

    for evidence in (
        capability_evidence.values()
    ):

        evidence_count += len(
            evidence.role_evidence
        )

        evidence_count += len(
            evidence.project_evidence
        )

    if skill_count == 0:
        return 0

    ratio = (
        evidence_count
        /
        skill_count
    )

    return round(
        min(ratio, 1.0),
        4
    )