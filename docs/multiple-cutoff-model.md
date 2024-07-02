# Multiple cutoff model

Having investigated the results from running the [simple models](simple-model.md), we were curious whether it would be beneficial to combine the scores of two algorithms together in order to gain an additional degree of freedom that can be used to remove false positives. We chose the following approach:

- Iterate over all possible combinations (15 in total) of algorithm pairs `(A,B)`
- Choose 3 different weights `w` (0.1, 0.25, 0.4) to combine the score algorithm `A` with the score of algorithm `B`:

$$
s_{(A,B)} = wA + (1-w)B
$$

- For each combination `(A,B,w)`, calculate the resulting scores, add them to the dataset and run the simple model (either hit or payment). This results in a false positive removal percentage.
- Return the best percentage, and write the results from all runs (3*15=45 in total) to an Excel file.

## Why only 2 algorithms?

We could have analyzed what would happen if we combined 3 or even more algorithms, but then it becomes much harder to explain to a regulator who audits the sanction screening program. We still may do this analysis in the future, but it was not the focus of the first approach.

## Implementation

::: opti_fit.multiple_cutoff_model

## Results

TBD
