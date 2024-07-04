import pandas as pd
import click

from opti_fit.utils.dataset_utils import get_hash
from opti_fit.utils.model_utils import analyze_performance
from opti_fit.utils.runner_utils import (
    PERFORMANCE_CUTOFF_COLUMNS,
    merge_performance_and_cutoff_output,
    parse_and_validate_runner_input,
    print_and_write_results,
)


@click.command()
@click.option("--model_name", default="simple_hit", help="The simple model to solve")
@click.option("--full_dataset", default=True, help="Whether to use the full dataset")
@click.option("--to_file", default=True, help="Whether to write the result to file")
@click.option("--solver_name", default="CBC", help="Name of solver to use ['GUROBI', 'CBC', 'HIGHS']")
def run_simple_model(model_name: str, full_dataset: bool, to_file: bool, solver_name: str):
    if "simple" not in model_name:
        raise ValueError(f"Invalid model name, should be 'simple_*', but got {model_name}")
    model, df = parse_and_validate_runner_input(model_name, solver_name, full_dataset)

    config_df = pd.DataFrame.from_dict(
        {"model": model_name, "df_hash": get_hash(df), "solver_name": solver_name}, orient="index", columns=["Value"]
    )

    cutoffs = model(df, solver_name)
    performance = analyze_performance(df, cutoffs)

    result_df = pd.DataFrame.from_records(
        data=[merge_performance_and_cutoff_output(performance, cutoffs)], columns=PERFORMANCE_CUTOFF_COLUMNS
    )
    filename = f"results/{model_name}_{solver_name}_{get_hash(df)}.json"
    print_and_write_results(config_df, result_df, to_file, filename)


if __name__ == "__main__":
    run_simple_model()
