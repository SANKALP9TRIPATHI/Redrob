"""
Heuristic self-labeling engine.
Generates pseudo ground truth labels (tiers 0-5) for LambdaMART training.
Acts as the "teacher" model based explicitly on the JD requirements and constraints.
"""


class PseudoLabeler:
    def __init__(self):
        pass
        
    def generate_label(self, features: dict) -> int:
        """
        Generate a relevance tier 0-5 based on extracted features.
        
        Tier 5: Perfect fit
        Tier 4: Strong fit
        Tier 3: Moderate fit
        Tier 2: Weak fit
        Tier 1: Poor fit
        Tier 0: No fit / Honeypot / Disqualified
        """
        
        # 1. Check strict disqualifiers (Tier 0)
        
        # Honeypot check
        if features.get("int_honeypot_prob", 0) > 0.5:
            return 0
            
        # Completely irrelevant title (e.g., Marketing Manager)
        if features.get("career_title_relevance", 0) < 0.2:
            return 0
            
        # Pure consulting career (explicitly disqualified in JD)
        if features.get("career_consulting_only", 0) > 0.5:
            return 0
            
        # Job hopper (explicitly disqualified)
        if features.get("career_job_hopper", 0) > 0.5:
            return 0
            
        # 2. Score positive signals
        
        score = 0.0
        
        # Semantic match contribution (0-2 points)
        sem_sim = features.get("semantic_combined_sim", 0)
        if sem_sim > 0.6: score += 2.0
        elif sem_sim > 0.4: score += 1.0
        elif sem_sim > 0.2: score += 0.5
        
        # Title relevance (0-2 points)
        title_rel = features.get("career_title_relevance", 0)
        if title_rel >= 0.9: score += 2.0
        elif title_rel >= 0.7: score += 1.5
        elif title_rel >= 0.4: score += 0.5
        
        # Must-have skills (0-2 points)
        mh_cov = features.get("skills_must_have_coverage", 0)
        if mh_cov >= 0.8: score += 2.0
        elif mh_cov >= 0.6: score += 1.5
        elif mh_cov >= 0.4: score += 1.0
        elif mh_cov >= 0.2: score += 0.5
        
        # Experience sweet spot (0-1 points)
        if features.get("career_exp_in_range", 0) > 0.5:
            score += 1.0
            
        # Product company experience (0-1 points)
        if features.get("career_has_product", 0) > 0.5:
            score += 1.0
            
        # Behavioral multipliers (cap at +1 point)
        beh_bonus = 0.0
        if features.get("beh_response_rate", 0) > 0.5: beh_bonus += 0.5
        if features.get("beh_open_to_work", 0) > 0.5: beh_bonus += 0.5
        score += min(beh_bonus, 1.0)
        
        # 3. Map continuous score to tiers
        
        # Max possible score is ~9.0
        
        if score >= 7.5:
            tier = 5
        elif score >= 6.0:
            tier = 4
        elif score >= 4.5:
            tier = 3
        elif score >= 3.0:
            tier = 2
        elif score >= 1.5:
            tier = 1
        else:
            tier = 0
            
        # 4. Final adjustments
        
        # Strongly penalize inactive/unresponsive candidates
        if features.get("beh_response_rate", 1.0) < 0.1 and tier > 1:
            tier -= 1
        if features.get("beh_notice_days", 0) > 60 and tier > 2:
            tier -= 1
            
        return max(0, min(5, tier))
