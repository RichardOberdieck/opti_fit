import pandas as pd
import click

from opti_fit.utils.dataset_utils import get_hash
from opti_fit.utils.model_utils import analyze_performance
from opti_fit.utils.runner_utils import (
    merge_performance_and_cutoff_output,
    parse_and_validate_runner_input,
    print_and_write_results,
)


@click.command()
@click.option("--model_type", default="hit", help="The model type [hit, payment]")
@click.option("--dataset", default="full_dataset.csv.gz", help="Name of dataset")
@click.option("--to_file", default=True, help="Whether to write the result to file")
@click.option("--solver_name", default="CBC", help="Name of solver to use ['GUROBI', 'CBC', 'HIGHS']")
@click.option("--slacks", default="0.99", help="Single or list of fractions of true positives to keep")
def run_relaxed_model(model_type: str, dataset: str, to_file: bool, solver_name: str, slacks: list[float]):
    model_name = "relaxed_" + model_type
    model, df = parse_and_validate_runner_input(model_name, solver_name, dataset)
    slacks_str = slacks.split(",")
    slacks = [float(slack) for slack in slacks_str]

    config_df = pd.DataFrame.from_dict(
        {"model": model_name, "df_hash": get_hash(df), "solver_name": solver_name, "slacks": slacks},
        orient="index",
        columns=["Value"],
    )

    results = []

    for slack in slacks:
        cutoffs = model(df, solver_name, slack)
        performance = analyze_performance(df, cutoffs)
        result, columns = merge_performance_and_cutoff_output(performance, cutoffs)
        results.append((slack,) + result)

    columns = ["slack"] + columns
    result_df = pd.DataFrame.from_records(data=results, columns=columns)
    filename = f"results/{model_name}_{solver_name}_{str(slacks)}_{get_hash(df)}.json"
    print_and_write_results(config_df, result_df, to_file, filename)


if __name__ == "__main__":
    run_relaxed_model()
