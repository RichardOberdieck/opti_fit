# Optimal cutoff selection for string matching algorithms

## Background
At [Banking Circle](https://www.bankingcircle.com/), we use a library designed to identify whether a given name is matching, with some variation, a (black)list of names. To achieve this, this library runs several algorithms such as regex matching, computing the fuzzy ratio and more. Most of these algorithms come with the notion of a `score`, and a hit is identified when the `score` is above a user-defined `cut-off`. Since false negatives (it should have been a hit, but is not detected) are unacceptable, the `cut-off`s have been set in such a way that we end up with a high percentage of false positives.

The purpose of this body of work is to investigate how to reduce the false-positive rate without introducing false-negatives.

### Reproducibility
This repository is designed to be complete, i.e. all results reported can be reproduced from the data provided.

## The algorithms

- **Regex match**: Checks whether the name matches a regular expression variation of the blacklist.
- **Jaro Winkler**: Computes the [Jaro Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) distance between the name and corresponding blacklist name.
- **Fuzz (Partial/Token Sort/Partial Token Sort) Ratio**: [This Stack Overflow post](https://stackoverflow.com/questions/31806695/when-to-use-which-fuzz-function-to-compare-2-strings) describes the algorithm in sufficient detail, so please refer there and the referenced links.

## The dataset

The vast majority of payments do not have any connections to sanctioned entities. This means that using the regular payment flow for a detailed analysis will heavily skew the distribution and make any form of statstical analysis meaningless. Therefore, we decided to use all payments that have been flagged by the algorithms since late 2023 as the baseline set. Each of these hits has been manually checked by a human, identifying it as a true hit or not.

There are two datasets:
- The [small dataset](../data/small_dataset.csv.gz) is used for testing the algorithm
- The [full dataset](../data/full_dataset.csv.gz) contains all the data

Note that due to size restrictions of Github the files have been compressed.