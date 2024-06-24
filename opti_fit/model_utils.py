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
