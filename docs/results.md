# Results

## Overview

- Just by applying the simple model results in a significant reduction of false positives:

| Model        | FP hit reduction [%]  | FP payment reduction [%] |
| ------------ | --------------------- | -------------------------|
| Hit          |                 15.16 |                     9.66 |
| Payment      |                   TBD |                      TBD |

- 



## Simple hit model

Performance:

| Type    |   Total |   Total True Positive |   Removed False Positive [absolute] |   Removed False Positive [%] |   Removed True Positive [absolute] |   Removed True Positive [%] |
|:--------|--------:|----------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|----------------------------:|
| Payment |  379691 |                  9967 |                               36684 |                      9.66154 |                                  0 |                           0 |
| Hits    |  853049 |                  4023 |                              129320 |                     15.1597  |                                  0 |                           0 |

Cutoffs:

|                               |   Cutoff value |
|:------------------------------|---------------:|
| regex_match                   |          91.68 |
| jaro_winkler                  |          88.43 |
| fuzz_ratio                    |          84.12 |
| fuzz_token_sort_ratio         |          81.2  |
| fuzz_partial_token_sort_ratio |          97.15 |
| fuzz_partial_ratio            |          97.31 |


|    |   removed_false_positive_hits_absolute |   removed_false_positive_hits_percent |   removed_true_positive_hits_absolute |   removed_true_positive_hits_percent |   removed_false_positive_payments_absolute |   removed_false_positive_payments_percent |   removed_true_positive_payments_absolute |   removed_true_positive_payments_percent |   cutoff_regex_match |   cutoff_jaro_winkler |   cutoff_fuzz_ratio |   cutoff_fuzz_partial_ratio |   cutoff_fuzz_token_sort_ratio |   cutoff_fuzz_partial_token_sort_ratio |
|---:|---------------------------------------:|--------------------------------------:|--------------------------------------:|-------------------------------------:|-------------------------------------------:|------------------------------------------:|------------------------------------------:|-----------------------------------------:|---------------------:|----------------------:|--------------------:|----------------------------:|-------------------------------:|---------------------------------------:|
|  0 |                                 129320 |                               15.1597 |                                     0 |                                    0 |                                      36684 |                                   9.66154 |                                         0 |                                        0 |                91.68 |                 88.43 |               84.12 |                       97.31 |                           81.2 |                                  97.15 |
