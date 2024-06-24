import pandas as pd
from enum import Enum

from opti_fit.dataset_utils import ALGORITHMS
from opti_fit.simple_model import solve_simple_model_using_mip


class Model(str, Enum):
    SIMPLE_HIT_MIP = "simple_hit_mip"

    def run(self, *data) -> tuple[dict, dict]:
        match self.value:
            case "simple_hit_mip":
                return solve_simple_model_using_mip(*data)
            case _:
                raise ValueError("Undefined model")


def validate_cutoffs(
    df: pd.DataFrame, cutoffs: dict[int, float], expected_hits: dict[int, float]
) -> None:
    scores = df[ALGORITHMS].to_dict(orient="records")
    for count, hit in enumerate(scores):
        is_still_hit = any([hit[a] >= cutoffs[a] for a in ALGORITHMS])
        if expected_hits[count] is True:
            assert is_still_hit
        else:
            assert not is_still_hit


def validate_hit_solution(df: pd.DataFrame, cutoffs: dict[int, float]) -> None:
    for _, row in df.iterrows():
        is_still_hit = any([row[a] >= cutoffs[a] for a in ALGORITHMS])
        if row["is_hit_true_hit"]:
            assert is_still_hit


def validate_payment_solution(df: pd.DataFrame, cutoffs: dict[int, float]) -> None:
    payment_df = df.groupby("payment_case_id", group_keys=True)[
        ["is_payment_true_hit"]
    ].apply(lambda row: row)
    payment_ids = payment_df.index.get_level_values("payment_case_id").unique()
    for payment_id in payment_ids:
        hit_df = payment_df.loc[payment_id]
        is_payment_still_hit = any(
            [
                any([df.loc[hit_id, a] >= cutoffs[a] for a in ALGORITHMS])
                for hit_id in hit_df.index
            ]
        )

        if hit_df["is_payment_true_hit"].any():
            assert is_payment_still_hit
