"""
Capability extraction.
"""

from collections import defaultdict

from src.taxonomy.capability_taxonomy import (
    CAPABILITY_TAXONOMY
)

from src.parser.skill_normalizer import (
    normalize_skill
)

from src.evidence.evidence_graph import (
    CapabilityEvidence,
    EvidenceNode
)


def extract_capabilities(candidate):

    capabilities = {}

    skills = [
        normalize_skill(skill)
        for skill in candidate.get("skills", [])
    ]

    role_text = " ".join(

        role.get("description", "")

        for role in candidate.get(
            "career_history",
            []
        )
    ).lower()

    for capability, keywords in (
        CAPABILITY_TAXONOMY.items()
    ):

        evidence = CapabilityEvidence(
            capability=capability
        )

        for skill in skills:

            if skill in keywords:

                evidence.skill_evidence.append(

                    EvidenceNode(
                        source_type="skill",
                        value=skill,
                        weight=1.0
                    )
                )

        for keyword in keywords:

            if keyword in role_text:

                evidence.role_evidence.append(

                    EvidenceNode(
                        source_type="role",
                        value=keyword,
                        weight=0.8
                    )
                )

        capabilities[capability] = evidence

    return capabilities