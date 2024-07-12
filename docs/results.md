# Results

## Simple model

The solution of the simple models already results in a significant reduction of false positives:

{{ read_json('simple_model_results.json') }}

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

From this, we can also construct a Pareto curve:

```plotly
{"file_path": "relaxed-hit-model-pareto.json"}
```

## Algorithm Combination

For the algorithm combination, we tested out 75 different combinations: the 15 different combinations of algorithms with 5 different weights. The 5 most effective were:

| Combination  | FP hit reduction [%]  | FP payment reduction [%] |
|:-------------|----------------------:| -------------------------|
|        0.999 |                 19.23 |                    13.26 |
|         0.99 |                 23.76 |                    16.73 |
|         0.98 |                 31.29 |                    24.87 |
|         0.97 |                 35.81 |                    27.33 |
|         0.96 |                 38.18 |                    29.69 |
|         0.95 |                 40.68 |                    32.15 |

The impact of all tested combinations can be seen in the sorted histogram below:

```plotly
{"file_path": "combination-hit-model-full-results.json"}
```

It is also interesting to see how the weight impacts the effectiveness of the added algorithm as a function of the weight:

```plotly
{"file_path": "combination-hit-model-weight-graph-results.json"}
```

## Some comments

- The results were achieved by running the `runs.sh` script in this repository. The graphs were created with the `generate_images.py` file.
- As we needed to run a lot of experiments, we looked into improving the Gurobi runime. We found that providing a MIP start helped, and so we provided the solution of the simple hit model to all runs as a start solution. We also used the following parameters for our runs:
    - [Presolve](https://www.gurobi.com/documentation/current/refman/presolve.html) = 1: This reduces the default amount of presolve to an extent, as we noticed that it would stall after a certain period. However, presolve is necessary as removig it completely resulted in significantly worse runtimes.
    - [Method](https://www.gurobi.com/documentation/current/refman/method.html) = 2: We found that the barrier method plus crossover was the most effective method and hence we used it rather than the default concurrent solver.
    - [Threads](https://www.gurobi.com/documentation/current/refman/threads.html) = 8: We had a machine with 16 threads (8 physical cores) and 32GB of RAM available for our experiments. Unfortunately, we did run out of memory on several occasions and so we found it to be more stable if we limited the number of threads to 8, rather than the default 16.

    
