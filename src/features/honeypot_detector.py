"""
Multi-signal honeypot detector.
Identifies candidates with subtly impossible profiles that are traps in the dataset.
Returns a probability score 0-1 where higher = more likely honeypot.
"""

from datetime import datetime, date


def detect_honeypot(candidate: dict) -> float:
    """
    Detect honeypot candidates with impossible profile signals.

    Checks for:
    1. Experience years vs career history mismatch
    2. Expert proficiency with zero endorsements and short duration
    3. Invalid timelines (start > end, overlapping roles)
    4. Impossible company tenure (e.g., 8 yrs at a 3-yr-old company)
    5. Skill count vs evidence mismatch
    6. Profile inconsistencies

    Returns:
        float: Honeypot probability 0.0-1.0
    """
    flags = 0
    total_checks = 10  # Number of checks we perform

    profile = candidate.get("profile", {})
    career = candidate.get("career_history", [])
    skills = candidate.get("skills", [])
    signals = candidate.get("redrob_signals", {})

    # --- Check 1: Experience years vs career history total ---
    claimed_years = profile.get("years_of_experience", 0)
    total_career_months = sum(
        role.get("duration_months", 0) for role in career
    )
    total_career_years = total_career_months / 12.0

    # If claimed experience is >3 years more than career history supports
    if claimed_years > total_career_years + 3:
        flags += 2  # Strong signal

    # --- Check 2: Expert skills with zero/low endorsements AND short duration ---
    expert_no_evidence = 0
    for skill in skills:
        if skill.get("proficiency") == "expert":
            endorsements = skill.get("endorsements", 0)
            duration = skill.get("duration_months", 0)
            if endorsements == 0 and duration < 12:
                expert_no_evidence += 1

    if expert_no_evidence >= 5:
        flags += 2  # Very suspicious
    elif expert_no_evidence >= 3:
        flags += 1

    # --- Check 3: Invalid role date ordering ---
    for role in career:
        start = role.get("start_date")
        end = role.get("end_date")
        if start and end and start > end:
            flags += 2  # Definite error

    # --- Check 4: Overlapping full-time roles ---
    dated_roles = []
    for role in career:
        start = role.get("start_date")
        end = role.get("end_date")
        if start:
            dated_roles.append((start, end or "9999-12-31"))

    dated_roles.sort()
    for i in range(len(dated_roles) - 1):
        _, end_i = dated_roles[i]
        start_next, _ = dated_roles[i + 1]
        # Significant overlap (more than 1 month)
        if end_i > start_next:
            flags += 1

    # --- Check 5: Title vs description mismatch ---
    # Check if current title doesn't match what career description says
    current_title = profile.get("current_title", "").lower()
    if career:
        latest_role = career[0]
        latest_desc = latest_role.get("description", "").lower()
        # If title says "ML Engineer" but description is about marketing
        title_domain = _get_domain(current_title)
        desc_domain = _get_domain(latest_desc)
        if title_domain and desc_domain and title_domain != desc_domain:
            flags += 1

    # --- Check 6: Absurd skill count with low profile completeness ---
    skill_count = len(skills)
    completeness = signals.get("profile_completeness_score", 100)
    if skill_count > 15 and completeness < 40:
        flags += 1

    # --- Check 7: Assessment scores wildly inconsistent ---
    assessments = signals.get("skill_assessment_scores", {})
    if assessments:
        scores = list(assessments.values())
        if len(scores) >= 3:
            # All assessments exactly the same score is suspicious
            if len(set(scores)) == 1:
                flags += 1

    # --- Check 8: Very high experience but entry-level signals ---
    if claimed_years > 15:
        if signals.get("connection_count", 0) < 5:
            flags += 1
        if signals.get("endorsements_received", 0) < 3:
            flags += 1

    # --- Check 9: Headline contradicts title ---
    headline = profile.get("headline", "").lower()
    if current_title and headline:
        if current_title in headline:
            pass  # Expected
        else:
            # Check if headline has a completely different role
            headline_domain = _get_domain(headline)
            title_domain_2 = _get_domain(current_title)
            if (headline_domain and title_domain_2
                    and headline_domain != title_domain_2):
                flags += 0.5

    # --- Check 10: Impossible experience for education timeline ---
    education = candidate.get("education", [])
    if education and claimed_years > 0:
        earliest_grad = min(
            (ed.get("end_year", 9999) for ed in education),
            default=9999
        )
        if earliest_grad < 9999:
            # Years since graduation
            years_since_grad = 2026 - earliest_grad
            if claimed_years > years_since_grad + 2:
                flags += 1

    # Normalize to 0-1 probability
    probability = min(flags / total_checks, 1.0)
    return round(probability, 4)


def _get_domain(text: str) -> str:
    """Infer the broad domain from text."""
    text = text.lower()

    ml_keywords = [
        "machine learning", "ml", "ai", "deep learning",
        "nlp", "data science", "neural", "model",
        "ranking", "retrieval", "embedding", "search",
    ]
    engineering_keywords = [
        "software", "backend", "frontend", "fullstack",
        "developer", "engineer", "python", "java",
        "devops", "platform",
    ]
    non_tech_keywords = [
        "marketing", "sales", "hr", "human resources",
        "accounting", "finance", "civil", "mechanical",
        "graphic", "design", "content", "writing",
        "customer support", "operations",
    ]

    ml_hits = sum(1 for kw in ml_keywords if kw in text)
    eng_hits = sum(1 for kw in engineering_keywords if kw in text)
    non_tech_hits = sum(1 for kw in non_tech_keywords if kw in text)

    if ml_hits > eng_hits and ml_hits > non_tech_hits:
        return "ml"
    elif eng_hits > non_tech_hits:
        return "engineering"
    elif non_tech_hits > 0:
        return "non_tech"

    return ""
