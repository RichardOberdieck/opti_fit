import hashlib
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


OVERVIEW_COLUMNS = ["payment_case_id", "is_payment_true_hit", "is_hit_true_hit"]
ALGORITHMS = [a for a in set(Algorithm)]  # Want a list of easy pandas code

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


def read_dataset(filename: str, validate: bool = True) -> pd.DataFrame:
    df = pd.read_csv(filename, compression="gzip", dtype=data_types)
    df.index.rename("hit_id", inplace=True)
    if validate:
        _validate_dataset(df)
    df = round_scores(df)
    return df


def _validate_dataset(df: pd.DataFrame) -> None:
    # Validation 1 - column names
    assert set(df.columns) == set(OVERVIEW_COLUMNS).union(ALGORITHMS)

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


def round_scores(df: pd.DataFrame) -> pd.DataFrame:
    for algorithm in ALGORITHMS:
        df[algorithm] = df[algorithm].apply(lambda row: round(row, 2))
    return df


def get_hash(df: pd.DataFrame) -> str:
    return hashlib.sha1(pd.util.hash_pandas_object(df).values).hexdigest()