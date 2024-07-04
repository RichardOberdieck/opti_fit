# Simple model

At its core, the aim is to shave off false positives while keeping the true positives. There are two flavors of this approach:

- Removing false positive *hits*
- Removing false positive *payments*

A payment has one or more hits associated with it, and if at least one hit is a true hit, the payment is considered a true hit.

## Removing false positive hits

```
hatch run solve --model='simple_hit_mip'
```

To identify the optimal cut-off values for removing false positive hits, we formulate the following mathematical optimization problem:

$$
\begin{array}{llll}
\text{minimize} & \sum_{h \in FP} z_h & & \text{(Minimize false positive hits)} \\
\text{subject to} & \sum_{h \in TP} z_h = 1 & & \text{(Ensure true positive hits)}\\
& z_h \leq \sum_{a} y_{h, a} & \forall h & \text{(If all $y_{h,a}=0$, then $z_h=0$)}\\
& y_{h, a} \leq z_h & \forall h, a & \text{(If any $y_{h,a} = 1$, then $z_h = 1$)} \\
& s_{h, a} - 100y_{h, a} \geq x_a - 100 & \forall h, a & \text{(If $y_{h,a} = 1$, then $s_{h, a} \geq x_a$ for a given hit $h$)}\\
& s_{h, a} - s_{h, a}y_{h, a} \leq x_a - \epsilon & \forall h, a & \text{(If $y_{h,a} = 0$, then $s_{h, a} < x_a$)} \\
& x_a \in [0,100] & \forall a & \\
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


## Removing false positive payments

```
hatch run solve --model='simple_payment_mip'
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
& x_a \in [0,100] & \forall a & \\
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

## Implementations

::: opti_fit.models.simple_model
