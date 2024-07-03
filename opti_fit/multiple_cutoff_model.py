import numpy as np
import pandas as pd
from itertools import combinations
from tqdm import tqdm

from opti_fit.dataset_utils import ALGORITHMS, CUTOFF_THRESHOLDS
from opti_fit.simple_model import solve_simple_hit_model
from opti_fit.model_utils import analyze_performance


def solve_hit_model_with_multiple_cutoffs(df: pd.DataFrame, solver_name: str = "CBC") -> tuple[dict, dict]:
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
    cutoff_results = {}
    performance = {}
    best_performance = 0
    best_cutoff = {}
    xlsx_filename = f"multiple_cutoffs_full_results_{len(df)}.xlsx"
    counter = 1

    for algorithms in tqdm(algorithm_combinations):
        string_rep = algorithms[0].value + "," + algorithms[1].value
        new_df = df.copy(deep=True)
        for weight in weighting:
            str_instance = f"{string_rep} - {weight}"
            print(f"Solving {str_instance}")
            new_df[string_rep] = new_df.apply(
                lambda row: weight * row[algorithms[0]] + (1 - weight) * row[algorithms[1]], axis=1
            )
            thresholds = CUTOFF_THRESHOLDS
            thresholds[string_rep] = (
                weight * CUTOFF_THRESHOLDS[algorithms[0]] + (1 - weight) * CUTOFF_THRESHOLDS[algorithms[1]]
            )
            cutoffs = solve_simple_hit_model(new_df, solver_name, thresholds)
            cutoff_results[(string_rep, weight)] = cutoffs
            performance[(string_rep, weight)] = analyze_performance(new_df, cutoffs)
            cutoffs_df = pd.DataFrame.from_dict(cutoffs, orient="index", columns=["Cutoff value"])
            config_df = pd.DataFrame.from_dict(
                {"Algorithm A": algorithms[0].value, "Algorithm B:": algorithms[1].value, "Weight": weight},
                orient="index",
                columns=["Value"],
            )

            with pd.ExcelWriter(xlsx_filename, engine="xlsxwriter") as writer:
                config_df.to_excel(writer, sheet_name=str(counter), startrow=0, startcol=0)
                cutoffs_df.to_excel(writer, sheet_name=str(counter), startrow=5, startcol=0)
                performance[(string_rep, weight)].to_excel(writer, sheet_name=str(counter), startrow=15, startcol=0)

            if performance[(string_rep, weight)].loc["Hits", "Removed False Positive [absolute]"] > best_performance:
                best_performance = performance[(string_rep, weight)].loc["Hits", "Removed False Positive [absolute]"]
                best_cutoff = cutoffs
            counter += 1

    return best_cutoff
