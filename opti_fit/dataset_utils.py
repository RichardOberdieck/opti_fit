import pandas as pd
import numpy as np
from enum import Enum


class Algorithm(str, Enum):
    REGEX_MATCH = "regex_match"
    JARO_WINKLER = "jaro_winkler"
    FUZZ_RATIO = "fuzz_ratio"
    FUZZ_PARTIAL_RATIO = "fuzz_partial_ratio"
    FUZZ_TOKEN_SORT_RATIO = "fuzz_token_sort_ratio"
    FUZZ_PARTIAL_TOKEN_SORT_RATIO = "fuzz_partial_token_sort_ratio"


ALGORITHMS = [a for a in set(Algorithm)]  # Want a list of easy pandas code
OTHER = ["payment_case_id", "is_payment_true_hit", "is_hit_true_hit"]

CUTOFF_THRESHOLDS = {
    Algorithm.REGEX_MATCH: 90,
    Algorithm.JARO_WINKLER: 93,
    Algorithm.FUZZ_PARTIAL_TOKEN_SORT_RATIO: 100,
    Algorithm.FUZZ_TOKEN_SORT_RATIO: 84,
    Algorithm.FUZZ_PARTIAL_RATIO: 97,
    Algorithm.FUZZ_RATIO: 81,
}


data_types = {
    "payment_case_id": np.int64,
    "is_payment_true_hit": np.bool,
    "is_hit_true_hit": np.bool,
    "regex_match": np.float64,
    "jaro_winkler": np.float64,
    "fuzz_ratio": np.float64,
    "fuzz_partial_ratio": np.float64,
    "fuzz_token_sort_ratio": np.float64,
    "fuzz_partial_token_sort_ratio": np.float64,
}


def read_dataset(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, compression="gzip", dtype=data_types)
    df.index.rename("hit_id", inplace=True)
    _validate_dataset(df)
    return df


def _validate_dataset(df: pd.DataFrame) -> None:
    # Validation 1 - column names
    assert set(df.columns) == set(OTHER).union(ALGORITHMS)

    # Validation 2 - all scores are between 0 and 100
    assert df[ALGORITHMS].min(axis=None) >= 0
    assert df[ALGORITHMS].max(axis=None) <= 100

    # Validation 3 - if payment is a hit, it has to have at least one true hit. If it is not, all hits have to be false positives
    payment_df = df[["payment_case_id", "is_payment_true_hit"]]
    payment_df = payment_df.drop_duplicates()
    series_grouped = df.groupby("payment_case_id", group_keys=True)["is_hit_true_hit"].apply(lambda x: x)
    verify = payment_df.apply(
        lambda row: series_grouped[row["payment_case_id"]].any() == row["is_payment_true_hit"],
        axis=1,
    )
    assert verify.all()
