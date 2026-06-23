"""
Master feature extraction pipeline.
Computes 50+ features across 5 groups for a candidate.
"""

from src.jd.jd_parser import JDRequirements
from src.features.title_classifier import classify_title, classify_industry
from src.features.honeypot_detector import detect_honeypot


class FeaturePipeline:
    def __init__(self, jd: JDRequirements, semantic_matcher=None):
        self.jd = jd
        self.semantic_matcher = semantic_matcher
        self._must_have_set = set(k.lower() for k in jd.must_have_keywords)
        self._nice_to_have_set = set(k.lower() for k in jd.nice_to_have_keywords)

    def extract_features_batch(self, batch: list) -> list:
        """Extract features for a batch of candidates using optimized operations."""
        results = []
        
        # 1. Get batched semantic features
        if self.semantic_matcher:
            sem_features_batch = self.semantic_matcher.get_semantic_features_batch(batch)
        else:
            sem_features_batch = [
                {
                    "semantic_combined_sim": 0.0,
                    "semantic_summary_sim": 0.0,
                    "semantic_career_sim": 0.0,
                    "semantic_skills_sim": 0.0,
                    "semantic_must_have_max_sim": 0.0,
                    "semantic_must_have_mean_sim": 0.0
                } for _ in batch
            ]
            
        # 2. Extract standard features and merge
        for cand, sem_feats in zip(batch, sem_features_batch):
            feats = {}
            feats.update(sem_feats)
            feats.update(self._extract_skills_capabilities(cand))
            feats.update(self._extract_career_trajectory(cand))
            feats.update(self._extract_behavioral_signals(cand))
            feats.update(self._extract_integrity_depth(cand))
            results.append(feats)
            
        return results

    def extract_features(self, candidate: dict) -> dict:
        """Extract all features for a single candidate."""
        features = {}
        
        # Group 1: Semantic Matching
        if self.semantic_matcher:
            features.update(self.semantic_matcher.get_semantic_features(candidate))
        else:
            # Fallback if no semantic matcher
            features.update({
                "semantic_combined_sim": 0.0,
                "semantic_summary_sim": 0.0,
                "semantic_career_sim": 0.0,
                "semantic_skills_sim": 0.0,
                "semantic_must_have_max_sim": 0.0,
                "semantic_must_have_mean_sim": 0.0
            })
            
        # Add other groups
        features.update(self._extract_skills_capabilities(candidate))
        features.update(self._extract_career_trajectory(candidate))
        features.update(self._extract_behavioral_signals(candidate))
        features.update(self._extract_integrity_depth(candidate))
        
        return features

    def _extract_skills_capabilities(self, candidate: dict) -> dict:
        features = {}
        skills = candidate.get("skills", [])
        
        must_have_count = 0
        nice_to_have_count = 0
        expert_count = 0
        total_prof = 0
        total_endors = 0
        total_dur = 0
        
        prof_map = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
        
        for skill in skills:
            name = skill.get("name", "").lower()
            prof = prof_map.get(skill.get("proficiency", ""), 0)
            endors = skill.get("endorsements", 0)
            dur = skill.get("duration_months", 0)
            
            if any(k in name for k in self._must_have_set):
                must_have_count += 1
            if any(k in name for k in self._nice_to_have_set):
                nice_to_have_count += 1
                
            if prof == 4:
                expert_count += 1
                
            total_prof += prof
            total_endors += endors
            total_dur += dur
            
        n_skills = max(len(skills), 1)
        
        features["skills_must_have_count"] = must_have_count
        features["skills_must_have_coverage"] = must_have_count / max(len(self.jd.must_have_capabilities), 1)
        features["skills_nice_to_have_count"] = nice_to_have_count
        features["skills_total_relevant"] = must_have_count + nice_to_have_count
        features["skills_irrelevant_ratio"] = 1.0 - (features["skills_total_relevant"] / n_skills)
        features["skills_avg_proficiency"] = total_prof / n_skills
        features["skills_expert_count"] = expert_count
        features["skills_avg_endorsements"] = total_endors / n_skills
        features["skills_total_endorsements"] = total_endors
        features["skills_avg_duration"] = total_dur / n_skills
        
        # Assessments
        signals = candidate.get("redrob_signals", {})
        assessments = signals.get("skill_assessment_scores", {})
        
        if assessments:
            scores = list(assessments.values())
            features["skills_assessment_mean"] = sum(scores) / len(scores)
            features["skills_assessment_count"] = len(scores)
        else:
            features["skills_assessment_mean"] = 0.0
            features["skills_assessment_count"] = 0
            
        features["skills_cert_count"] = len(candidate.get("certifications", []))
        
        return features

    def _extract_career_trajectory(self, candidate: dict) -> dict:
        features = {}
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        
        years_exp = profile.get("years_of_experience", 0)
        features["career_years_exp"] = years_exp
        
        # Sweet spot
        if self.jd.experience_min <= years_exp <= self.jd.experience_max:
            features["career_exp_in_range"] = 1.0
        else:
            features["career_exp_in_range"] = 0.0
            
        n_companies = len(history)
        features["career_num_companies"] = n_companies
        
        total_months = 0
        max_tenure = 0
        consulting_months = 0
        has_product = 0
        
        for role in history:
            dur = role.get("duration_months", 0)
            comp = role.get("company", "").lower()
            
            total_months += dur
            max_tenure = max(max_tenure, dur)
            
            is_consulting = any(c in comp for c in self.jd.consulting_companies)
            if is_consulting:
                consulting_months += dur
            else:
                has_product = 1
                
        features["career_avg_tenure"] = total_months / max(n_companies, 1)
        features["career_max_tenure"] = max_tenure
        
        # Job hopper flag
        features["career_job_hopper"] = 1.0 if (features["career_avg_tenure"] < 18 and n_companies > 3) else 0.0
        
        features["career_consulting_ratio"] = consulting_months / max(total_months, 1)
        features["career_consulting_only"] = 1.0 if (features["career_consulting_ratio"] > 0.9) else 0.0
        features["career_has_product"] = float(has_product)
        
        features["career_title_relevance"] = classify_title(profile.get("current_title", ""))
        features["career_industry_relevance"] = classify_industry(profile.get("current_industry", ""))
        
        return features

    def _extract_behavioral_signals(self, candidate: dict) -> dict:
        features = {}
        signals = candidate.get("redrob_signals", {})
        
        features["beh_open_to_work"] = float(signals.get("open_to_work_flag", False))
        features["beh_response_rate"] = signals.get("recruiter_response_rate", 0.0)
        
        # Lower is better for response time, impute high value if missing
        features["beh_response_time"] = signals.get("avg_response_time_hours", 720.0)
        
        features["beh_completeness"] = signals.get("profile_completeness_score", 0)
        features["beh_views_30d"] = signals.get("profile_views_received_30d", 0)
        features["beh_apps_30d"] = signals.get("applications_submitted_30d", 0)
        features["beh_connections"] = signals.get("connection_count", 0)
        
        notice = signals.get("notice_period_days", 90)
        features["beh_notice_days"] = notice
        features["beh_notice_short"] = 1.0 if notice <= self.jd.max_notice_preferred else 0.0
        
        features["beh_github"] = signals.get("github_activity_score", -1)
        features["beh_saved_30d"] = signals.get("saved_by_recruiters_30d", 0)
        features["beh_search_30d"] = signals.get("search_appearance_30d", 0)
        
        features["beh_interview_rate"] = signals.get("interview_completion_rate", 0.0)
        
        offer_rate = signals.get("offer_acceptance_rate", -1)
        features["beh_offer_rate"] = offer_rate if offer_rate >= 0 else 0.5
        
        verified = sum([
            signals.get("verified_email", False),
            signals.get("verified_phone", False),
            signals.get("linkedin_connected", False)
        ])
        features["beh_verified_count"] = verified
        features["beh_relocate"] = float(signals.get("willing_to_relocate", False))
        
        return features

    def _extract_integrity_depth(self, candidate: dict) -> dict:
        features = {}
        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        education = candidate.get("education", [])
        
        # Depth
        word_count = sum(len(role.get("description", "").split()) for role in history)
        features["int_desc_words"] = word_count
        features["int_avg_desc_len"] = word_count / max(len(history), 1)
        
        tier_map = {"tier_1": 1, "tier_2": 2, "tier_3": 3, "tier_4": 4, "unknown": 5}
        best_tier = 5
        for ed in education:
            t = tier_map.get(ed.get("tier", "unknown"), 5)
            best_tier = min(best_tier, t)
        features["int_edu_best_tier"] = best_tier
        
        features["int_has_certs"] = 1.0 if candidate.get("certifications") else 0.0
        
        # Honeypot detection
        features["int_honeypot_prob"] = detect_honeypot(candidate)
        
        return features
