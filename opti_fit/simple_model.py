import pandas as pd
from mip import Model, CBC, CONTINUOUS, BINARY, xsum, minimize

from opti_fit.dataset_utils import ALGORITHMS, CUTOFF_THRESHOLDS


def solve_simple_model_using_mip(
    df: pd.DataFrame, mps_filename: str | None = None
) -> tuple[dict, dict]:
    n_names = len(df)

    model = Model(solver_name=CBC)

    # Add the variables
    x = {
        a: model.add_var(f"x_{a}", var_type=CONTINUOUS, lb=CUTOFF_THRESHOLDS[a], ub=100)
        for a in ALGORITHMS
    }
    y = {
        (a, n): model.add_var(f"y_{a},{n}", var_type=BINARY)
        for a in ALGORITHMS
        for n in range(n_names)
        if df.loc[n, a] >= CUTOFF_THRESHOLDS[a]
    }
    z = {n: model.add_var(f"z_{n}", var_type=BINARY) for n in range(n_names)}

    # Add constraints
    objective = []
    for index, row in df.iterrows():
        model += z[index] <= xsum(y[a, index] for a in ALGORITHMS if (a, index) in y)

        if row["is_hit_true_hit"]:
            model += z[index] == 1
        else:
            objective.append(z[index])

        for a in ALGORITHMS:
            if (a, index) in y:
                model += (row[a] - 100) * y[a, index] >= x[a] - 100
                model += row[a] - row[a] * y[a, index] <= x[a] - 0.01
                model += y[a, index] <= z[index]

    # Add objective
    model.objective = minimize(xsum(objective))
    if mps_filename is not None:
        model.write(mps_filename)
    model.optimize(max_seconds=60)

    cut_offs = {a: v.x for a, v in x.items()}
    expected_hits = {i: v.x > 0.5 for i, v in z.items()}

    return cut_offs, expected_hits
