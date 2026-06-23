"""
Integrity confidence.
"""

from src.integrity.contradiction_detector import (
    detect_contradictions
)


def compute_integrity_score(
    candidate
):

    flags = detect_contradictions(
        candidate
    )

    confidence = 1.0

    confidence -= (
        len(flags) * 0.15
    )

    confidence = max(
        confidence,
        0.5
    )

    return {
        "score": confidence,
        "flags": flags
    }