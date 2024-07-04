import os
import pandas as pd
import click
from time import time
from tqdm import tqdm

from opti_fit.utils.dataset_utils import Algorithm, read_dataset
from opti_fit.utils.model_utils import analyze_performance
from opti_fit.models.models import Model


@click.command()
@click.option("--model", default="simple_hit_mip", help="The model to solve")
@click.option("--n_seeds", default=5, help="Number of random seeds used")
@click.option("--full_dataset", default=True, help="Whether to use the full dataset")
@click.option("--to_file", default=True, help="Whether to write the result to file")
def compare_solvers(model: str, n_seeds: int, full_dataset: bool, to_file: bool):
    solvers = ["GUROBI", "CBC", "HIGHS"]
    model = Model(model)
    filename = "full_dataset.csv.gz" if full_dataset else "small_dataset.csv.gz"
    df = read_dataset(os.path.join("data", filename))

    columns = [
        "solver_name",
        "seed",
        "runtime",
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
    results = []

    for solver_name in tqdm(solvers):
        for seed in range(n_seeds):
            start = time()
            cutoffs = model.run(df, solver_name, seed)
            runtime = time() - start
            performance_df = analyze_performance(df, cutoffs)
            results.append(
                (
                    solver_name,
                    seed,
                    runtime,
                    performance_df.loc["Hits", "Removed False Positive [absolute]"],
                    performance_df.loc["Hits", "Removed True Positive [absolute]"],
                    performance_df.loc["Payment", "Removed False Positive [absolute]"],
                    performance_df.loc["Payment", "Removed True Positive [absolute]"],
                    cutoffs[Algorithm("regex_match")],
                    cutoffs[Algorithm("jaro_winkler")],
                    cutoffs[Algorithm("fuzz_ratio")],
                    cutoffs[Algorithm("fuzz_partial_ratio")],
                    cutoffs[Algorithm("fuzz_token_sort_ratio")],
                    cutoffs[Algorithm("fuzz_partial_token_sort_ratio")],
                )
            )

    result_df = pd.DataFrame.from_records(data=results, columns=columns)

    print("Results:")
    print(result_df.to_markdown())

    if to_file:
        filename = f"results/solver_comparison_{model.value}_{full_dataset}_{n_seeds}.xlsx"
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            result_df.to_excel(writer, sheet_name="Results")
        print(f"Written to {filename}")


if __name__ == "__main__":
    compare_solvers()
