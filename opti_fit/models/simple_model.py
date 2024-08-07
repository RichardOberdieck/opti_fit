import pandas as pd
from mip import Model, CONTINUOUS, BINARY, xsum, minimize, Var

from opti_fit.utils.dataset_utils import ALGORITHMS, OVERVIEW_COLUMNS
from opti_fit.utils.model_utils import TIMELIMIT


def solve_simple_hit_model(df: pd.DataFrame, solver_name: str = "CBC", seed: int = 0) -> dict[str, float]:
    """This is the simplest model for this problem. It tries to minimize the false positive hits
    while keeping the true positives.

    Args:
        df (pd.DataFrame): Data with the scores etc.
        solver_name (str): Name of the solver to use
        seed (int): Random seed for the solver

    Returns:
        The optimal cutoffs
    """
    algorithms = [col for col in df.columns if col not in OVERVIEW_COLUMNS]

    model = Model(solver_name=solver_name)

    # Add the variables
    x, y, z = define_hit_variables(model, df, algorithms)

    # Add constraints
    objective = []
    for hit_id, scores in df.iterrows():
        if scores["is_hit_true_hit"]:
            model += z[hit_id] == 1
        else:
            objective.append(z[hit_id])

        model = define_cutoff_constraints(model, scores, x, y, z, algorithms, hit_id)

    model.objective = minimize(xsum(objective))
    cutoffs = solve(model, seed, x)

    return cutoffs


def solve_simple_payment_model(df: pd.DataFrame, solver_name: str = "CBC", seed: int = 0) -> dict[str, float]:
    """This model goes one level up from the simple hit model, as it considers
    that payments should be true positives, rather than hits.

    Args:
        df (pd.DataFrame): Data with the scores etc.
        solver_name (str): Name of the solver to use
        seed (int): Random seed for the solver

    Returns:
        The optimal cutoffs
    """
    payment_df = df.groupby("payment_case_id", group_keys=True)[["is_payment_true_hit", "is_hit_true_hit"]].apply(
        lambda row: row
    )
    payment_ids = df["payment_case_id"].unique()

    model = Model(solver_name=solver_name)

    # Add the variables
    x, y, z = define_hit_variables(model, df, ALGORITHMS)
    alpha = {payment_id: model.add_var(f"alpha_{payment_id}", var_type=BINARY) for payment_id in payment_ids}

    # Add constraints
    objective = []
    for payment_id in payment_ids:
        hit_df = payment_df.loc[payment_id]
        if hit_df["is_payment_true_hit"].any():
            model += alpha[payment_id] == 1
        else:
            objective.append(alpha[payment_id])

        model += alpha[payment_id] <= xsum(z[hit_id] for hit_id in hit_df.index)

        for hit_id in hit_df.index:
            model += z[hit_id] <= alpha[payment_id]

            model = define_cutoff_constraints(model, df.loc[hit_id], x, y, z, ALGORITHMS, hit_id)

    model.objective = minimize(xsum(objective))
    cutoffs = solve(model, seed, x)

    return cutoffs


def solve_simple_combined_model(df: pd.DataFrame, solver_name: str = "CBC", seed: int = 0) -> dict[str, float]:
    """This model combines the hit and payment models such that we should not have any true positive
    violations while minimizing the true positive payments.

    Args:
        df (pd.DataFrame): Data with the scores etc.
        solver_name (str): Name of the solver to use
        seed (int): Random seed for the solver

    Returns:
        The optimal cutoffs
    """
    payment_df = df.groupby("payment_case_id", group_keys=True)[["is_payment_true_hit", "is_hit_true_hit"]].apply(
        lambda row: row
    )
    payment_ids = df["payment_case_id"].unique()

    model = Model(solver_name=solver_name)

    # Add the variables
    x, y, z = define_hit_variables(model, df, ALGORITHMS)
    alpha = {payment_id: model.add_var(f"alpha_{payment_id}", var_type=BINARY) for payment_id in payment_ids}

    # Add constraints
    objective = []
    for payment_id in payment_ids:
        hit_df = payment_df.loc[payment_id]
        if hit_df["is_payment_true_hit"].any():
            model += alpha[payment_id] == 1
        else:
            objective.append(alpha[payment_id])

        model += alpha[payment_id] <= xsum(z[hit_id] for hit_id in hit_df.index)

        for hit_id, scores in hit_df.iterrows():
            model += z[hit_id] <= alpha[payment_id]
            if scores["is_hit_true_hit"]:
                model += z[hit_id] == 1

            model = define_cutoff_constraints(model, df.loc[hit_id], x, y, z, ALGORITHMS, hit_id)

    model.objective = minimize(xsum(objective))
    cutoffs = solve(model, seed, x)

    return cutoffs


def define_hit_variables(model: Model, df: pd.DataFrame, algorithms: list[str]) -> tuple[dict, dict, dict]:
    x = {a: model.add_var(f"x_{a}", var_type=CONTINUOUS, lb=80, ub=100) for a in algorithms}
    y = {
        (hit_id, a): model.add_var(f"y_{a},{hit_id}", var_type=BINARY)
        for a in algorithms
        for hit_id in df.index
        if df.loc[hit_id, a] >= 80
    }
    z = {hit_id: model.add_var(f"z_{hit_id}", var_type=BINARY) for hit_id in df.index}
    return x, y, z


def define_cutoff_constraints(
    model: Model, scores: dict, x: dict, y: dict, z: dict, algorithms: list[str], hit_id: int
) -> Model:
    model += z[hit_id] <= xsum(y[hit_id, a] for a in algorithms if (hit_id, a) in y)
    for a in algorithms:
        if (hit_id, a) not in y:
            continue

        model += y[hit_id, a] <= z[hit_id]
        model += (scores[a] - 100) * y[hit_id, a] >= x[a] - 100
        model += scores[a] - scores[a] * y[hit_id, a] <= x[a] - 0.01

    return model


def solve(model: Model, seed: int, x: dict[str, Var]) -> dict[str, float]:
    model.seed = seed
    with open("data/hit_start.mst", "r") as file:
        start_data = file.readlines()
    # Ignore first line as it is a comment
    mip_start = []
    for line in start_data[1:]:
        entries = line.split(" ")
        if len(entries) != 2:
            raise ValueError()
        var = model.var_by_name(entries[0])
        if var is not None:
            mip_start.append((var, float(entries[1][:-1])))  # Need to get rid of \n

    model.start = mip_start
    model.optimize(max_seconds=TIMELIMIT)
    return {a: v.x for a, v in x.items()}
