import json
import os
import pandas as pd
from opti_fit.models.models import get_model
from opti_fit.utils.dataset_utils import read_dataset
from opti_fit.utils.model_utils import PERFORMANCE_COLUMNS


def parse_and_validate_runner_input(
    model_name: str = "simple_hit", solver_name: str = "CBC", dataset: str = "full_dataset.csv.gz"
):
    model = get_model(model_name)
    if solver_name not in ["GUROBI", "GRB", "CBC", "HIGHS"]:
        raise ValueError(f"Invalid solver name, got {solver_name}")

    df = read_dataset(os.path.join("data", dataset))

    return model, df


def merge_performance_and_cutoff_output(performance_df: pd.DataFrame, cutoffs: dict[str, float]) -> tuple[tuple, list]:
    result = ()
    column_names = []
    for element in ["hits", "payments"]:
        for column in PERFORMANCE_COLUMNS:
            if column.startswith("removed_"):
                result += (float(performance_df.loc[element, column]),)
                column_names.append(column + "_" + element)

    for algorithm, cutoff in cutoffs.items():
        result += (cutoff,)
        column_names.append(f"cutoff_{algorithm}")

    return result, column_names


def print_and_write_results(config_df: pd.DataFrame, result_df: pd.DataFrame, to_file: bool, filename: str):
    print("Configuration:")
    print(config_df.to_markdown())
    print("Results:")
    print(result_df.to_markdown())

    if to_file:
        with open(filename, "w") as file:
            json.dump([config_df.to_dict(orient="index"), result_df.to_dict(orient="index")], file)
        print(f"Written to {filename}")


def read_result(filepath: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    with open(filepath) as file:
        data = json.load(file)

    config_df = pd.DataFrame.from_dict(data[0], orient="index")  # The first entry is the configuration
    result_df = pd.DataFrame.from_dict(data[1], orient="index")  # The second entry is the result

    return config_df, result_df
