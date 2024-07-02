# Simple model

At its core, the aim is to shave off false positives while keeping the true positives. There are two flavors of this approach:

- Removing false positive *hits*
- Removing false positive *payments*

A payment has one or more hits associated with it, and if at least one hit is a true hit, the payment is considered a true hit.

## Removing false positive hits

To identify the optimal cut-off values for removing false positive hits, we formulate the following mathematical optimization problem:

$$
\begin{array}{llll}
\text{minimize} & \sum_{h \in FP} z_h & & \text{(Minimize false positive hits)} \\
\text{subject to} & \sum_{h \in TP} z_h = 1 & & \text{(Ensure true positive hits)}\\
& z_h \leq \sum_{a} y_{a, h} & \forall h & \text{(If all $y_a=0$, then $z=0$)}\\
& y_{a, h} \leq z_h & \forall h, a & \text{(If any $y_a = 1$, then $z = 1$)} \\
& s_{a, h} - 100y_{a, h} \geq x_a - 100 & \forall h, a & \text{(If $y_a = 1$, then $s_a \geq x_a$)}\\
& s_{a, h} - s_{a, h}y_{a, h} \leq x_a - \epsilon & \forall h, a & \text{(If $y_a = 0$, then $s_a < x_a$)} \\
& x_a \in [0,100] & \forall a & \\
& y_{a,h} \in \{0,1\} & \forall a,h & \\
& z_h \in \{0,1\} & \forall h & \\
\end{array}
$$

where:

- $x_a$ is the optimal cut-off for algorithm $a$
- $y_{a,h}$ indicates whether algorithm $a$ hits on name $h$
- $z_h$ indicates whether name $h$ is a hit or not.
- $FP$ is the set of false positives hits, i.e. names which are not true hits.
- $TP$ is the set of true positives hits.
- $s_{a,h}$ are the scores for algorithm $a$ and name $h$.
- $\epsilon$ is the tolerance to make the "less than" work mathematically.


## Removing false positive payments

To identify the optimal cut-off values for removing false positive payments, we formulate the following mathematical optimization problem:

$$
\begin{array}{llll}
\text{minimize} & \sum_{p \in FP} \alpha_p & & \text{(Minimize false positive payments)} \\
\text{subject to} & \sum_{p \in TP} \alpha_p = 1 & & \text{(Ensure true positive payments)}\\
& \alpha_p \leq \sum_{h \in H(p)} z_{h} & \forall p & \text{(If all $z_h=0$, then $\alpha_p=0$)} \\
& z_{h} \leq \alpha_p & \forall p, h\in H(p) & \text{(If any $z_h=1$, then $\alpha_p=1$)} \\
& z_h \leq \sum_{a} y_{a, h} & \forall h & \text{(If all $y_a=0$, then $z=0$)}\\
& y_{a, h} \leq z_h & \forall h, a & \text{(If any $y_a = 1$, then $z = 1$)} \\
& s_{a, h} - 100y_{a, h} \geq x_a - 100 & \forall h, a & \text{(If $y_a = 1$, then $s_a \geq x_a$)}\\
& s_{a, h} - s_{a, h}y_{a, h} \leq x_a - \epsilon & \forall h, a & \text{(If $y_a = 0$, then $s_a < x_a$)} \\
& x_a \in [0,100] & \forall a & \\
& y_{a,h} \in \{0,1\} & \forall a,h & \\
& z_h \in \{0,1\} & \forall h & \\
& \alpha_p \in \{0,1\} & \forall p & \\
\end{array}
$$

where:

- $x_a$ is the optimal cut-off for algorithm $a$
- $y_{a,h}$ indicates whether algorithm $a$ hits on name $h$
- $z_h$ indicates whether name $h$ is a hit or not.
- $FP$ is the set of false positive payments, i.e. names which are not true hits.
- $TP$ is the set of true positive payments.
- $H(p)$ is the set of all hits that are assigned to payment $p$.
- $s_{a,h}$ are the scores for algorithm $a$ and name $h$.
- $\epsilon$ is the tolerance to make the "less than" work mathematically.

!!! note

    Since we only enforce that we have keep the true positive payments, not the true positive hits, it is possible that solving this model removes true positive hits.

## Implementations

::: opti_fit.simple_model
