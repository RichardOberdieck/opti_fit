import pandas as pd
from enum import Enum


class Algorithm(str, Enum):
    REGEX_MATCH = "regex_match"
    JARO_WINKLER = "jaro_winkler"
    FUZZ_RATIO = "fuzz_ratio"
    FUZZ_PARTIAL_RATIO = "fuzz_partial_ratio"
    FUZZ_TOKEN_SORT_RATIO = "fuzz_token_sort_ratio"
    FUZZ_PARTIAL_TOKEN_SORT_RATIO = "fuzz_partial_token_sort_ratio"


ALGORITHMS = [a for a in set(Algorithm)]  # Want a list of easy pandas code

CUTOFF_THRESHOLDS = {
    Algorithm.REGEX_MATCH: 90,
    Algorithm.JARO_WINKLER: 93,
    Algorithm.FUZZ_PARTIAL_TOKEN_SORT_RATIO: 100,
    Algorithm.FUZZ_TOKEN_SORT_RATIO: 84,
    Algorithm.FUZZ_PARTIAL_RATIO: 97,
    Algorithm.FUZZ_RATIO: 81,
}


def read_dataset(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, compression="gzip")
    _validate_dataset(df)
    return df


def _validate_dataset(df: pd.DataFrame) -> None:
    # Validation 1 - column names
    assert set(df.columns) == {
        "payment_id",
        "is_payment_true_hit",
        "is_hit_true_hit",
    }.union(ALGORITHMS)

    # Validation 2 - all scores are between 0 and 100
    assert df[ALGORITHMS].min(axis=None) >= 0
    assert df[ALGORITHMS].max(axis=None) <= 100


def remove_payment_hits_without_true_hits(df: pd.DataFrame) -> pd.DataFrame:
    pass
