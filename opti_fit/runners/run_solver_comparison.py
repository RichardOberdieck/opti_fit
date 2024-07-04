import pandas as pd
import click
from time import time
from tqdm import tqdm

from opti_fit.utils.dataset_utils import get_hash
from opti_fit.utils.model_utils import analyze_performance
from opti_fit.utils.runner_utils import (
    PERFORMANCE_CUTOFF_COLUMNS,
    merge_performance_and_cutoff_output,
    parse_and_validate_runner_input,
    print_and_write_results,
)


@click.command()
@click.option("--model_name", default="simple_hit_mip", help="The model to solve")
@click.option("--n_seeds", default=5, help="Number of random seeds used")
@click.option("--full_dataset", default=True, help="Whether to use the full dataset")
@click.option("--to_file", default=True, help="Whether to write the result to file")
def run_solver_comparison(model_name: str, n_seeds: int, full_dataset: bool, to_file: bool):
    solvers = ["GUROBI", "CBC", "HIGHS"]
    model, df = parse_and_validate_runner_input(model_name=model_name, full_dataset=full_dataset)
    config_df = pd.DataFrame.from_dict(
        {"model": model_name, "df_hash": get_hash(df), "n_seeds": n_seeds}, orient="index", columns=["Value"]
    )

    results = []

    for solver_name in tqdm(solvers):
        for seed in range(n_seeds):
            print(f"Running {solver_name} - {seed}")
            start = time()
            cutoffs = model(df, solver_name, seed)
            runtime = time() - start
            performance_df = analyze_performance(df, cutoffs)
            results.append((solver_name, seed, runtime) + merge_performance_and_cutoff_output(performance_df, cutoffs))

    columns = ["solver_name", "seed", "runtime"] + PERFORMANCE_CUTOFF_COLUMNS
    result_df = pd.DataFrame.from_records(data=results, columns=columns)
    filename = f"results/solver_comparison_{model_name}_{n_seeds}_{get_hash(df)}.json"
    print_and_write_results(config_df, result_df, to_file, filename)


if __name__ == "__main__":
    run_solver_comparison()
