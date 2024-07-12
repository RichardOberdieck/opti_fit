from typing import Callable
import pandas as pd
import click
import numpy as np
from itertools import combinations
from tqdm import tqdm

from opti_fit.utils.dataset_utils import OVERVIEW_COLUMNS, get_algorithms_from_df, get_hash
from opti_fit.utils.model_utils import analyze_performance
from opti_fit.utils.runner_utils import (
    merge_performance_and_cutoff_output,
    parse_and_validate_runner_input,
    print_and_write_results,
)


@click.command()
@click.option("--base_model_type", default="hit", help="The base model type [hit, payment, combined]")
@click.option("--dataset", default="full_dataset.csv.gz", help="Name of dataset")
@click.option("--to_file", default=True, help="Whether to write the result to file")
@click.option("--solver_name", default="CBC", help="Name of solver to use ['GUROBI', 'CBC', 'HIGHS']")
def run_algorithm_combination(base_model_type: str, dataset: str, to_file: bool, solver_name: str):
    base_model_name = "simple_" + base_model_type
    base_model, df = parse_and_validate_runner_input(base_model_name, solver_name, dataset)
    df_hash = get_hash(df)
    config_df = pd.DataFrame.from_dict(
        {"base_model": base_model_name, "df_hash": get_hash(df), "solver_name": solver_name},
        orient="index",
        columns=["Value"],
    )

    result_df = iterate_over_combinations(df, base_model, solver_name)

    filename = f"results/combination_{base_model_name}_{solver_name}_{df_hash}.json"
    print_and_write_results(config_df, result_df, to_file, filename)


def iterate_over_combinations(df: pd.DataFrame, base_model: Callable, solver_name: str) -> list[tuple]:
    original_algorithms = get_algorithms_from_df(df)
    algorithm_combinations = set([frozenset(combination) for combination in combinations(original_algorithms, 2)])
    weighting = np.linspace(0.1, 0.9, 5)
    result_df = pd.DataFrame()

    for algorithms_set in tqdm(algorithm_combinations):
        algorithms = list(algorithms_set)
        string_rep = get_string_representation(algorithms)

        for weight in weighting:
            instance = (string_rep, weight)
            print(f"Solving {str(instance)}")
            df = update_df(df, algorithms, original_algorithms, weight)

            cutoffs = base_model(df, solver_name)
            if any([c is None for c in cutoffs.values()]):
                continue
            performance = analyze_performance(df, cutoffs)

            # Update the result_df
            merged_result, column_names = merge_performance_and_cutoff_output(performance, cutoffs)
            result_data = instance + merged_result
            columns = ["algorithms", "weight"] + column_names

            result = pd.DataFrame(data=result_data, columns=columns)
            result.rename(columns={f"cutoff_{string_rep}": "new_cutoff"}, inplace=True)
            result_df = result_df.append(result)

    return result


def get_string_representation(algorithms: list[str]) -> str:
    return algorithms[0] + "," + algorithms[1]


def update_df(df: pd.DataFrame, algorithms: list[str], original_algorithms: list[str], weight: float) -> pd.DataFrame:
    df.drop(
        columns=[c for c in df.columns if c not in OVERVIEW_COLUMNS + original_algorithms], inplace=True
    )  # Clean-up first
    string_rep = get_string_representation(algorithms)
    df[string_rep] = df.apply(lambda row: weight * row[algorithms[0]] + (1 - weight) * row[algorithms[1]], axis=1)
    return df


if __name__ == "__main__":
    run_algorithm_combination()
