from pytest import mark

from opti_fit.models.relaxed_model import solve_relaxed_hit_model, solve_relaxed_payment_model
from opti_fit.utils.model_utils import (
    check_hit_solution,
    check_payment_solution,
)


@mark.parametrize("slack", [0.3, 0.7, 0.999])
def test_solve_relaxed_hit_model(simple_df, slack):
    # Arrange
    n_hits = sum(simple_df["is_hit_true_hit"])

    # Act
    cutoffs = solve_relaxed_hit_model(simple_df, solver_name="CBC", slack=slack)

    # Assert
    _, true_positives_removed = check_hit_solution(simple_df, cutoffs, validate=False)
    assert (n_hits - true_positives_removed) / n_hits >= slack


@mark.parametrize("slack", [0.3, 0.7, 0.999])
def test_solve_simple_payment_model_using_mip(simple_df, slack):
    # Act
    cutoffs = solve_relaxed_payment_model(simple_df, solver_name="CBC", slack=slack)

    # Assert
    n_payment_hits, true_positives_removed = check_payment_solution(simple_df, cutoffs, validate=False)
    n_total = n_payment_hits + true_positives_removed
    assert (n_total - true_positives_removed) / n_total >= slack
