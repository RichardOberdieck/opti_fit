import hashlib
import pandas as pd


OVERVIEW_COLUMNS = ["payment_case_id", "is_payment_true_hit", "is_hit_true_hit"]


def read_dataset(filename: str, validate: bool = True) -> pd.DataFrame:
    df = pd.read_csv(filename, compression="gzip")
    df.index.rename("hit_id", inplace=True)
    if validate:
        _validate_dataset(df)
    df = round_scores(df)
    return df


def _validate_dataset(df: pd.DataFrame) -> None:
    # Validation 1 - column names
    assert set(df.columns).intersection(set(OVERVIEW_COLUMNS)) == set(OVERVIEW_COLUMNS)

    algorithms = get_algorithms_from_df(df)

    # Validation 2 - all scores are between 0 and 100
    assert df[algorithms].min(axis=None) >= 0
    assert df[algorithms].max(axis=None) <= 100

    # Validation 3 - if payment is a hit, it has to have at least one true hit. If it is not, all hits have to be false positives
    payment_df = df[["payment_case_id", "is_payment_true_hit"]]
    payment_df = payment_df.drop_duplicates()
    series_grouped = df.groupby("payment_case_id", group_keys=True)["is_hit_true_hit"].apply(lambda x: x)
    verify = payment_df.apply(
        lambda row: series_grouped[row["payment_case_id"]].any() == row["is_payment_true_hit"],
        axis=1,
    )
    assert verify.all()


def get_algorithms_from_df(df: pd.DataFrame) -> list[str]:
    return sorted([col for col in df.columns if col not in OVERVIEW_COLUMNS])


def round_scores(df: pd.DataFrame) -> pd.DataFrame:
    algorithms = get_algorithms_from_df(df)
    for algorithm in algorithms:
        df[algorithm] = df[algorithm].apply(lambda row: round(row, 2))
    return df


def get_hash(df: pd.DataFrame) -> str:
    return hashlib.sha1(pd.util.hash_pandas_object(df).values).hexdigest()
