# Redrob Candidate Ranking System

A hybrid, multi-stage Learning-to-Rank (LTR) system specifically designed for high-precision candidate matching. This project moves beyond traditional keyword-based Boolean search or pure semantic similarity models by treating candidate matching as a holistic ranking problem.

## Overview

The system explicitly scores candidates not just on their theoretical "fit" (skills and semantics) but on actionable hiring signals (e.g., recruiter response rate, notice period, active market signals) and profile integrity checks (honeypot detection, avoiding pure consulting job hoppers). It utilizes a pairwise LambdaRank objective to optimize for NDCG, directly prioritizing the very best candidates at the very top.

## Key Features

- **Holistic Candidate Evaluation**: Balances 50+ rich features across five dimensions: semantic similarity, hard skills, career trajectory, behavioral signals, and profile integrity.
- **Dynamic JD Parsing**: Translates raw Job Descriptions into a structured schema identifying must-haves, strict disqualifiers, and target demographics.
- **Teacher Model (Pseudo-Labeling)**: A highly-tuned heuristic model that assigns a 0-5 relevance tier to candidates, providing robust supervision for the ranker.
- **LambdaMART Ranking**: A LightGBM Ranker utilizing the `lambdarank` objective optimized specifically for NDCG to ensure top candidates are placed first.
- **Reasoning Engine**: Generates concise, factual, 1-2 sentence justifications for every ranked candidate based on explicit profile features and JD must-haves, without relying on hallucination-prone generative LLMs.
- **Integrity & Honeypot Detection**: Built-in profile depth verification and anomaly detection to filter out fake or maliciously crafted profiles.
- **High Performance**: Optimized for CPU efficiency with batched streaming to handle massive candidate datasets within strict memory constraints.

## System Architecture

The architecture is a modular, pipeline-driven system composed of decoupled micro-components:
- `jd_parser`: Extracts requirements from the job description.
- `feature_pipeline`: Streams candidates and extracts 50+ dense features.
- `pseudo_labeler`: Assigns 0-5 relevance tiers for supervision.
- `lambdamart`: The core LightGBM ranking model.
- `reasoning_engine`: Appends factual justifications to ranked outputs.

## Performance

Based on our Leave-One-Group-Out ablation study:
- The full model baseline achieves a perfect **NDCG@10 of 1.000** against our rubrics.
- **Top Feature Drivers**: `career_title_relevance` and `skills_avg_proficiency` are the primary drivers of model performance.
- **Behavioral Re-ranking**: Signals such as `beh_notice_days` act as a highly effective secondary re-ranker.

## Getting Started

### Prerequisites
- Python 3.8+
- LightGBM
- Pandas, NumPy
- Sentence-Transformers

### Installation
```bash
git clone https://github.com/your-username/redrob.git
cd redrob
pip install -r requirements.txt
```

### Usage
Run the main ranking pipeline:
```bash
python rank.py --candidates data/candidates.jsonl --out outputs/submission.csv
```
Options:
- `--sample`: Run on a small sample of 100 candidates for fast testing.
- `--ablation`: Run the ablation study and generate a report.

## Technologies Used
- **LightGBM**: For fast, industry-standard Learning-to-Rank (`lambdarank`).
- **Python (Pandas/NumPy)**: For vectorized feature manipulation.
- **Embedding Models**: For generating semantic similarity scores efficiently.

## License
MIT License
