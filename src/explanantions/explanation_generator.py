"""
Explanation generation.
"""


def generate_explanation(
    profile,
    fit_result,
    integrity_result
):

    top_capabilities = []

    for capability, score in sorted(
        profile.capability_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]:

        if score > 0.5:
            top_capabilities.append(
                capability
            )

    capability_text = (
        ", ".join(top_capabilities)
        if top_capabilities
        else "general ML systems"
    )

    explanation = (

        f"Strong evidence for "
        f"{capability_text}. "
        f"Covers "
        f"{len(fit_result['coverage']['covered'])}"
        f"/"
        f"{len(fit_result['coverage']['covered']) + len(fit_result['coverage']['missing'])}"
        f" key requirements."
    )

    if integrity_result["flags"]:

        explanation += (
            " Some profile inconsistencies detected."
        )

    return explanation