from opti_fit.models.relaxed_model import solve_relaxed_hit_model, solve_relaxed_payment_model
from opti_fit.models.simple_model import solve_simple_combined_model, solve_simple_hit_model, solve_simple_payment_model
from opti_fit.utils.runner_utils import parse_and_validate_runner_input
from pytest import mark, raises


@mark.parametrize(
    "model_name, solver_name, raises_exception",
    [
        ("simple_hit", "CBC", False),
        ("simple_that", "CBC", True),
        ("relaxed_payment", "GUROBI", False),
        ("simple_payment", "HIGHS", False),
        ("simple_combined", "CPLEX", True),
    ],
)
def test_parse_and_validate_runner_input_exception(model_name, solver_name, raises_exception):
    if raises_exception:
        with raises(ValueError):
            parse_and_validate_runner_input(model_name, solver_name, False)
    else:
        parse_and_validate_runner_input(model_name, solver_name, False)


@mark.parametrize(
    "model_name, expected_model",
    [
        ("simple_hit", solve_simple_hit_model),
        ("simple_payment", solve_simple_payment_model),
        ("simple_combined", solve_simple_combined_model),
        ("relaxed_hit", solve_relaxed_hit_model),
        ("relaxed_payment", solve_relaxed_payment_model),
    ],
)
def test_parse_and_validate_runner_input_model(model_name, expected_model):
    # Act
    model, _ = parse_and_validate_runner_input(model_name, full_dataset=False)

    # Assert
    assert expected_model == model
