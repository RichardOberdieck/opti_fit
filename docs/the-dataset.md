# The dataset

The dataset in this repository contains the real algorithm scores from the production environment in Banking Circle. The set is a compressed csv file, where each row represents one hit. The dataset has the following columns:

- **payment_case_id**: A unique identifier for each payment
- **is_payment_true_hit**: Whether the payment is a true hit or not
- **is_hit_true_hit**: Whether the hit is a true hit or not
- **regex_match**: Score of this hit for the algorithm REGEX_MATCH
- **jaro_winkler**: Score of this hit for the algorithm JARO_WINKLER
- **fuzz_ratio**: Score of this hit for the algorithm FUZZ_RATIO
- **fuzz_partial_ratio**: Score of this hit for the algorithm FUZZ_PARTIAL_RATIO
- **fuzz_token_sort_ratio**: Score of this hit for the algorithm FUZZ_TOKEN_SORT_RATIO
- **fuzz_partial_token_sort_ratio**: Score of this hit for the algorithm FUZZ_PARTIAL_TOKEN_SORT_RATIO

!!! note

    In the `read_dataset` function of the code, we round the scores to the second digits to reduce numerical issues. Especially since we are looking to calculate cutoffs, having 13 digits after the decimal will not be helpful.


## The dataset in numbers

- 853049 total hits, of which 4023 are true positive hits (0.47%)
- 379691 total payments, of which 2572 are true positives (0.68%)

## Hit distribution

On average, a payment that is a true hit has 3.87 hits associated with it, while a false positive only has 2.23. However, the distributions look remarkably similar:

```plotly
{"file_path": "hit_distribution_true_positive.json"}
```

```plotly
{"file_path": "hit_distribution_false_positive.json"}
```

This suggests that while there may be information to be gained from the number of hits for a given payment, it is not a clear avenue to pursue.
