from dataclasses import dataclass


@dataclass
class FeatureVector:

    candidate_id: str

    fit_score: float

    capability_score: float

    career_score: float

    behavioral_score: float

    founder_fit_score: float

    evidence_strength: float

    profile_depth: float

    keyword_authenticity: float

    integrity_score: float

    semantic_match_score: float

    availability_multiplier: float

    target_label: int | None = None