"""
Final ranking artifact.
"""

from dataclasses import dataclass


@dataclass
class RankingResult:

    candidate_id: str

    final_score: float

    fit_score: float

    capability_score: float

    career_score: float

    founder_fit_score: float

    behavioral_score: float

    evidence_strength: float

    integrity_score: float

    availability_multiplier: float

    risk_penalty: float

    explanation: str = ""