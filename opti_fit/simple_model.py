import pandas as pd
from mip import Model, CBC, CONTINUOUS, BINARY, xsum, minimize

from opti_fit.dataset_utils import ALGORITHMS


def solve_simple_model_using_mip(df: pd.DataFrame):
    # Extract data - may be moved out if too elaborate
    lb_for_cutoff = df[ALGORITHMS].min(axis=0)
    n_names = len(df)
    
    
    model = Model(solver_name=CBC)

    # Add the variables
    x = {a: model.add_var(f"x_{a}", var_type=CONTINUOUS, lb=lb_for_cutoff[a], ub=100) for a in ALGORITHMS}
    y = {(a, n): model.add_var(f"y_{a},{n}", var_type=BINARY) for a in ALGORITHMS for n in range(n_names)}
    z = {n: model.add_var(f"z_{n}", var_type=BINARY) for n in range(n_names)}

    # Add constraints
    objective = 0
    for h, row in df.iterrows():
        model += z[h] <= xsum(y[a, h] for a in ALGORITHMS if (a, h) in y)

        if row[' is_hit_true_hit']:
            model += z[h] == 1
        else:
            objective.append(z[h])

        for a in ALGORITHMS:
            if (a, h) in y:
                model += (row[a] - 100) * y[a, h] >= x[a] - 100
                model += row[a] - row[a] * y[a, h] <= x[a] - 0.01
                model += y[a, h] <= z[h]

    # Add objective
    model.objective = minimize(xsum(objective))
    model.write("model.mps")
    model.optimize(max_seconds=600)

    cut_offs = {a: v.x for a, v in x.items()}
    expected_hits = {name: v.x > 0.5 for name, v in z.items()}

    return cut_offs, expected_hits