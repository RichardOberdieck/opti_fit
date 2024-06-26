import pandas as pd
from enum import Enum

from opti_fit.dataset_utils import ALGORITHMS
from opti_fit.simple_model import (
    solve_simple_model_using_mip,
    solve_simple_payment_model_using_mip,
)


class Model(str, Enum):
    SIMPLE_HIT_MIP = "simple_hit_mip"
    SIMPLE_PAYMENT_MIP = "simple_payment_mip"

    def run(self, *data) -> tuple[dict, dict]:
        match self.value:
            case "simple_hit_mip":
                return solve_simple_model_using_mip(*data)
            case "simple_payment_mip":
                return solve_simple_payment_model_using_mip(*data)
            case _:
                raise ValueError("Undefined model")


def validate_cutoffs(df: pd.DataFrame, cutoffs: dict[int, float], expected_hits: dict[int, float]) -> None:
    scores = df[ALGORITHMS].to_dict(orient="records")
    for count, hit in enumerate(scores):
        is_still_hit = any([hit[a] >= cutoffs[a] for a in ALGORITHMS])
        if expected_hits[count] is True:
            assert is_still_hit
        else:
            assert not is_still_hit


def check_hit_solution(df: pd.DataFrame, cutoffs: dict[Model, float], validate: bool = False) -> tuple[int, int]:
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


def check_payment_solution(df: pd.DataFrame, cutoffs: dict[Model, float], validate: bool = False) -> tuple[int, int]:
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


def analyze_performance(df: pd.DataFrame, cutoffs: dict[Model, float]) -> pd.DataFrame:
    n_hits, true_positive_hits_removed = check_hit_solution(df, cutoffs)
    n_payment_hits, true_positive_payments_removed = check_payment_solution(df, cutoffs)

    total_hits = df["is_hit_true_hit"].sum()
    total_payment_hits = df["is_payment_true_hit"].sum()

    data = [
        (
            "Payment",
            total_payment_hits,
            total_payment_hits - n_payment_hits,
            (total_payment_hits - n_payment_hits) / total_payment_hits,
            true_positive_payments_removed,
            true_positive_payments_removed / total_payment_hits,
        ),
        (
            "Hits",
            total_hits,
            total_hits - n_hits,
            (total_hits - n_hits) / total_hits,
            true_positive_hits_removed,
            true_positive_hits_removed / total_hits,
        ),
    ]

    return pd.DataFrame.from_records(
        data,
        columns=[
            "Type",
            "Total",
            "Removed False Positive [absolute]",
            "Removed False Positive [%]",
            "Removed True Positive [absolute]",
            "Removed True Positive [%]",
        ],
        index="Type",
    )
