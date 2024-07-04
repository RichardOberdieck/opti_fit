import json
import os
import pandas as pd
from opti_fit.models.models import get_model
from opti_fit.utils.dataset_utils import read_dataset


def parse_and_validate_runner_input(
    model_name: str = "simple_hit", solver_name: str = "CBC", full_dataset: bool = True
):
    model = get_model(model_name)
    if solver_name not in ["GUROBI", "GRB", "CBC", "HIGHS"]:
        raise ValueError(f"Invalid solver name, got {solver_name}")

    filename = "full_dataset.csv.gz" if full_dataset else "small_dataset.csv.gz"
    df = read_dataset(os.path.join("data", filename))

    return model, df


PERFORMANCE_CUTOFF_COLUMNS = [
    "removed_false_positive_hits",
    "removed_true_positive_hits",
    "removed_false_positive_payments",
    "removed_true_positive_payments",
    "cutoff_regex_match",
    "cutoff_jaro_winkler",
    "cutoff_fuzz_ratio",
    "cutoff_fuzz_partial_ratio",
    "cutoff_fuzz_token_sort_ratio",
    "cutoff_fuzz_partial_token_sort_ratio",
]


def merge_performance_and_cutoff_output(performance_df: pd.DataFrame, cutoffs: dict[str, float]) -> tuple:
    return (
        performance_df.loc["Hits", "Removed False Positive [absolute]"],
        performance_df.loc["Hits", "Removed True Positive [absolute]"],
        performance_df.loc["Payment", "Removed False Positive [absolute]"],
        performance_df.loc["Payment", "Removed True Positive [absolute]"],
        cutoffs["regex_match"],
        cutoffs["jaro_winkler"],
        cutoffs["fuzz_ratio"],
        cutoffs["fuzz_partial_ratio"],
        cutoffs["fuzz_token_sort_ratio"],
        cutoffs["fuzz_partial_token_sort_ratio"],
    )


def print_and_write_results(config_df: pd.DataFrame, result_df: pd.DataFrame, to_file: bool, filename: str):
    print("Configuration:")
    print(config_df.to_markdown())
    print("Results:")
    print(result_df.to_markdown())

    if to_file:
        with open(filename, "w") as file:
            json.dump([config_df.to_dict(orient="index"), result_df.to_dict(orient="index")], file)
        print(f"Written to {filename}")
