# Solver Comparisons

```
hatch run compare
```

We made the choice to use the [python-mip](https://github.com/coin-or/python-mip) library as the modeling framework for this project, as its API is straightforward and it has been around for a few years. This library supports [Gurobi](https://gurobi.com/), [CBC](https://github.com/coin-or/Cbc) and [HiGHS](https://highs.dev/) as solvers, and so we naturally were curious how these solvers would compare their behaviour.

We would like to express our gratitude to the CBC and HiGHS teams for providing an open-source solver. We also would like to thank Gurobi Optimization for providing an evaluation license in order to run these experiments.

!!! note

    We needed to use a specific commit, rather than a released version, for the `python-mip` package, as the HiGHS integration was not released yet when we performed these experiments. Also, `python-mip` does not allow the specification of the CBC version, which makes this comparison less reproducible.

## Methodology

In order to make the results as robust as possible, we considered the following:

- Use a single simple model
- Use 5 different random seeds

!!! note

    We did set some Gurobi parameters (see [Results](results.md) section), however they only had a modest impact on the overall runtime. Nonetheless, we removed those parameters for this comparison in order to be as fair as possible.

## Results

Gurobi is order of magnitudes more performant and efficient than HiGHS and CBC. 
