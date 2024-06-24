import pandas as pd
from opti_fit.dataset_utils import ALGORITHMS


def validate_hit_solution(df: pd.DataFrame, cutoffs: dict, expected_hits: dict):
    scores = df[ALGORITHMS].to_dict(orient="records")
    for count, hit in enumerate(scores):
        is_still_hit = any([hit[a] >= cutoffs[a] for a in ALGORITHMS])
        if expected_hits[count] is True:
            assert is_still_hit
        else:
            assert not is_still_hit

        if df["is_hit_true_hit"][count]:
            assert is_still_hit
