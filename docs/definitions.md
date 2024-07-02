
# Definitions

In the code and the documentation, several terms are used that may require a deeper explanation:

## Sanctions

A **sanctioned entity** is an entity such as a person, corporation, ship or country which is listed on a **sanctions list**. These lists are issued by goverments (e.g. the American, British or German), state unions (such as the European Union) or even by the United Nations. If an entity is on a list, a bank operating in the jurisdiction of the government to whom the list belong has a legal requirement to ensure that **this entity cannot receive or send any funds**. If a financial institution fails to have adequate controls in place, they can be fined. [In 2023 alone, the U.S. sanctions enforcement issued fines worth $1.5bn](https://www.mofo.com/resources/insights/240304-us-sanctions-enforcement-2023-trends).

For a visual representation, [this map](https://www.sanctionsmap.eu/#/main) shows the sanctions currently in place in the European Union.

!!! note

    For ease of reading, we refer to a single "sanctions list". However, in reality, there are dozens of lists that a bank has to consider. They are, however, merged into a single list whenever possible.

## Payments and hits

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

## Algorithms

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
