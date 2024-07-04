# Relax the true positive requirement

```
hatch run solve --model='relaxed_true_positive'
```

What is the "cost", mathematically speaking, of enforcing that all true positives should be a hit? And how would that change if we were to relax this constraint?

To analyze this, we only need to take the model from the [Simple Model](simple-model.md) section and replace the true positive constraint:

$$
z_h = 1
$$

with

$$
\sum_{h\in TP} z_h \geq \beta |TP|
$$

where:

- $\beta \in [0,1]$ is the fraction of the true positive hits that should be a hit
- $|\cdot |$ is the cardinality of a set, i.e. $|TP|$ refers to how many true positives there are

!!! note

    It is trivial to extend to the case where payments are considered instead of hits.

## Implementation

::: opti_fit.models.relaxed_model
