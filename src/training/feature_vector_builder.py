from src.models.feature_vector import (
    FeatureVector
)


def build_feature_vector(

    candidate_id,

    ranking_outputs
):

    return FeatureVector(

        candidate_id=candidate_id,

        fit_score=
            ranking_outputs["fit_score"],

        capability_score=
            ranking_outputs["capability_score"],

        career_score=
            ranking_outputs["career_score"],

        behavioral_score=
            ranking_outputs["behavior_score"],

        founder_fit_score=
            ranking_outputs["founder_fit"],

        evidence_strength=
            ranking_outputs["evidence_strength"],

        profile_depth=
            ranking_outputs["profile_depth"],

        keyword_authenticity=
            ranking_outputs["keyword_authenticity"],

        integrity_score=
            ranking_outputs["integrity_score"],

        semantic_match_score=
            ranking_outputs["semantic_match"],

        availability_multiplier=
            ranking_outputs[
                "availability_multiplier"
            ]
    )