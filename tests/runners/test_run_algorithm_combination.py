from pytest import approx

from opti_fit.models.simple_model import solve_simple_hit_model
from opti_fit.runners.run_algorithm_combination import get_string_representation, iterate_over_combinations, update_df
from opti_fit.utils.dataset_utils import Algorithm


def test_run_algorithm_combination(simple_df):
    # Act
    result = iterate_over_combinations(simple_df, solve_simple_hit_model, solver_name="CBC")

    # Assert
    assert 75 == len(result)


def test_get_string_representation():
    # Arrange
    algorithms = [Algorithm.REGEX_MATCH, Algorithm.FUZZ_RATIO]

    # Act
    string_rep = get_string_representation(algorithms)

    # Assert
    assert "regex_match,fuzz_ratio" == string_rep


def test_update_df(simple_df):
    # Arrange
    algorithms = [Algorithm.REGEX_MATCH, Algorithm.FUZZ_RATIO]
    weight = 0.3
    n_cols = len(simple_df.columns)

    # Act
    df = update_df(simple_df, algorithms, weight)

    # Assert
    assert n_cols + 1 == len(df.columns)
    assert simple_df.loc[1, "regex_match,fuzz_ratio"] == approx(83)
