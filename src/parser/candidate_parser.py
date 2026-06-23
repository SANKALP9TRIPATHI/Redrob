"""
Candidate parsing pipeline.
"""

from dataclasses import dataclass

from src.features.career_features import (
    extract_career_features
)

from src.features.behavioral_features import (
    extract_behavioral_features
)


@dataclass
class CandidateFeatures:

    candidate_id: str

    years_experience: float

    current_title: str

    current_company: str

    career_features: dict

    behavioral_features: dict


def build_candidate_features(
    candidate: dict
) -> CandidateFeatures:

    profile = candidate["profile"]

    return CandidateFeatures(

        candidate_id=
            candidate["candidate_id"],

        years_experience=
            profile.get(
                "years_of_experience",
                0
            ),

        current_title=
            profile.get(
                "current_title",
                ""
            ),

        current_company=
            profile.get(
                "current_company",
                ""
            ),

        career_features=
            extract_career_features(
                candidate
            ),

        behavioral_features=
            extract_behavioral_features(
                candidate
            )
    )