from mip import Model

from opti_fit.utils.model_utils import (
    check_hit_solution,
    check_payment_solution,
)
from opti_fit.models.simple_model import (
    define_cutoff_constraints,
    define_hit_variables,
    solve_simple_combined_model,
    solve_simple_hit_model,
    solve_simple_payment_model,
)


def test_solve_simple_hit_model(simple_df):
    # Act
    cutoffs = solve_simple_hit_model(simple_df, solver_name="CBC")

    # Assert expected hits and cutoffs are working as advertised
    check_hit_solution(simple_df, cutoffs, validate=True)


def test_solve_simple_payment_model(simple_df):
    # Act
    cutoffs = solve_simple_payment_model(simple_df, solver_name="CBC")

    # Assert expected payment and cutoffs are working as advertised
    check_payment_solution(simple_df, cutoffs, validate=True)


def test_solve_simple_combined_model(simple_df):
    # Act
    cutoffs = solve_simple_combined_model(simple_df, solver_name="CBC")

    # Assert expected hit and payment and cutoffs are working as advertised
    check_hit_solution(simple_df, cutoffs, validate=True)
    check_payment_solution(simple_df, cutoffs, validate=True)


def test_define_hit_variables(simple_df):
    # Arrange
    model = Model(solver_name="CBC")
    algorithms = ["regex_match", "fuzz_ratio"]

    # Act
    x, y, z = define_hit_variables(model, simple_df, algorithms)

    # Assert
    assert set(algorithms) == set(x.keys())
    assert 15 == len(y)
    assert 8 == len(z)


def test_define_cutoff_constraints(simple_df):
    # Arrange
    model = Model(solver_name="CBC")
    algorithms = ["regex_match", "fuzz_ratio"]
    x, y, z = define_hit_variables(model, simple_df, algorithms)
    hit_id = 0

    # Act
    model = define_cutoff_constraints(model, simple_df.loc[0], x, y, z, algorithms, hit_id)

    # Assert
    assert 7 == len(model.constrs)
    assert "- y_regex_match,0 - y_fuzz_ratio,0 + z_0  <= - 0.0" == str(model.constrs[0].expr)
