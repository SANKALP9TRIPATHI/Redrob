"""
Evidence graph structures.
"""

from dataclasses import dataclass, field


@dataclass
class EvidenceNode:

    source_type: str
    value: str
    weight: float


@dataclass
class CapabilityEvidence:

    capability: str

    skill_evidence: list[EvidenceNode] = field(
        default_factory=list
    )

    role_evidence: list[EvidenceNode] = field(
        default_factory=list
    )

    assessment_evidence: list[EvidenceNode] = field(
        default_factory=list
    )

    project_evidence: list[EvidenceNode] = field(
        default_factory=list
    )