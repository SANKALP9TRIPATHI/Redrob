"""
Requirement coverage scoring.
"""

from src.jd.role_contract import (
    RoleContract
)

from src.models.candidate_profile import (
    CandidateProfile
)


def compute_requirement_coverage(
    profile: CandidateProfile,
    role: RoleContract
):

    covered = []
    missing = []

    scores = profile.capability_scores

    for capability in (
        role.must_have_capabilities
    ):

        if scores.get(
            capability,
            0
        ) >= 0.5:

            covered.append(capability)

        else:

            missing.append(capability)

    coverage_ratio = (
        len(covered)
        /
        max(
            len(role.must_have_capabilities),
            1
        )
    )

    return {

        "coverage_ratio":
            coverage_ratio,

        "covered":
            covered,

        "missing":
            missing
    }