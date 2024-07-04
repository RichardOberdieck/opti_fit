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

### Reproducibility
This repository is designed to be complete, i.e. all results reported can be reproduced from the data provided. Each model starts with the `hatch` command needed to run the code. Note that this may be very time consuming and require 32GB or more of RAM, depending on the dataset that is being solved.

In addition, all the versions of packages used are pinned to make it easier to reproduce the results. However, this is not the case for [the CBC solver](https://github.com/coin-or/Cbc), which is downloaded by cloning the corresponding Github repository. This is an in-built design choice by the modeling framework `python-mip` that we used. 

Also note that it was necessary to pin a specific commit of `python-mip` since at the time of this writing the latest release (1.15.0) did not support [the HiGHS solver](https://github.com/ERGO-Code/HiGHS), whereas the code was already available on the master branch.
