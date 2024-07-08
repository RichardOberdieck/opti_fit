# Simple model

At its core, the aim is to shave off false positives while keeping the true positives. There are two flavors of this approach:

- Removing false positive *hits*
- Removing false positive *payments*

A payment has one or more hits associated with it, and if at least one hit is a true hit, the payment is considered a true hit.

## Removing false positive hits

```
hatch run simple --model_type='hit'
```

To identify the optimal cut-off values for removing false positive hits, we formulate the following mathematical optimization problem:

$$
\begin{array}{llll}
\text{minimize} & \sum_{h \in FP} z_h & & \text{(Minimize false positive hits)} \\
\text{subject to} & z_h = 1 & \forall h \in TP & \text{(Ensure true positive hits)}\\
& z_h \leq \sum_{a} y_{h, a} & \forall h & \text{(If all $y_{h,a}=0$, then $z_h=0$)}\\
& y_{h, a} \leq z_h & \forall h, a & \text{(If any $y_{h,a} = 1$, then $z_h = 1$)} \\
& s_{h, a} - 100y_{h, a} \geq x_a - 100 & \forall h, a & \text{(If $y_{h,a} = 1$, then $s_{h, a} \geq x_a$ for a given hit $h$)}\\
& s_{h, a} - s_{h, a}y_{h, a} \leq x_a - \epsilon & \forall h, a & \text{(If $y_{h,a} = 0$, then $s_{h, a} < x_a$)} \\
& x_a \in [80,100] & \forall a & \\
& y_{h, a} \in \{0,1\} & \forall a,h & \\
& z_h \in \{0,1\} & \forall h & \\
\end{array}
$$

where:

- $x_a$ is the optimal cut-off for algorithm $a$.
- $y_{h,a}$ indicates whether algorithm $a$ hits on name $h$.
- $z_h$ indicates whether name $h$ is a hit or not.
- $FP$ is the set of false positives hits, i.e. names which are not true hits.
- $TP$ is the set of true positives hits.
- $s_{h,a}$ are the scores for algorithm $a$ and name $h$.
- $\epsilon$ is the tolerance to make the "less than" work mathematically.

!!! info
    
    Theoretically, a lower bound of 0 on the $x_a$ variable would be correct, as one cannot by definition exclude those scores below 80. However, this leads to a tremendous increase in the problem size and therefore, we deemed 80 to be a good threshold. As the [Results](results.md) section shows, none of the optimal cutoffs calculated reach the lower bound of 80.


## Removing false positive payments

```
hatch run simple --model_type='payment'
```

To identify the optimal cut-off values for removing false positive payments, we formulate the following mathematical optimization problem:

$$
\begin{array}{llll}
\text{minimize} & \sum_{p \in FP} \alpha_p & & \text{(Minimize false positive payments)} \\
\text{subject to} & \sum_{p \in TP} \alpha_p = 1 & & \text{(Ensure true positive payments)}\\
& \alpha_p \leq \sum_{h \in H(p)} z_{h} & \forall p & \text{(If all $z_h=0$, then $\alpha_p=0$)} \\
& z_{h} \leq \alpha_p & \forall p, h\in H(p) & \text{(If any $z_h=1$, then $\alpha_p=1$)} \\
& z_h \leq \sum_{a} y_{h,a} & \forall h & \text{(If all $y_{h,a}=0$, then $z_h=0$)}\\
& y_{h,a} \leq z_h & \forall h, a & \text{(If any $y_{h,a} = 1$, then $z_h = 1$)} \\
& s_{h,a} - 100y_{h,a} \geq x_a - 100 & \forall h, a & \text{(If $y_{h,a} = 1$, then $s_{h,a} \geq x_a$)}\\
& s_{h,a} - s_{h,a}y_{h,a} \leq x_a - \epsilon & \forall h, a & \text{(If $y_{h,a} = 0$, then $s_{h,a} < x_a$)} \\
& x_a \in [80,100] & \forall a & \\
& y_{h,a} \in \{0,1\} & \forall a,h & \\
& z_h \in \{0,1\} & \forall h & \\
& \alpha_p \in \{0,1\} & \forall p & \\
\end{array}
$$

where:

- $x_a$ is the optimal cut-off for algorithm $a$
- $y_{h,a}$ indicates whether algorithm $a$ hits on name $h$
- $z_h$ indicates whether name $h$ is a hit or not.
- $FP$ is the set of false positive payments, i.e. names which are not true hits.
- $TP$ is the set of true positive payments.
- $H(p)$ is the set of all hits that are assigned to payment $p$.
- $s_{h,a}$ are the scores for algorithm $a$ and name $h$.
- $\epsilon$ is the tolerance to make the "less than" work mathematically.

!!! note

    Since we only enforce that we have keep the true positive payments, not the true positive hits, it is possible that solving this model removes true positive hits.

## Removing false positive payments while respecting true positive hits

```
hatch run simple --model_type='combined'
```

To respecte the true positive nature of the hits, we simply have to add this constraint to the payment model:

$$
z_h = 1 & \forall h \in TP_{hits}
$$

where $TP_{hits}$ is the set of all true positive hits.

## Implementations

::: opti_fit.models.simple_model
