"""
Behavioral feature extraction.
"""

from datetime import datetime


def extract_behavioral_features(
    candidate: dict
) -> dict:

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    return {

        "open_to_work":
            signals.get(
                "open_to_work_flag",
                False
            ),

        "response_rate":
            signals.get(
                "recruiter_response_rate",
                0
            ),

        "response_time_hours":
            signals.get(
                "avg_response_time_hours",
                999
            ),

        "notice_period_days":
            signals.get(
                "notice_period_days",
                999
            ),

        "github_activity":
            signals.get(
                "github_activity_score",
                -1
            ),

        "interview_completion":
            signals.get(
                "interview_completion_rate",
                0
            ),

        "offer_acceptance":
            signals.get(
                "offer_acceptance_rate",
                -1
            ),

        "saved_by_recruiters":
            signals.get(
                "saved_by_recruiters_30d",
                0
            ),

        "search_appearance":
            signals.get(
                "search_appearance_30d",
                0
            )
    }