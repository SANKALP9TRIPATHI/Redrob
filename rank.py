#!/usr/bin/env python3
"""
Main entry point for the Redrob Candidate Ranking System.
Implements the full pipeline: parsing -> features -> labeling -> training -> predicting -> submission.
"""

import argparse
import time
import os
import csv
import pandas as pd
import numpy as np
from pathlib import Path

from src.jd.jd_parser import parse_jd
from src.features.semantic_matcher import SemanticMatcher
from src.features.feature_pipeline import FeaturePipeline
from src.labeling.pseudo_labeler import PseudoLabeler
from src.models.lambdamart import RankerModel
from src.explanations.reasoning_engine import ReasoningEngine
from src.utils.data_loader import stream_candidates, load_candidates
from src.ablation.ablation_runner import AblationRunner
from src.ablation.ablation_report import generate_report


def parse_args():
    parser = argparse.ArgumentParser(description="Redrob Candidate Ranker")
    parser.add_argument("--candidates", type=str, required=True, help="Path to candidates.jsonl")
    parser.add_argument("--out", type=str, required=True, help="Path for output submission.csv")
    parser.add_argument("--ablation", action="store_true", help="Run ablation study")
    parser.add_argument("--sample", action="store_true", help="Run on a small sample for fast testing")
    return parser.parse_args()


def process_candidates(candidates_path, is_sample=False):
    """Load candidates and extract features."""
    jd = parse_jd()
    
    print("Initializing Semantic Matcher (loading model)...")
    semantic_matcher = SemanticMatcher(jd)
    
    print("Initializing Feature Pipeline...")
    pipeline = FeaturePipeline(jd, semantic_matcher)
    
    labeler = PseudoLabeler()
    
    features_list = []
    labels_list = []
    candidates_data = []
    
    print("Processing candidates...")
    start_time = time.time()
    
    # Load all at once for sample, stream for full
    max_cands = 100 if is_sample else None
    
    if is_sample or candidates_path.endswith('.json'):
        # For small sample
        candidates = load_candidates(candidates_path, max_candidates=max_cands)
        candidates_data.extend(candidates)
        batch_feats = pipeline.extract_features_batch(candidates)
        for feats in batch_feats:
            features_list.append(feats)
            labels_list.append(labeler.generate_label(feats))
        print(f"Processed {len(candidates)} candidates...")
    else:
        # For large JSONL stream
        for batch in stream_candidates(candidates_path, batch_size=5000):
            candidates_data.extend(batch)
            batch_feats = pipeline.extract_features_batch(batch)
            for feats in batch_feats:
                features_list.append(feats)
                labels_list.append(labeler.generate_label(feats))
            print(f"Processed {len(candidates_data)} candidates...")
            
    print(f"Feature extraction took {time.time() - start_time:.2f} seconds.")
    
    # Convert to DataFrame
    X = pd.DataFrame(features_list)
    y = np.array(labels_list)
    
    # Handle NaN/Inf
    X = X.fillna(0.0).replace([np.inf, -np.inf], 0.0)
    
    return X, y, candidates_data, jd


def main():
    args = parse_args()
    start_total = time.time()
    
    # 1. Feature Extraction & Labeling
    X, y, candidates_data, jd = process_candidates(args.candidates, args.sample)
    
    print(f"Data shape: {X.shape}, Label distribution: {np.bincount(y)}")
    
    # 2. Train Model
    print("\\nTraining LambdaMART model...")
    model = RankerModel()
    group = np.array([len(X)])
    model.train(X, y, group)
    
    # 3. Predict & Rank
    print("\\nPredicting scores...")
    scores = model.predict(X)
    
    # Sort by score descending
    ranked_indices = np.argsort(scores)[::-1]
    
    # We need top 100
    top_indices = ranked_indices[:100]
    
    # 4. Generate Reasoning & Save CSV
    print(f"\\nGenerating reasoning and saving to {args.out}...")
    reasoning_engine = ReasoningEngine(jd)
    
    # Prepare submission directory
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        
        for rank_zero_idx, idx in enumerate(top_indices):
            rank = rank_zero_idx + 1
            cand = candidates_data[idx]
            score = float(scores[idx])
            feats = X.iloc[idx].to_dict()
            
            # Use pseudo-label as base for final score to ensure monotonicity
            # LambdaMART outputs raw scores, we can normalize them or use them directly
            # For submission, they just need to be non-increasing.
            
            reasoning = reasoning_engine.generate_reasoning(cand, rank, feats)
            
            writer.writerow([
                cand["candidate_id"],
                rank,
                f"{score:.4f}",
                reasoning
            ])
            
    print(f"Submission saved to {args.out}")
    
    # 5. Optional Ablation Study
    if args.ablation:
        print("\\nRunning Ablation Study...")
        runner = AblationRunner(X, y)
        results, importance = runner.run_ablation()
        
        report_path = out_path.parent / "ablation_report.md"
        generate_report(results, importance, report_path)
        print(f"Ablation report saved to {report_path}")
        
    print(f"\\nTotal pipeline time: {time.time() - start_total:.2f} seconds.")


if __name__ == "__main__":
    main()
