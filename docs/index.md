# Optimal cutoff selection for string matching algorithms

At [Banking Circle](https://www.bankingcircle.com/), we use a library designed to identify whether a given name is matching, with some variation, a (black)list of names. To achieve this, this library runs several algorithms such as regex matching, computing the fuzzy ratio and more. Most of these algorithms come with the notion of a `score`, and a hit is identified when the `score` is above a user-defined `cutoff`. Since false negatives (it should have been a hit, but is not detected) are unacceptable, the `cutoff`s have been set in such a way that we end up with a high percentage of false positives.

The purpose of this body of work is to investigate how to reduce the false-positive rate without removing true positives. Specifically, we investigate the following "simple" questions:

- What is the optimal cutoff to minimize the amount of false positive *hits*?
- What is the optimal cutoff to minimize the amount of false positive *payments*?

The results can be found in the [Simple Model](simple-model.md) section.

Based on these models, we investigated how much better of a reduction we can achieve by:

- Combining the scores from multiple algorithms together to achieve a better reduction of false positives, see the [Algorithm Combination](algorithm-combination.md) section.
- Allowing for the removal of some true positive hits or payments, see the [Relax True Positive Requirement](relax-the-true-positive-requirement.md) section.

As we were provided a free evaluation license by [Gurobi Optimization](https://gurobi.com) for a portion of this work, we also were interested in the impact of using a commerical versus an open-source solver in terms of runtime, stability and results. This analysis can be found in the [Solver Comparison](solver-comparisons.md) section.

## Getting started

The code uses [hatch](https://hatch.pypa.io/) as a project manager, with the `pyproject.toml` file for configuration. There are four command-line scripts that are defined to run the analysis:

- `hatch run simple`: Solves the simple hit, payment or combined models, see the [Simple Model](simple-model.md) section.
- `hatch run relaxed`: Solves the relaxed hit or payment model, see the [Relax True Positive Requirement](relax-the-true-positive-requirement.md) section.
- `hatch run combination`: Solve the algorithm combination model, see the [Algorithm Combination](algorithm-combination.md) section.
- `hatch run compare`: Compares the different solvers, see the [Solver Comparison](solver-comparisons.md) section.

To get started, install `hatch` and run one of the commands, e.g.:

```
hatch run simple
```

This will execute the script that picks a simple model, a dataset and solves it with the default settings. If you would like to specify the details, you can pass them as arguments, e.g.:

```
hatch run simple --model_name='simple_hit' --full_dataset=False --to_file=True
```

For more information, please check the help:

```
hatch run simple --help
```


## Reproducibility
To run all the analysis as it is reported here, you simply need to execute the `runs.sh` script.

Note that this may be very time consuming and require 32GB or more of RAM, depending on the dataset that is being solved. In addition, as you will see in the [Solver Comparison](solver-comparisons.md) section, running the full dataset without Gurobi is virtually impossible.

All the versions of packages used are pinned to make it easier to reproduce the results. However, this is not the case for [the CBC solver](https://github.com/coin-or/Cbc), which is downloaded by cloning the corresponding Github repository. This is an in-built design choice by the modeling framework `python-mip` that we used. 

Also note that it was necessary to pin a specific commit of `python-mip` since at the time of this writing the latest release (1.15.0) did not support [the HiGHS solver](https://github.com/ERGO-Code/HiGHS), whereas the code was already available on the master branch.

Finally, the data for all runs is stored in json files in the `results` folder of this repository. With it, you can recreate the configuration used for each run, as well as the performance and cutoffs achieved.
