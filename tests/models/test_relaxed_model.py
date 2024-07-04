from opti_fit.utils.model_utils import (
    check_hit_solution,
    check_payment_solution,
)
from opti_fit.models.simple_model import (
    solve_simple_hit_model,
    solve_simple_payment_model,
)


def test_solve_simple_model_using_mip(simple_df):
    # Act
    cutoffs = solve_simple_hit_model(simple_df, solver_name="CBC")

    # Assert expected hits and cutoffs are working as advertised
    check_hit_solution(simple_df, cutoffs, validate=True)


def test_solve_simple_payment_model_using_mip(simple_df):
    # Act
    cutoffs = solve_simple_payment_model(simple_df, solver_name="CBC")

    # Assert expected payment and cutoffs are working as advertised
    check_payment_solution(simple_df, cutoffs, validate=True)
