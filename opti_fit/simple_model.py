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


def solve_simple_payment_model_using_mip(
    df: pd.DataFrame, mps_filename: str | None = None
) -> tuple[dict, dict]:
    payment_df = df.groupby("payment_case_id", group_keys=True)[
        ["is_payment_true_hit", "is_hit_true_hit"]
    ].apply(lambda row: row)
    payment_ids = payment_df.index.get_level_values("payment_case_id").unique()
    hit_ids = payment_df.index.get_level_values("hit_id").unique()

    model = Model(solver_name=CBC)

    # Add the variables
    x = {
        a: model.add_var(f"x_{a}", var_type=CONTINUOUS, lb=CUTOFF_THRESHOLDS[a], ub=100)
        for a in ALGORITHMS
    }
    y = {
        (a, hit_id): model.add_var(f"y_{a},{hit_id}", var_type=BINARY)
        for a in ALGORITHMS
        for hit_id in hit_ids
        if df.loc[hit_id, a] >= CUTOFF_THRESHOLDS[a]
    }
    z = {
        (payment_id, hit_id): model.add_var(f"z_{payment_id},{hit_id}", var_type=BINARY)
        for payment_id, hit_id in payment_df.index
    }
    alpha = {
        payment_id: model.add_var(f"alpha_{payment_id}", var_type=BINARY)
        for payment_id in payment_ids
    }

    # Add constraints
    objective = []
    for payment_id in payment_ids:
        hit_df = payment_df.loc[payment_id]
        if hit_df["is_payment_true_hit"].any():
            model += alpha[payment_id] == 1
        else:
            objective.append(alpha[payment_id])

        model += alpha[payment_id] <= xsum(
            z[payment_id, hit_id] for hit_id in hit_df.index
        )
        for hit_id in hit_df.index:
            model += z[payment_id, hit_id] <= alpha[payment_id]
            model += z[payment_id, hit_id] <= xsum(
                y[a, hit_id] for a in ALGORITHMS if (a, hit_id) in y
            )

            for a in ALGORITHMS:
                if (a, hit_id) in y:
                    score = df.loc[hit_id, a]
                    model += y[a, hit_id] <= z[payment_id, hit_id]
                    model += (score - 100) * y[a, hit_id] >= x[a] - 100
                    model += score - score * y[a, hit_id] <= x[a] - 0.01

    # Add objective
    model.objective = minimize(xsum(objective))
    if mps_filename is not None:
        model.write(mps_filename)
    model.optimize(max_seconds=60)

    cut_offs = {a: v.x for a, v in x.items()}
    expected_hits = {i[1]: v.x > 0.5 for i, v in z.items()}

    return cut_offs, expected_hits
