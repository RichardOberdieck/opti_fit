from opti_fit.multiple_cutoff_model import solve_hit_model_with_multiple_cutoffs_using_mip


def test_solve_hit_model_with_multiple_cutoffs_using_mip(simple_df):
    # Act
    cutoff_results, hit_count = solve_hit_model_with_multiple_cutoffs_using_mip(simple_df)

    # Assert
    assert 45 == len(cutoff_results)
    assert 45 == len(hit_count)
