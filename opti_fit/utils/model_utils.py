import pandas as pd

from opti_fit.utils.dataset_utils import get_algorithms_from_df


TIMELIMIT = 10800  # In seconds
DEFAULT_SEED = 0
PERFORMANCE_COLUMNS = [
    "element",
    "total",
    "total_true_positive",
    "removed_false_positive_absolute",
    "removed_false_positive_percent",
    "removed_true_positive_absolute",
    "removed_true_positive_percent",
]


def check_hit_solution(df: pd.DataFrame, cutoffs, validate: bool = False) -> tuple[int, int, int]:
    n_hits = 0
    true_positives_removed = 0
    n_true_positives = 0
    algorithms = get_algorithms_from_df(df)
    for _, row in df.iterrows():
        is_still_hit = any([row[a] >= cutoffs[a] for a in algorithms])
        n_hits += is_still_hit
        if row["is_hit_true_hit"]:
            n_true_positives += 1
            if validate:
                assert is_still_hit
            if not is_still_hit:
                true_positives_removed += 1

    return n_hits, true_positives_removed, n_true_positives


def check_payment_solution(df: pd.DataFrame, cutoffs, validate: bool = False) -> tuple[int, int, int]:
    payment_df = df.groupby("payment_case_id", group_keys=True)[["is_payment_true_hit"]].apply(lambda row: row)
    payment_ids = payment_df.index.get_level_values("payment_case_id").unique()
    n_payment_hits = 0
    true_positives_removed = 0
    n_true_positives = 0
    algorithms = get_algorithms_from_df(df)
    for payment_id in payment_ids:
        hit_df = payment_df.loc[payment_id]
        is_payment_still_hit = any(
            [any([df.loc[hit_id, a] >= cutoffs[a] for a in algorithms]) for hit_id in hit_df.index]
        )
        n_payment_hits += is_payment_still_hit

        if hit_df["is_payment_true_hit"].any():
            n_true_positives += 1
            if validate:
                assert is_payment_still_hit
            if not is_payment_still_hit:
                true_positives_removed += 1

    return n_payment_hits, true_positives_removed, n_true_positives


def analyze_performance(df: pd.DataFrame, cutoffs) -> pd.DataFrame:
    n_hits, true_positive_hits_removed, n_true_positives_hits = check_hit_solution(df, cutoffs)
    n_payment_hits, true_positive_payments_removed, n_true_positives_payments = check_payment_solution(df, cutoffs)

    n_payments = len(df["payment_case_id"].unique())

    data = [
        (
            "payments",
            n_payments,
            n_true_positives_payments,
            n_payments - n_payment_hits,
            100 * (n_payments - n_payment_hits) / n_payments,
            true_positive_payments_removed,
            100 * true_positive_payments_removed / n_true_positives_payments,
        ),
        (
            "hits",
            len(df),
            n_true_positives_hits,
            len(df) - n_hits,
            100 * (len(df) - n_hits) / len(df),
            true_positive_hits_removed,
            100 * true_positive_hits_removed / n_true_positives_hits,
        ),
    ]

    return pd.DataFrame.from_records(
        data,
        columns=PERFORMANCE_COLUMNS,
        index="element",
    )
