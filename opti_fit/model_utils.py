import pandas as pd

from opti_fit.dataset_utils import ALGORITHMS


def validate_cutoffs(df: pd.DataFrame, cutoffs: dict[int, float], expected_hits: dict[int, float]) -> None:
    scores = df[ALGORITHMS].to_dict(orient="records")
    for count, hit in enumerate(scores):
        is_still_hit = any([hit[a] >= cutoffs[a] for a in ALGORITHMS])
        if expected_hits[count] is True:
            assert is_still_hit
        else:
            assert not is_still_hit


def check_hit_solution(df: pd.DataFrame, cutoffs, validate: bool = False) -> tuple[int, int]:
    n_hits = 0
    true_positives_removed = 0
    for _, row in df.iterrows():
        is_still_hit = any([row[a] >= cutoffs[a] for a in ALGORITHMS])
        n_hits += is_still_hit
        if row["is_hit_true_hit"]:
            if validate:
                assert is_still_hit
            if not is_still_hit:
                true_positives_removed += 1

    return n_hits, true_positives_removed


def check_payment_solution(df: pd.DataFrame, cutoffs, validate: bool = False) -> tuple[int, int]:
    payment_df = df.groupby("payment_case_id", group_keys=True)[["is_payment_true_hit"]].apply(lambda row: row)
    payment_ids = payment_df.index.get_level_values("payment_case_id").unique()
    n_payment_hits = 0
    true_positives_removed = 0
    for payment_id in payment_ids:
        hit_df = payment_df.loc[payment_id]
        is_payment_still_hit = any(
            [any([df.loc[hit_id, a] >= cutoffs[a] for a in ALGORITHMS]) for hit_id in hit_df.index]
        )
        n_payment_hits += is_payment_still_hit

        if hit_df["is_payment_true_hit"].any():
            if validate:
                assert is_payment_still_hit
            if not is_payment_still_hit:
                true_positives_removed += 1

    return n_payment_hits, true_positives_removed


def analyze_performance(df: pd.DataFrame, cutoffs) -> pd.DataFrame:
    n_hits, true_positive_hits_removed = check_hit_solution(df, cutoffs)
    n_payment_hits, true_positive_payments_removed = check_payment_solution(df, cutoffs)

    total_true_hits = df["is_hit_true_hit"].sum()
    total_true_payment_hits = df["is_payment_true_hit"].sum()
    n_payments = len(df["payment_case_id"].unique())

    data = [
        (
            "Payment",
            n_payments,
            total_true_payment_hits,
            n_payments - n_payment_hits,
            100 * (n_payments - n_payment_hits) / n_payments,
            true_positive_payments_removed,
            100 * true_positive_payments_removed / total_true_payment_hits,
        ),
        (
            "Hits",
            len(df),
            total_true_hits,
            len(df) - n_hits,
            100 * (len(df) - n_hits) / len(df),
            true_positive_hits_removed,
            100 * true_positive_hits_removed / total_true_hits,
        ),
    ]

    return pd.DataFrame.from_records(
        data,
        columns=[
            "Type",
            "Total",
            "Total True Positive",
            "Removed False Positive [absolute]",
            "Removed False Positive [%]",
            "Removed True Positive [absolute]",
            "Removed True Positive [%]",
        ],
        index="Type",
    )
