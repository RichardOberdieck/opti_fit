from opti_fit.model_utils import (
    check_hit_solution,
    check_payment_solution,
)
from opti_fit.simple_model import (
    solve_simple_model_using_mip,
    solve_simple_payment_model_using_mip,
)


def test_solve_simple_model_using_mip(simple_df):
    # Act
    cutoffs = solve_simple_model_using_mip(simple_df)

    # Assert expected hits and cutoffs are working as advertised
    check_hit_solution(simple_df, cutoffs, validate=True)


def test_solve_simple_payment_model_using_mip(simple_df):
    # Act
    cutoffs = solve_simple_payment_model_using_mip(simple_df)

    # Assert expected payment and cutoffs are working as advertised
    check_payment_solution(simple_df, cutoffs, validate=True)
