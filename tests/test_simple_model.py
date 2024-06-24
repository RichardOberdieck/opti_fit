import pandas as pd
from pytest import fixture

from opti_fit.dataset_utils import ALGORITHMS
from opti_fit.model_utils import (
    validate_cutoffs,
    validate_hit_solution,
    validate_payment_solution,
)
from opti_fit.simple_model import (
    solve_simple_model_using_mip,
    solve_simple_payment_model_using_mip,
)


@fixture
def simple_df():
    columns = ["payment_case_id", "is_payment_true_hit", "is_hit_true_hit"] + ALGORITHMS
    data = [
        (1, True, True, 100, 100, 100, 100, 100, 100),
        (1, True, False, 60, 70, 80, 75, 85, 90),
        (2, False, False, 95, 91, 90, 88, 92, 91),
        (3, False, False, 80, 90, 85, 75, 85, 90),
        (3, False, False, 10, 43, 66, 85, 89, 95),
        (3, False, False, 91, 80, 80, 92, 85, 90),
        (4, True, True, 91, 89, 92, 90, 88, 93),
        (4, True, False, 92, 90, 93, 95, 89, 88),
    ]
    df = pd.DataFrame(data=data, columns=columns)
    df.index.rename("hit_id", inplace=True)
    return df


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
