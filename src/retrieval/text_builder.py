"""
Build embedding text from candidate profile.
"""


def build_candidate_text(candidate):

    profile = candidate.get("profile", {})

    headline = profile.get(
        "current_title",
        ""
    )

    skills = candidate.get(
        "skills",
        []
    )

    role_descriptions = []

    for role in candidate.get(
        "career_history",
        []
    ):

        role_descriptions.append(
            role.get(
                "description",
                ""
            )
        )

    text = " ".join([
        headline,
        " ".join(skills),
        " ".join(role_descriptions)
    ])

    return text