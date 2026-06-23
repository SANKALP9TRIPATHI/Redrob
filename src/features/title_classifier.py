"""
Title relevance classifier.
Maps candidate titles to a 0.0-1.0 relevance score based on the JD requirements.
Uses both exact matching and fuzzy keyword matching.
"""

import re

# Title relevance tiers based on JD analysis
# Tier 1.0 — Direct match titles
TIER_1_PATTERNS = [
    r"ml engineer", r"machine learning engineer",
    r"ai engineer", r"artificial intelligence engineer",
    r"nlp engineer", r"natural language processing",
    r"search engineer", r"ranking engineer",
    r"recommendation engineer", r"retrieval engineer",
    r"applied scientist", r"applied ml",
    r"ml research engineer",
    r"information retrieval",
]

# Tier 0.8 — Strong adjacent
TIER_08_PATTERNS = [
    r"data scientist", r"senior data scientist",
    r"research scientist",
    r"ml ops", r"mlops engineer",
    r"deep learning engineer",
    r"computer vision engineer",  # still ML
]

# Tier 0.5 — Could be a fit with right skills
TIER_05_PATTERNS = [
    r"backend engineer", r"software engineer",
    r"data engineer", r"platform engineer",
    r"full.?stack engineer", r"full.?stack developer",
    r"software developer", r"python developer",
    r"analytics engineer",
    r"devops engineer",
]

# Tier 0.3 — Unlikely but not impossible
TIER_03_PATTERNS = [
    r"tech lead", r"engineering manager",
    r"technical architect", r"solution architect",
    r"product manager",
    r"consultant",
]

# Tier 0.0 — Explicitly wrong domain
TIER_0_PATTERNS = [
    r"marketing manager", r"hr manager", r"human resources",
    r"accountant", r"financial analyst", r"finance manager",
    r"civil engineer", r"mechanical engineer", r"electrical engineer",
    r"graphic designer", r"ui designer", r"ux designer",
    r"content writer", r"copywriter", r"editor",
    r"sales executive", r"sales manager", r"business development",
    r"customer support", r"customer service",
    r"operations manager", r"supply chain",
    r"teacher", r"professor", r"lecturer",
    r"doctor", r"nurse", r"pharmacist",
    r"lawyer", r"legal", r"compliance",
]


def classify_title(title: str) -> float:
    """
    Classify a job title into a relevance score 0.0-1.0.

    Returns:
        float: Relevance score where 1.0 = perfect match, 0.0 = completely irrelevant
    """
    if not title:
        return 0.0

    title_lower = title.lower().strip()

    # Check from most specific to least specific
    for pattern in TIER_1_PATTERNS:
        if re.search(pattern, title_lower):
            # Boost for "senior" prefix
            if re.search(r"(senior|staff|principal|lead)", title_lower):
                return 1.0
            if re.search(r"junior", title_lower):
                return 0.75
            return 0.9

    for pattern in TIER_08_PATTERNS:
        if re.search(pattern, title_lower):
            if re.search(r"(senior|staff|principal)", title_lower):
                return 0.85
            return 0.75

    for pattern in TIER_05_PATTERNS:
        if re.search(pattern, title_lower):
            if re.search(r"(senior|staff|principal)", title_lower):
                return 0.55
            return 0.45

    for pattern in TIER_03_PATTERNS:
        if re.search(pattern, title_lower):
            return 0.3

    for pattern in TIER_0_PATTERNS:
        if re.search(pattern, title_lower):
            return 0.05

    # Unknown title — slight default
    return 0.2


def classify_industry(industry: str) -> float:
    """
    Classify current industry relevance.
    """
    if not industry:
        return 0.3

    industry_lower = industry.lower()

    high_relevance = [
        "technology", "software", "internet", "ai",
        "machine learning", "data", "analytics",
        "saas", "cloud", "fintech",
    ]

    medium_relevance = [
        "it services", "information technology",
        "e-commerce", "telecommunications", "media",
        "financial services", "banking",
    ]

    low_relevance = [
        "manufacturing", "construction", "mining",
        "retail", "hospitality", "real estate",
        "healthcare", "pharmaceutical", "agriculture",
        "paper products", "textiles", "automotive",
    ]

    for kw in high_relevance:
        if kw in industry_lower:
            return 1.0

    for kw in medium_relevance:
        if kw in industry_lower:
            return 0.6

    for kw in low_relevance:
        if kw in industry_lower:
            return 0.2

    return 0.4
