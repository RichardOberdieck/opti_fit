from pytest import fixture

from opti_fit.utils.model_utils import analyze_performance, check_hit_solution, check_payment_solution


@fixture
def cutoffs():
    return {
        "regex_match": 94,
        "jaro_winkler": 94,
        "fuzz_ratio": 94,
        "fuzz_partial_ratio": 94,
        "fuzz_token_sort_ratio": 94,
        "fuzz_partial_token_sort_ratio": 94,
    }


def test_check_hit_solution(simple_df, cutoffs):
    # Act
    n_hits, true_positives_removed, n_true_positives_hits = check_hit_solution(simple_df, cutoffs, False)

    # Assert
    assert 4 == n_hits
    assert 1 == true_positives_removed
    assert 2 == n_true_positives_hits


def test_check_payment_solution(simple_df, cutoffs):
    # Act
    n_payment_hits, true_positives_removed, n_true_positives_payments = check_payment_solution(
        simple_df, cutoffs, False
    )

    # Assert
    assert 4 == n_payment_hits
    assert 0 == true_positives_removed
    assert 2 == n_true_positives_payments


def test_analyze_performance(simple_df, cutoffs):
    # Act
    df = analyze_performance(simple_df, cutoffs)

    # Assert
    assert 2 == len(df)
    assert 2 == df.loc["Payment", "Total True Positive"]
    assert 0 == df.loc["Payment", "Removed True Positive [absolute]"]
    assert 2 == df.loc["Hits", "Total True Positive"]
    assert 1 == df.loc["Hits", "Removed True Positive [absolute]"]
