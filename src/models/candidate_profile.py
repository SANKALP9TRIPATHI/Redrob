"""
Unified candidate profile.
"""

from dataclasses import dataclass

from src.parser.candidate_parser import (
    CandidateFeatures
)


@dataclass
class CandidateProfile:

    features: CandidateFeatures

    capability_evidence: dict

    capability_scores: dict

    integrity_flags: list


# from src.features.capability_extractor import (
#     extract_capabilities
# )

# from src.features.capability_scoring import (
#     score_all_capabilities
# )

# from src.models.candidate_profile import (
#     CandidateProfile
# )

# candidate_features = (
#     build_candidate_features(
#         candidate
#     )
# )

# capability_evidence = (
#     extract_capabilities(candidate)
# )

# capability_scores = (
#     score_all_capabilities(
#         capability_evidence
#     )
# )

# profile = CandidateProfile(
#     features=candidate_features,
#     capability_evidence=capability_evidence,
#     capability_scores=capability_scores,
#     integrity_flags=[]
# )