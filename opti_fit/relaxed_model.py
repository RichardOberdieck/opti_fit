import pandas as pd
from mip import Model, xsum, minimize, BINARY

from opti_fit.dataset_utils import ALGORITHMS, CUTOFF_THRESHOLDS
from opti_fit.simple_model import define_cutoff_constraints, define_hit_variables, solve


def solve_relaxed_hit_model(
    df: pd.DataFrame, solver_name: str = "CBC", seed: int = 0, slack: float = 0.99
) -> dict[str, float]:
    """This mdoel allows for a fraction of the true positive hits to be violated.

    Args:
        df (pd.DataFrame): Data with the scores etc.
        solver_name (str): Name of the solver to use
        seed (int): Random seed for the solver
        slack (float): Fraction of true positives to keep

    Returns:
        dict[str, float]: The optimal cutoffs
    """
    model = Model(solver_name=solver_name)

    x, y, z = define_hit_variables(model, df, CUTOFF_THRESHOLDS, ALGORITHMS)

    # Add constraints
    objective = []
    true_positive_constraint = []
    for hit_id, scores in df.iterrows():
        if scores["is_hit_true_hit"]:
            true_positive_constraint.append(z[hit_id])
        else:
            objective.append(z[hit_id])

        model = define_cutoff_constraints(model, scores, x, y, z, ALGORITHMS, hit_id)

    # Add true positive relaxed constraint
    model += xsum(true_positive_constraint) >= slack * len(true_positive_constraint)

    # Add objective
    model.objective = minimize(xsum(objective))
    cutoffs = solve(model, seed, x)

    return cutoffs


def solve_relaxed_payment_model(
    df: pd.DataFrame, solver_name: str = "CBC", seed: int = 0, slack: float = 0.99
) -> dict[str, float]:
    """This mdoel allows for a fraction of the true positive payments to be violated.

    Args:
        df (pd.DataFrame): Data with the scores etc.
        solver_name (str): Name of the solver to use
        seed (int): Random seed for the solver
        slack (float): Fraction of true positives to keep

    Returns:
        dict[str, float]: The optimal cutoffs
    """
    payment_df = df.groupby("payment_case_id", group_keys=True)[["is_payment_true_hit", "is_hit_true_hit"]].apply(
        lambda row: row
    )
    payment_ids = df["payment_case_id"].unique()

    model = Model(solver_name=solver_name)

    # Add the variables
    x, y, z = define_hit_variables(model, df, CUTOFF_THRESHOLDS, ALGORITHMS)
    alpha = {payment_id: model.add_var(f"alpha_{payment_id}", var_type=BINARY) for payment_id in payment_ids}

    # Add constraints
    objective = []
    true_positive_constraint = []
    for payment_id in payment_ids:
        hit_df = payment_df.loc[payment_id]
        if hit_df["is_payment_true_hit"].any():
            true_positive_constraint.append(alpha[payment_id])
        else:
            objective.append(alpha[payment_id])

        model += alpha[payment_id] <= xsum(z[hit_id] for hit_id in hit_df.index)

        for hit_id in hit_df.index:
            model += z[hit_id] <= alpha[payment_id]

            model = define_cutoff_constraints(model, df.loc[hit_id], x, y, z, ALGORITHMS, hit_id)

    model += xsum(true_positive_constraint) >= slack * len(true_positive_constraint)
    model.objective = minimize(xsum(objective))
    cutoffs = solve(model, seed, x)

    return cutoffs
