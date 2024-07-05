# Results

## Overview

- Just by applying the simple model results in a significant reduction of false positives:

| Model        | FP hit reduction [%]  | FP payment reduction [%] |
| ------------ | --------------------- | -------------------------|
| Hit          |                 15.16 |                     9.66 |
| Payment      |                   TBD |                      TBD |
| Combined     |                 14.89 |                     9.70 |

The corresponding cutoffs are:

|                               |            Hit |       Payment |       Combined |
|:------------------------------|---------------:|--------------:|---------------:|
| regex_match                   |          91.68 |          TBD  |          91.68 |
| jaro_winkler                  |          88.43 |          TBD  |          92.97 |
| fuzz_ratio                    |          84.12 |          TBD  |          82.25 |
| fuzz_token_sort_ratio         |          81.20 |          TBD  |          81.02 |
| fuzz_partial_token_sort_ratio |          97.15 |          TBD  |          97.30 |
| fuzz_partial_ratio            |          97.31 |          TBD  |          97.31 |
