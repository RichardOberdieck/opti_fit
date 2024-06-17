import pandas as pd
from enum import Enum


class Algorithm(str, Enum):
    REGEX_MATCH = " Regex Match"
    JARO_WINKLER = " Jaro Winkler"
    FUZZ_RATIO = " Fuzz Ratio"
    FUZZ_PARTIAL_RATIO = " Fuzz Partial Ratio"
    FUZZ_TOKEN_SORT_RATIO = " Fuzz Token Sort Ratio"
    FUZZ_PARTIAL_TOKEN_SORT_RATIO = " Fuzz Partial Token Sort Ratio"


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
        "payment_case_id",
        " Fuzz Partial Token Sort Ratio",
        " Fuzz Token Sort Ratio",
        " Fuzz Ratio",
        " Fuzz Partial Ratio",
        " Jaro Winkler",
        " is_payment_true_hit",
        " is_hit_true_hit",
        " Regex Match",
    }

    # Validation 2 - all scores are between 0 and 100
    assert df[ALGORITHMS].min(axis=None) >= 0
    assert df[ALGORITHMS].max(axis=None) <= 100
