import json
from typing import Callable
import numpy as np
import pandas as pd
from itertools import combinations
from tqdm import tqdm

from opti_fit.utils.dataset_utils import ALGORITHMS, OVERVIEW_COLUMNS, Algorithm, get_hash
from opti_fit.models.simple_model import solve_simple_hit_model
from opti_fit.utils.model_utils import PERFORMANCE_COLUMNS, analyze_performance


def solve_model_with_multiple_cutoffs(
    df: pd.DataFrame, solver_name: str = "CBC", base_model: Callable = solve_simple_hit_model
) -> dict[str, float]:
    """This model tests the assumption that it is possible to use the information from multiple
    algorithms to remove even more false positives. We essentially combine the weighted scores from 2 algorithms
    and run the simple hit model with this additional "algorithm score".

    Args:
        df (pd.DataFrame): Data with the scores etc.
        solver_name (str): Name of the solver to use

    Returns:
        tuple[dict, dict]: Returns all the cutoff results and the number of hits expected from each combination.
    """

    algorithm_combinations = combinations(ALGORITHMS, 2)
    weighting = np.linspace(0.1, 0.4, 3)
    cutoff_dict = {}
    performance_dict = {}
    result = []
    filename = f"results/multiple_cutoffs_{solver_name}_{base_model.__name__}_{get_hash(df)}.json"

    for algorithms in tqdm(algorithm_combinations):
        string_rep = get_string_representation(algorithms)

        for weight in weighting:
            instance = (string_rep, weight)
            print(f"Solving {str(instance)}")
            df = update_df(df, algorithms, weight)

            cutoffs = base_model(df, solver_name)

            cutoff_dict[instance] = cutoffs
            performance = analyze_performance(df, cutoffs)
            performance_dict[instance] = performance.to_dict()
            result.append(instance + performance.to_records())

    result_df = pd.DataFrame.from_records(
        result, columns=["Algorithm A", "Algorithm B", "weight"] + PERFORMANCE_COLUMNS
    )
    result_df.sort_values(by="Removed False Positive [%]", axis=1, inplace=True)

    with open(filename, "w") as file:
        json.dump([result_df.to_dict(), cutoff_dict, performance_dict], file)

    return result_df


def get_string_representation(algorithms: list[Algorithm]) -> str:
    return algorithms[0].value + "," + algorithms[1].value


def update_df(df: pd.DataFrame, algorithms: list[Algorithm], weight: float) -> pd.DataFrame:
    df.drop(columns=[c for c in df.columns if c not in OVERVIEW_COLUMNS + ALGORITHMS], inplace=True)  # Clean-up first
    string_rep = get_string_representation(algorithms)
    df[string_rep] = df.apply(lambda row: weight * row[algorithms[0]] + (1 - weight) * row[algorithms[1]], axis=1)
    return df
