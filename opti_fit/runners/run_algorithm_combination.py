from typing import Callable
import pandas as pd
import click
import numpy as np
from itertools import combinations
from tqdm import tqdm

from opti_fit.utils.dataset_utils import ALGORITHMS, OVERVIEW_COLUMNS, Algorithm, get_hash
from opti_fit.utils.model_utils import analyze_performance
from opti_fit.utils.runner_utils import (
    PERFORMANCE_CUTOFF_COLUMNS,
    merge_performance_and_cutoff_output,
    parse_and_validate_runner_input,
    print_and_write_results,
)


@click.command()
@click.option(
    "--base_model_name",
    default="simple_hit",
    help="The base model to use for the combination. Has to be a simple model",
)
@click.option("--full_dataset", default=True, help="Whether to use the full dataset")
@click.option("--to_file", default=True, help="Whether to write the result to file")
@click.option("--solver_name", default="CBC", help="Name of solver to use ['GUROBI', 'CBC', 'HIGHS']")
def run_algorithm_combination(base_model_name: str, full_dataset: bool, to_file: bool, solver_name: str):
    if "simple" not in base_model_name:
        raise ValueError(f"Invalid model name, should be 'simple_*', but got {base_model_name}")
    base_model, df = parse_and_validate_runner_input(base_model_name, solver_name, full_dataset)
    config_df = pd.DataFrame.from_dict(
        {"base_model": base_model_name, "df_hash": get_hash(df), "solver_name": solver_name},
        orient="index",
        columns=["Value"],
    )

    result = iterate_over_combinations(df, base_model, solver_name)

    result_df = pd.DataFrame.from_records(
        result, columns=["algorithm_A", "algorithm_B", "weight"] + PERFORMANCE_CUTOFF_COLUMNS + ["new_cutoff"]
    )
    result_df.sort_values(by="removed_false_positive_hits", axis=1, inplace=True, ascending=False)
    filename = f"results/{base_model_name}_{solver_name}_{get_hash(df)}.json"
    print_and_write_results(config_df, result_df, to_file, filename)


def iterate_over_combinations(df: pd.DataFrame, base_model: Callable, solver_name: str) -> list[tuple]:
    algorithm_combinations = set([frozenset(combination) for combination in combinations(ALGORITHMS, 2)])
    weighting = np.linspace(0.1, 0.9, 5)
    result = []

    for algorithms_set in tqdm(algorithm_combinations):
        algorithms = list(algorithms_set)
        string_rep = get_string_representation(algorithms)

        for weight in weighting:
            instance = (string_rep, weight)
            print(f"Solving {str(instance)}")
            df = update_df(df, algorithms, weight)

            cutoffs = base_model(df, solver_name)

            performance = analyze_performance(df, cutoffs)
            result.append(instance + merge_performance_and_cutoff_output(performance, cutoffs) + (cutoffs[string_rep],))

    return result


def get_string_representation(algorithms: list[Algorithm]) -> str:
    return algorithms[0] + "," + algorithms[1]


def update_df(df: pd.DataFrame, algorithms: list[Algorithm], weight: float) -> pd.DataFrame:
    df.drop(columns=[c for c in df.columns if c not in OVERVIEW_COLUMNS + ALGORITHMS], inplace=True)  # Clean-up first
    string_rep = get_string_representation(algorithms)
    df[string_rep] = df.apply(lambda row: weight * row[algorithms[0]] + (1 - weight) * row[algorithms[1]], axis=1)
    return df


if __name__ == "__main__":
    run_algorithm_combination()
