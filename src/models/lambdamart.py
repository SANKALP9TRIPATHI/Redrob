"""
LambdaMART model implementation using LightGBM.
Optimized for the Learning-to-Rank objective on CPU.
"""

import lightgbm as lgb
import numpy as np
import pandas as pd


class RankerModel:
    def __init__(self):
        # Hyperparameters tuned for LambdaMART on CPU
        self.params = {
            'objective': 'lambdarank',
            'metric': 'ndcg',
            'ndcg_eval_at': [10, 50, 100],
            'learning_rate': 0.05,
            'num_leaves': 63,
            'min_child_samples': 20,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'reg_alpha': 0.1,    # L1 regularization
            'reg_lambda': 1.0,   # L2 regularization
            'n_estimators': 300,
            'random_state': 42,
            'importance_type': 'gain',
            'n_jobs': 1  # Avoid macOS multiprocessing crashes
        }
        self.model = None
        self.feature_names = None

    def train(self, X: pd.DataFrame, y: np.ndarray, group: np.ndarray):
        """
        Train the LambdaMART model.
        X: Feature matrix
        y: Relevance labels (tiers 0-5)
        group: Array indicating number of items per query (we have 1 query: the JD)
        """
        self.feature_names = list(X.columns)
        
        # LightGBM LambdaMART limits query size to 10,000 items.
        # Since we are essentially doing pointwise training for 1 JD, we can split
        # our dataset into arbitrary chunks of 10,000 to satisfy the ranker constraint.
        n_rows = len(X)
        if n_rows > 10000:
            n_full = n_rows // 10000
            rem = n_rows % 10000
            if rem == 0:
                group = np.array([10000] * n_full)
            else:
                group = np.array([10000] * n_full + [rem])
        
        self.model = lgb.LGBMRanker(**self.params)
        
        print(f"Training LambdaMART on {len(X)} candidates with {len(self.feature_names)} features...")
        self.model.fit(
            X, 
            y,
            group=group
        )
        print("Training complete.")

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict ranking scores."""
        if self.model is None:
            raise ValueError("Model not trained yet.")
        
        # Guarantee feature order matches training
        X_pred = X[self.feature_names]
        return self.model.predict(X_pred)

    def get_feature_importance(self) -> dict:
        """Return feature importance map."""
        if self.model is None:
            return {}
            
        importances = self.model.feature_importances_
        
        # Sort by importance
        feat_imp = [
            (feat, float(imp)) 
            for feat, imp in zip(self.feature_names, importances)
        ]
        feat_imp.sort(key=lambda x: x[1], reverse=True)
        
        return {k: v for k, v in feat_imp}
