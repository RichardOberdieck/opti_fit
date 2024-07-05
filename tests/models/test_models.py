from opti_fit.models.models import get_model
from pytest import raises, mark


@mark.parametrize(
    "model_str, raises_value_error",
    [
        ("simple_hit", False),
        ("simple_payment", False),
        ("simple_combined", False),
        ("relaxed_hit", False),
        ("relaxed_payment", False),
        ("relaxed_combined", True),
    ],
)
def test_get_model(model_str, raises_value_error):
    # Act
    if raises_value_error:
        with raises(ValueError):
            get_model(model_str)
    else:  # Does not raise error
        get_model(model_str)
