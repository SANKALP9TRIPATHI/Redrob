"""
Career feature extraction.
"""

from statistics import mean


CONSULTING_COMPANIES = {
    "tcs",
    "infosys",
    "wipro",
    "accenture",
    "cognizant",
    "capgemini",
    "hcl"
}


def extract_career_features(candidate: dict) -> dict:

    history = candidate.get("career_history", [])

    total_months = sum(
        role.get("duration_months", 0)
        for role in history
    )

    num_companies = len(history)

    avg_tenure = (
        mean([
            role.get("duration_months", 0)
            for role in history
        ])
        if history else 0
    )

    consulting_months = 0

    for role in history:

        company = role.get("company", "").lower()

        if company in CONSULTING_COMPANIES:
            consulting_months += role.get(
                "duration_months", 0
            )

    return {

        "num_companies": num_companies,

        "total_months": total_months,

        "avg_tenure_months": avg_tenure,

        "consulting_months": consulting_months,

        "consulting_ratio":
            consulting_months / total_months
            if total_months else 0
    }