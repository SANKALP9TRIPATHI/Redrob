import pandas as pd

from dataclasses import asdict


def build_dataset(
    feature_vectors
):

    return pd.DataFrame(
        [
            asdict(x)
            for x in feature_vectors
        ]
    )