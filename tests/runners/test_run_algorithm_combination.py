from opti_fit.models.simple_model import solve_simple_hit_model
from opti_fit.runners.run_algorithm_combination import iterate_over_combinations


def test_run_algorithm_combination(simple_df):
    # Act
    iterate_over_combinations(simple_df, solve_simple_hit_model, solver_name="CBC")

    # Assert that we have an extra entry in cutoffs
    # assert len(ALGORITHMS) + 1 == len(cutoff_results)
