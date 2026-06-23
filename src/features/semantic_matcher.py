"""
Semantic matching using sentence-transformers.
Provides dense vector matching between JD and candidate profiles.
Optimized with batched inference for 100K candidates.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from src.jd.jd_parser import JDRequirements

MODEL_NAME = "all-MiniLM-L6-v2"

class SemanticMatcher:
    def __init__(self, jd: JDRequirements):
        self.model = SentenceTransformer(MODEL_NAME)
        self.jd = jd
        
        # Pre-compute JD embeddings
        self.jd_full_emb = self._encode(self.jd.jd_full_text)
        self.jd_summary_emb = self._encode(self.jd.jd_summary)
        
        # Encode specific capability keywords for finer matching
        self.must_have_embs = self._encode_batch_raw(self.jd.must_have_keywords)

    def _encode(self, text: str) -> np.ndarray:
        if not text:
            return np.zeros(384)
        emb = self.model.encode(text, normalize_embeddings=True)
        return emb

    def _encode_batch_raw(self, texts: list) -> np.ndarray:
        if not texts:
            return np.zeros((1, 384))
        return self.model.encode(texts, normalize_embeddings=True)

    def get_semantic_features_batch(self, batch: list) -> list:
        """Extract semantic similarity features for a batch of candidates to maximize GPU/CPU efficiency."""
        summaries = []
        career_descs = []
        skills_texts = []
        combined_texts = []
        
        for cand in batch:
            profile = cand.get("profile", {})
            headline = profile.get("headline", "")
            summary = profile.get("summary", "")
            
            career_desc = " ".join([
                role.get("description", "") for role in cand.get("career_history", [])
            ])
            
            skills_text = " ".join([
                skill.get("name", "") for skill in cand.get("skills", [])
            ])
            
            combined = f"{headline} {summary} {career_desc} {skills_text}".strip()
            
            summaries.append(summary)
            career_descs.append(career_desc)
            skills_texts.append(skills_text)
            combined_texts.append(combined)
            
        # Batch encode (uses optimized C++/Torch backend with internal batching)
        # batch_size=256 internally in sentence-transformers
        summary_embs = self.model.encode(summaries, normalize_embeddings=True, show_progress_bar=False)
        career_embs = self.model.encode(career_descs, normalize_embeddings=True, show_progress_bar=False)
        skills_embs = self.model.encode(skills_texts, normalize_embeddings=True, show_progress_bar=False)
        combined_embs = self.model.encode(combined_texts, normalize_embeddings=True, show_progress_bar=False)
        
        # Fast matrix multiplication for similarities
        sem_comb_sim = np.dot(combined_embs, self.jd_full_emb)
        sem_sum_sim = np.dot(summary_embs, self.jd_summary_emb)
        sem_car_sim = np.dot(career_embs, self.jd_full_emb)
        sem_skills_sim = np.dot(skills_embs, self.jd_full_emb)
        
        if len(self.must_have_embs) > 0:
            must_have_sims = np.dot(skills_embs, self.must_have_embs.T) # shape (batch_size, num_keywords)
            must_have_max = np.max(must_have_sims, axis=1)
            must_have_mean = np.mean(must_have_sims, axis=1)
            
            # Zero out where skills text was empty
            norms = np.linalg.norm(skills_embs, axis=1)
            mask = norms > 0
            must_have_max = must_have_max * mask
            must_have_mean = must_have_mean * mask
        else:
            must_have_max = np.zeros(len(batch))
            must_have_mean = np.zeros(len(batch))
            
        # Package results
        results = []
        for i in range(len(batch)):
            results.append({
                "semantic_combined_sim": float(sem_comb_sim[i]),
                "semantic_summary_sim": float(sem_sum_sim[i]),
                "semantic_career_sim": float(sem_car_sim[i]),
                "semantic_skills_sim": float(sem_skills_sim[i]),
                "semantic_must_have_max_sim": float(must_have_max[i]),
                "semantic_must_have_mean_sim": float(must_have_mean[i])
            })
            
        return results
