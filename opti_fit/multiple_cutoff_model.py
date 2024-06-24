import numpy as np
import pandas as pd
from itertools import combinations

from opti_fit.dataset_utils import ALGORITHMS, CUTOFF_THRESHOLDS
from opti_fit.simple_model import solve_simple_model_using_mip


def solve_hit_model_with_multiple_cutoffs_using_mip(
    df: pd.DataFrame, mps_filename: str | None = None
) -> tuple[dict, dict]:
    """This model tests the assumption that it is possible to use the information from multiple
    algorithms to remove even more false positives. We essentially combine the weighted scores from 2 algorithms
    and run the simple hit model with this additional "algorithm score".

    Args:
        df (pd.DataFrame): Data with the scores etc.
        mps_filename (str | None, optional): Filenames to be saved. Defaults to None.

    Returns:
        tuple[dict, dict]: Returns all the cutoff results and the number of hits expected from each combination.
    """

    algorithm_combinations = combinations(ALGORITHMS, 2)
    weighting = np.linspace(0, 1, 5)
    cutoff_results = {}
    hit_count = {}
    filename = None

    for algorithms in algorithm_combinations:
        string_rep = str(algorithms[0]) + "," + str(algorithms[1])
        new_df = df.copy(deep=True)
        for weight in weighting:
            new_df[string_rep] = new_df.apply(
                lambda row: weight * row[algorithms[0]] + (1 - weight) * row[algorithms[1]], axis=1
            )
            if mps_filename:
                filename = mps_filename + "_" + string_rep + "_" + weight
            thresholds = CUTOFF_THRESHOLDS
            thresholds[string_rep] = (
                weight * CUTOFF_THRESHOLDS[algorithms[0]] + (1 - weight) * CUTOFF_THRESHOLDS[algorithms[1]]
            )
            cutoffs, expected_hits = solve_simple_model_using_mip(df, filename, thresholds)
            cutoff_results[(string_rep, weight)] = cutoffs
            hit_count[(string_rep, weight)] = sum(expected_hits.values())

    return cutoff_results, hit_count
