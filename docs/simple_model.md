# Simple model

To identify the optimal cut-off values, we formulate the following mathematical optimization problem:
$$
\begin{array}{llll}
\text{minimize} & \sum_{h \in FP} z_h & & \text{(Minimize false positives)}\\
\text{subject to} & \sum_{h \in TP} z_h = 1 & & \text{(Ensure true positives)}\\
& z_h \leq \sum_{a} y_{a, h} & \forall h & \text{(If all $y_a=0$, then $z=0$)}\\
& s_{a, h} - 100y_{a, h} \geq x_a - 100 & \forall h, a & \text{(If $y_a = 1$, then $s_a \geq x_a$)}\\
& s_{a, h} - s_{a, h}y_{a, h} \leq x_a - 0.01 & \forall h, a & \text{(If $y_a = 0$, then $s_a < x_a$)} \\
& y_{a, h} \leq z_h & \forall h, a & \text{(If any $y_a = 1$, then $z = 1$)} \\
& x_a \in [0,100] & \forall a \\
& y_{a,h} \in \{0,1\} & \forall a,h \\
& z_h \in \{0,1\} & \forall h
\end{array}
$$

where:
- $x_a$ is the optimal cut-off for algorithm $a$
- $y_{a,h}$ indicates whether algorithm $a$ hits on name $h$
- $z_h$ indicates whether name $h$ is a hit or not.
- $FP$ is the set of false positives, i.e. names which are not true hits.
- $TP$ is the set of true positives
- $s_{a,h}$ are the scores for algorithm $a$ and name $h$.

::: opti_fit.simple_model