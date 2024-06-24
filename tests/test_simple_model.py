from opti_fit.model_utils import (
    validate_cutoffs,
    validate_hit_solution,
    validate_payment_solution,
)
from opti_fit.simple_model import (
    solve_simple_model_using_mip,
    solve_simple_payment_model_using_mip,
)


def test_solve_simple_model_using_mip(simple_df):
    # Act
    cutoffs, expected_hits = solve_simple_model_using_mip(simple_df)

    # Assert expected hits and cutoffs are working as advertised
    validate_cutoffs(simple_df, cutoffs, expected_hits)
    validate_hit_solution(simple_df, cutoffs)


def test_solve_simple_payment_model_using_mip(simple_df):
    # Act
    cutoffs, expected_hits = solve_simple_payment_model_using_mip(simple_df)

    # Assert expected payment and cutoffs are working as advertised
    validate_cutoffs(simple_df, cutoffs, expected_hits)
    validate_payment_solution(simple_df, cutoffs)
