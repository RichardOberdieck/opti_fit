from opti_fit.utils.model_utils import check_hit_solution


def test_check_hit_solution(simple_df):
    # Arrange
    cutoffs = {
        "regex_match": 94,
        "jaro_winkler": 94,
        "fuzz_ratio": 94,
        "fuzz_partial_ratio": 94,
        "fuzz_token_sort_ratio": 94,
        "fuzz_partial_token_sort_ratio": 94,
    }

    # Act
    n_hits, true_positives_removed = check_hit_solution(simple_df, cutoffs, False)

    # Assert
    assert 4 == n_hits
    assert 1 == true_positives_removed
