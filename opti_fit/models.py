from enum import Enum

from opti_fit.relaxed_model import solve_relaxed_hit_model
from opti_fit.simple_model import (
    solve_simple_hit_model,
    solve_simple_payment_model,
)
from opti_fit.multiple_cutoff_model import solve_hit_model_with_multiple_cutoffs


class Model(str, Enum):
    SIMPLE_HIT_MIP = "simple_hit_mip"
    SIMPLE_PAYMENT_MIP = "simple_payment_mip"
    MULTIPLE_HIT_MIP = "cutoff_combination_hit"
    RELAXED_TRUE_POSITIVE = "relaxed_true_positive"

    def run(self, *data) -> tuple[dict, dict]:
        match self.value:
            case "simple_hit_mip":
                return solve_simple_hit_model(*data)
            case "simple_payment_mip":
                return solve_simple_payment_model(*data)
            case "cutoff_combination_hit":
                return solve_hit_model_with_multiple_cutoffs(*data)
            case "relaxed_true_positive":
                return solve_relaxed_hit_model(*data)
            case _:
                raise ValueError("Undefined model")
