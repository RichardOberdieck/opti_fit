# Results

## Simple model

The solution of the simple models already results in a significant reduction of false positives:

| Model        | FP hit reduction [%]  | FP payment reduction [%] |
| ------------ | --------------------- | -------------------------|
| Hit          |                 15.16 |                     9.66 |
| Payment      |                 25.56 |                    17.44 |
| Combined     |                 14.89 |                     9.70 |

The corresponding cutoffs are:

|                               |            Hit |       Payment |       Combined |
|:------------------------------|---------------:|--------------:|---------------:|
| regex_match                   |          91.68 |        91.68  |          91.68 |
| jaro_winkler                  |          88.43 |        93.28  |          92.97 |
| fuzz_ratio                    |          84.12 |        94.34  |          82.25 |
| fuzz_token_sort_ratio         |          81.20 |        81.44  |          81.02 |
| fuzz_partial_token_sort_ratio |          97.15 |        97.67  |          97.30 |
| fuzz_partial_ratio            |          97.31 |        98.97  |          97.31 |

!!! warning

    The payment-based model results in 66 true positive hits (1.64%) being missed.
