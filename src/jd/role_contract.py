"""
Role contract representation.
"""

from dataclasses import dataclass, field


@dataclass
class RoleContract:

    role_name: str

    must_have_capabilities: list[str] = field(
        default_factory=list
    )

    nice_to_have_capabilities: list[str] = field(
        default_factory=list
    )

    behavioral_preferences: list[str] = field(
        default_factory=list
    )

    disqualifiers: list[str] = field(
        default_factory=list
    )

    logistics_constraints: dict = field(
        default_factory=dict
    )