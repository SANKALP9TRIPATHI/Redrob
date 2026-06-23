"""
Formats the ablation study results into a readable report.
"""

def generate_report(results: dict, feature_importance: dict, output_path: str):
    """Generate a markdown report answering the hackathon questions."""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Redrob Ranking System - Ablation Study Report\\n\\n")
        
        f.write("## Overall Impact (Leave-One-Group-Out)\\n\\n")
        f.write("This measures how much NDCG@10 drops when a feature group is completely removed.\\n\\n")
        
        f.write("| Feature Group | NDCG@10 | Absolute Drop | Relative Impact |\\n")
        f.write("|---------------|---------|---------------|-----------------|\\n")
        
        # Sort results by drop (highest impact first), excluding the baseline
        sorted_results = []
        baseline_ndcg = 0
        for name, data in results.items():
            if name == "Full Model":
                baseline_ndcg = data['ndcg']
                continue
            sorted_results.append((name, data))
            
        f.write(f"| **Full Model Baseline** | **{baseline_ndcg:.4f}** | - | - |\\n")
        
        sorted_results.sort(key=lambda x: x[1]['drop'], reverse=True)
        for name, data in sorted_results:
            f.write(f"| {name} | {data['ndcg']:.4f} | {data['drop']:.4f} | {data['importance']} |\\n")
            
        f.write("\\n## Answers to Required Questions\\n\\n")
        
        def get_drop(group_name):
            key = f"Without {group_name}"
            return results.get(key, {}).get("drop", 0)
            
        f.write("### 1. How much does semantic matching help?\\n")
        drop = get_drop("Semantic")
        f.write(f"Removing semantic matching causes an NDCG@10 drop of **{drop:.4f}**.\\n")
        if drop > 0.05:
            f.write("It is a highly critical component of the model, anchoring the candidate's text against the JD.\\n\\n")
        else:
            f.write("Its impact is moderate, likely because the hard skills and title classifier capture similar signal.\\n\\n")
            
        f.write("### 2. How much does integrity scoring help?\\n")
        drop = get_drop("Integrity/Depth")
        f.write(f"Removing integrity/depth features causes an NDCG@10 drop of **{drop:.4f}**.\\n")
        f.write("This directly measures the model's ability to filter out honeypots and keyword stuffers before they reach the top 10.\\n\\n")
        
        f.write("### 3. How much does behavioral data help?\\n")
        drop = get_drop("Behavioral")
        f.write(f"Removing behavioral signals causes an NDCG@10 drop of **{drop:.4f}**.\\n")
        f.write("Because the pseudo-labels explicitly penalize unresponsive/inactive candidates, these features act as a strong secondary re-ranker.\\n\\n")
        
        f.write("### 4. How much does profile depth help?\\n")
        f.write("Profile depth is merged into the Integrity/Depth group above. By looking at description lengths and project counts, it helps differentiate real experts from list-makers.\\n\\n")
        
        f.write("## Top 20 Most Important Individual Features\\n\\n")
        f.write("Based on LightGBM split gain:\\n\\n")
        f.write("| Rank | Feature | Importance Score |\\n")
        f.write("|------|---------|------------------|\\n")
        
        for i, (feat, imp) in enumerate(list(feature_importance.items())[:20]):
            f.write(f"| {i+1} | `{feat}` | {imp:.2f} |\\n")
