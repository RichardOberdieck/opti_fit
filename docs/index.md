# Optimal cutoff selection for string matching algorithms

## Authorship, Contributions and Acknowledgements

This work was carried out by Richard Oberdieck, Ruben Menke and Christian Karsten and the intellectual property of this work rests entirely with our employer, [Banking Circle](https://www.bankingcircle.com/). The work may be reused and reproduced (in fact, we highly encourage it), as stated in the license attached to the Github repository.

If you wish to contribute to this repository (again, highly encouraged), please create a pull request and we will aim to review it as soon as possible.

Finally, we would like to acknowledge the many people who provide the open-source software that makes works such as these possible. We hope to contribute in a small way to that movement by providing access to our research on this topic.

## Overview

At [Banking Circle](https://www.bankingcircle.com/), we use a library designed to identify whether a given name is matching, with some variation, a (black)list of names. To achieve this, this library runs several algorithms such as regex matching, computing the fuzzy ratio and more. Most of these algorithms come with the notion of a `score`, and a hit is identified when the `score` is above a user-defined `cutoff`. Since false negatives (it should have been a hit, but is not detected) are unacceptable, the `cutoff`s have been set in such a way that we end up with a high percentage of false positives.

The purpose of this body of work is to investigate how to reduce the false-positive rate without removing true positives. Specifically, we investigate the following "simple" questions:

- What is the optimal cutoff to minimize the amount of false positive *hits*?
- What is the optimal cutoff to minimize the amount of false positive *payments*?

The results can be found in the [Simple Model](simple_model.md) section.

Based on these models, we investigated how much better of a reduction we can achieve by:

- Combining the scores from multiple algorithms together to achieve a better reduction of false positives, see the [Multiple Cutoff Model](multiple_cutoff_model.md) section.
- Allowing for the removal of some true positive hits or payments, see the [Relax True Positive Requirement](relax-the-true-positive-requirement.md) section.

As we were provided a free evaluation license by [Gurobi Optimization](https://gurobi.com) for a portion of this work, we also were interested in the impact of using a commerical versus an open-source solver in terms of runtime, stability and results. This analysis can be found in the [Solver Comparison](solver-comparisons.md) section.

### Reproducibility
This repository is designed to be complete, i.e. all results reported can be reproduced from the data provided. If there should be any issues, please raise an issue on Github.

## Definitions

In the code and the documentation, several terms are used that may require a deeper explanation:

### Sanctions

A **sanctioned entity** is an entity such as a person, corporation, ship or country which is listed on a **sanctions list**. These lists are issued by goverments (e.g. the American, British or German), state unions (such as the European Union) or even by the United Nations. If an entity is on a list, a bank operating in the jurisdiction of the government to whom the list belong has a legal requirement to ensure that **this entity cannot receive or send any funds**. If a financial institution fails to have adequate controls in place, they can be fined. [In 2023 alone, the U.S. sanctions enforcement issued fines worth $1.5bn](https://www.mofo.com/resources/insights/240304-us-sanctions-enforcement-2023-trends).

For a visual representation, [this map](https://www.sanctionsmap.eu/#/main) shows the sanctions currently in place in the European Union.

!!! note

    For ease of reading, we refer to a single "sanctions list". However, in reality, there are dozens of lists that a bank has to consider. They are, however, merged into a single list whenever possible.

### Payments and hits

A **payment** is a transaction where money is sent from a sender to a receiver. Legally, every payment needs to be screened for sanction violations. Each payment has a sender, a receiver, and maybe other components such as remitter information and addresses. Each of these components is **screened** against the sanctions list. This can result in one or more **hits** against names on the sanctions list. Therefore, in the context of sanction screening, we have the following structure:

- Payment 1
    - Hit 1
    - Hit 2
    - Hit 3
- Payment 2
    - Hit 4
- Payment 3
    - Hit 5
    - Hit 6

Each of the hits is **assessed by an analyst** whether they are **true/false positives**. If a payment has at least one true positive, it is **escalated** and sent to the **Financial Intelligence Unit (FIU)** of the respective jurisdiction. If all hits in a payment are deemed false positives, the payment is **released**.

Therefore, considering the example from above, we may have the following situation:

- Payment 1 - True positive
    - Hit 1 - True positive
    - Hit 2 - False positive
    - Hit 3 - True positive
- Payment 2 - True positive
    - Hit 4 - True positive
- Payment 3 - False positive
    - Hit 5 - False positive
    - Hit 6 - False positive

"Pythonically", we can write that a payment `p` is a hit if:

```
any(h.is_hit_true_hit for h in H(p))
```

where `H(p)` is the set of all hits that are assigned to payment `p`.

### Algorithms

Since it is impossible to manually review millions of payments a day, algorithms are used to perform the initial screening of the payments. Since the task at hand is essentially string matching, we chose to use the following algorithms:

- **Regex match**: Checks whether the name matches a regular expression variation of the blacklist.
- **Jaro Winkler**: Computes the [Jaro Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) distance between the name and corresponding blacklist name.
- **Fuzz (Partial/Token Sort/Partial Token Sort) Ratio**: [This Stack Overflow post](https://stackoverflow.com/questions/31806695/when-to-use-which-fuzz-function-to-compare-2-strings) describes the algorithm in sufficient detail, so please refer there and the referenced links.

These algorithms all work similarly in that they calculate a **score**. Based on experimentation, we have set a (conservative) **cutoff** (or **threshold**) for each of these algorithms. If the score exceeds the threshold, it is deemed a hit. "Pythonically" again, this means that a screening `h` is a considered a hit if:

```
any(h.score[a] >= cutoff[a] for a in algorithms)
```

where `algorithms` is the set of all algorithms applied.

!!! note

    There are also a couple of other algorithms, but they are not relevant for the analysis performed in this body of work. Also, note that there are a lot more compoenents that create a sanction screening tool than the string matching, although the string matching is a core component.

## The dataset

The dataset in this repository contains the real algorithms scores from our production environment in the bank. The dataset in numbers:

- 853049 total hits, of which 4023 are true positive hits (0.47%)
- 379691 total payments, of which 2572 are true positives (0.68%)

The set is a compressed csv file, where each row represents one hit. The dataset has the following columns:

- **payment_case_id**: A unique identifier for each payment
- **is_payment_true_hit**: Whether the payment is a true hit or not
- **is_hit_true_hit**: Whether the hit is a true hit or not
- **regex_match**: Score of this hit for the algorithm REGEX_MATCH
- **jaro_winkler**: Score of this hit for the algorithm JARO_WINKLER
- **fuzz_ratio**: Score of this hit for the algorithm FUZZ_RATIO
- **fuzz_partial_ratio**: Score of this hit for the algorithm FUZZ_PARTIAL_RATIO
- **fuzz_token_sort_ratio**: Score of this hit for the algorithm FUZZ_TOKEN_SORT_RATIO
- **fuzz_partial_token_sort_ratio**: Score of this hit for the algorithm FUZZ_PARTIAL_TOKEN_SORT_RATIO
