"""
Capability scoring.
"""

from src.evidence.evidence_graph import (
    CapabilityEvidence
)


def score_capability(
    evidence: CapabilityEvidence
):

    score = 0

    score += (
        len(evidence.skill_evidence)
        * 0.40
    )

    score += (
        len(evidence.role_evidence)
        * 0.40
    )

    score += (
        len(
            evidence.assessment_evidence
        )
        * 0.20
    )

    return min(score, 1.0)


def score_all_capabilities(
    capability_dict
):

    return {

        capability:
            score_capability(
                evidence
            )

        for capability, evidence
        in capability_dict.items()
    }