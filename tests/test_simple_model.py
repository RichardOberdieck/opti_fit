import pandas as pd

from opti_fit.dataset_utils import ALGORITHMS
from opti_fit.model_utils import validate_hit_solution
from opti_fit.simple_model import solve_simple_model_using_mip


def test_solve_simple_model_using_mip():
    # Arrange
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

    # Act
    cutoffs, expected_hits = solve_simple_model_using_mip(df)

    # Assert expected hits and cutoffs are working as advertised
    validate_hit_solution(df, cutoffs, expected_hits)
