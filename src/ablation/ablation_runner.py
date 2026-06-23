"""
Ablation study framework.
Evaluates the contribution of different feature groups to the ranking model.
Answers the 4 specific questions required by the hackathon.
"""

import numpy as np
import pandas as pd
from src.models.lambdamart import RankerModel

def calculate_ndcg(y_true, y_score, k=10):
    """Calculate NDCG@k."""
    # This is a simplified version of NDCG for ablation comparison
    # Sort indices by predicted score
    order = np.argsort(y_score)[::-1]
    y_true_sorted = y_true[order]
    
    # Take top k
    y_true_topk = y_true_sorted[:k]
    
    # Calculate DCG
    discounts = np.log2(np.arange(k) + 2)
    dcg = np.sum((2**y_true_topk - 1) / discounts)
    
    # Calculate IDCG
    ideal_order = np.argsort(y_true)[::-1]
    ideal_topk = y_true[ideal_order][:k]
    idcg = np.sum((2**ideal_topk - 1) / discounts)
    
    if idcg == 0:
        return 0.0
    return dcg / idcg


class AblationRunner:
    def __init__(self, X: pd.DataFrame, y: np.ndarray):
        self.X = X
        self.y = y
        self.group = np.array([len(X)])  # Single query group
        
        # Define feature groups by prefixes
        self.feature_groups = {
            "Semantic": [c for c in X.columns if c.startswith("semantic_")],
            "Skills": [c for c in X.columns if c.startswith("skills_")],
            "Career": [c for c in X.columns if c.startswith("career_")],
            "Behavioral": [c for c in X.columns if c.startswith("beh_")],
            "Integrity/Depth": [c for c in X.columns if c.startswith("int_")]
        }

    def run_ablation(self):
        """Run the full ablation study."""
        print("\\n=== Starting Ablation Study ===")
        results = {}
        
        # 1. Baseline (Full Model)
        print("Training full baseline model...")
        model = RankerModel()
        model.train(self.X, self.y, self.group)
        preds = model.predict(self.X)
        baseline_ndcg = calculate_ndcg(self.y, preds, k=10)
        results["Full Model"] = {"ndcg": baseline_ndcg, "drop": 0.0}
        
        print(f"Baseline NDCG@10: {baseline_ndcg:.4f}")
        
        # 2. Leave-One-Group-Out Ablation
        for group_name, cols in self.feature_groups.items():
            if not cols:
                continue
                
            print(f"\\nTraining without {group_name} features ({len(cols)} features)...")
            
            # Remove features
            X_ablated = self.X.drop(columns=cols)
            
            # Train and evaluate
            model = RankerModel()
            model.train(X_ablated, self.y, self.group)
            preds = model.predict(X_ablated)
            
            ndcg = calculate_ndcg(self.y, preds, k=10)
            drop = baseline_ndcg - ndcg
            
            results[f"Without {group_name}"] = {
                "ndcg": ndcg,
                "drop": drop,
                "importance": f"-{drop/baseline_ndcg*100:.1f}%" if baseline_ndcg > 0 else "0%"
            }
            print(f"NDCG@10: {ndcg:.4f} (Drop: {drop:.4f})")
            
        return results, model.get_feature_importance()
