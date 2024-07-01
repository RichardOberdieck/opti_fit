import pandas as pd
from mip import Model, CBC, CONTINUOUS, BINARY, xsum, minimize, GUROBI

from opti_fit.dataset_utils import ALGORITHMS, CUTOFF_THRESHOLDS, OTHER, Algorithm


def solve_relaxed_hit_model_using_mip(
    df: pd.DataFrame, mps_filename: str | None = None, thresholds: dict[Algorithm, float] = CUTOFF_THRESHOLDS
) -> dict[str, float]:
    """This is the simplest model for this problem. It tries to minimize the false positive hits
    while keeping the true positives.

    Args:
        df (pd.DataFrame): Data with the scores etc.
        mps_filename (str | None, optional): Filename for the mps file. Defaults to None.

    Returns:
        dict[str, float]: The optimal cutoffs
    """
    n_names = len(df)
    algorithms = [col for col in df.columns if col not in OTHER]

    model = Model(solver_name=GUROBI)

    # Add the variables
    x = {a: model.add_var(f"x_{a}", var_type=CONTINUOUS, lb=CUTOFF_THRESHOLDS[a], ub=100) for a in algorithms}
    y = {
        (a, n): model.add_var(f"y_{a},{n}", var_type=BINARY)
        for a in algorithms
        for n in range(n_names)
        if df.loc[n, a] >= CUTOFF_THRESHOLDS[a]
    }
    z = {n: model.add_var(f"z_{n}", var_type=BINARY) for n in range(n_names)}

    # Add constraints
    objective = []
    true_positive_constraint = []
    for index, row in df.iterrows():
        model += z[index] <= xsum(y[a, index] for a in algorithms if (a, index) in y)

        if row["is_hit_true_hit"]:
            true_positive_constraint.append(z[index])
        else:
            objective.append(z[index])

        for a in algorithms:
            if (a, index) in y:
                model += (row[a] - 100) * y[a, index] >= x[a] - 100
                model += row[a] - row[a] * y[a, index] <= x[a] - 0.01
                model += y[a, index] <= z[index]

    # Add true positive relaxed constraint
    model += xsum(true_positive_constraint) >= 0.99*len(true_positive_constraint)

    # Add objective
    model.objective = minimize(xsum(objective))
    if mps_filename is not None:
        model.write(mps_filename)
    model.optimize()

    cut_offs = {a: v.x for a, v in x.items()}

    return cut_offs