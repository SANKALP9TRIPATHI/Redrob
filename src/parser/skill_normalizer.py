"""
Skill normalization utilities.
"""

import re


SKILL_ALIASES = {

    "pine cone": "pinecone",
    "pinecone vector db": "pinecone",

    "sentence transformer": "sentence-transformers",
    "sentence transformers": "sentence-transformers",

    "open ai embeddings": "openai embeddings",

    "elastic search": "elasticsearch",

    "a/b testing": "ab testing",

    "learning-to-rank": "learning to rank",
}


def normalize_skill(skill: str) -> str:

    if not skill:
        return ""

    skill = skill.lower().strip()

    skill = re.sub(r"[^a-z0-9 ]", "", skill)

    skill = re.sub(r"\s+", " ", skill)

    return SKILL_ALIASES.get(skill, skill)