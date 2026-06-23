"""
Reasoning engine.
Generates 1-2 sentence justifications for ranked candidates based on profile facts.
Ensures no hallucinations and highlights JD-specific connections.
"""

from src.jd.jd_parser import JDRequirements


class ReasoningEngine:
    def __init__(self, jd: JDRequirements):
        self.jd = jd
        self.must_haves = set(k.lower() for k in jd.must_have_keywords)

    def generate_reasoning(self, candidate: dict, rank: int, features: dict) -> str:
        """
        Generate reasoning specific to the candidate and their assigned rank.
        Top ranks get more glowing reasoning; lower ranks get more qualified reasoning.
        """
        profile = candidate.get("profile", {})
        title = profile.get("current_title", "Professional")
        years = profile.get("years_of_experience", 0)
        
        # Extract actual matched skills to prevent hallucination
        matched_must_haves = []
        all_skills = [s.get("name", "") for s in candidate.get("skills", [])]
        for skill in all_skills:
            if any(mh in skill.lower() for mh in self.must_haves):
                matched_must_haves.append(skill)
                
        # Limit to 2 skills for brevity
        matched_must_haves = list(set(matched_must_haves))
        skill_str = ""
        if matched_must_haves:
            skill_str = f" with expertise in {', '.join(matched_must_haves[:2])}"
            
        # Behavior signal
        signals = candidate.get("redrob_signals", {})
        response_rate = signals.get("recruiter_response_rate", 0)
        beh_str = f" (Response rate: {response_rate:.2f})."
        if response_rate < 0.2:
            beh_str = f", though low response rate ({response_rate:.2f}) is a concern."
            
        # Tone matches rank
        if rank <= 20:
            if features.get("int_honeypot_prob", 0) > 0.5:
                # We shouldn't rank honeypots this high, but if we do, call it out
                return f"Ranked high despite anomalies. {title} with {years} yrs{skill_str}."
                
            return f"Strong fit: {title} with {years} yrs relevant experience{skill_str}{beh_str}"
            
        elif rank <= 50:
            return f"Solid candidate: {title} ({years} yrs){skill_str}{beh_str}"
            
        else:
            return f"{title} with {years} yrs experience{skill_str}{beh_str}"
