from typing import Callable

from opti_fit.models.relaxed_model import solve_relaxed_hit_model, solve_relaxed_payment_model
from opti_fit.models.simple_model import (
    solve_simple_combined_model,
    solve_simple_hit_model,
    solve_simple_payment_model,
)


def get_model(model_str: str) -> Callable:
    match model_str:
        case "simple_hit":
            return solve_simple_hit_model
        case "simple_payment":
            return solve_simple_payment_model
        case "simple_combined":
            return solve_simple_combined_model
        case "relaxed_hit":
            return solve_relaxed_hit_model
        case "relaxed_payment":
            return solve_relaxed_payment_model
        case _:
            raise ValueError("Undefined model")
