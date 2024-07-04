from opti_fit.utils.dataset_utils import ALGORITHMS
from opti_fit.models.combination_model import solve_hit_model_with_multiple_cutoffs


def test_solve_hit_model_with_multiple_cutoffs_using_mip(simple_df):
    # Act
    cutoff_results = solve_hit_model_with_multiple_cutoffs(simple_df)

    # Assert that we have an extra entry in cutoffs
    assert len(ALGORITHMS) + 1 == len(cutoff_results)
