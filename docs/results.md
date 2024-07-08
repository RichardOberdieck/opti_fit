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


## Relaxed model

The false positive hit reduction is quite significant, even when only a small slack is introduced:

| Slack        | FP hit reduction [%]  | FP payment reduction [%] |
|-------------:|----------------------:| -------------------------|
|        0.999 |                 15.16 |                     9.66 |
|         0.99 |                 25.56 |                    17.44 |
|         0.98 |                 14.89 |                     9.70 |
|         0.97 |                 14.89 |                     9.70 |
|         0.96 |                 14.89 |                     9.70 |
|         0.95 |                 14.89 |                     9.70 |

Graphically, this looks as follows:

```plotly
{"file_path": "relaxed-hit-model-results.json"}
```

## Algorithm Combination

For the algorithm combination, we tested out 75 different combinations: the 15 different combinations of algorithms with 5 different weights. The 5 most effective were:

| Combination  | FP hit reduction [%]  | FP payment reduction [%] |
|:-------------|----------------------:| -------------------------|
|        0.999 |                 15.16 |                     9.66 |
|         0.99 |                 25.56 |                    17.44 |
|         0.98 |                 14.89 |                     9.70 |
|         0.97 |                 14.89 |                     9.70 |
|         0.96 |                 14.89 |                     9.70 |

The impact of all tested combinations can be seen in the sorted histogram below:

```plotly
{"file_path": "combination-hit-model-full-results.json"}
```

It is also interesting to see how the weight impacts the effectiveness of the added algorithm as a function of the weight:

```plotly
{"file_path": "combination-hit-model-weight-graph-results.json"}
```
