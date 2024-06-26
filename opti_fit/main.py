import os
import pandas as pd
import click

from opti_fit.dataset_utils import read_dataset
from opti_fit.model_utils import Model, analyze_performance


@click.command()
@click.option("--model", default="simple_hit_mip", help="The model to solve")
@click.option("--full_dataset", default=True, help="Whether to use the full dataset")
@click.option("--to_file", default=True, help="Whether to write the result to file")
def run_model(model: str, full_dataset: bool, to_file: bool):
    model = Model(model)

    filename = "full_dataset.csv.gz" if full_dataset else "small_dataset.csv.gz"
    df = read_dataset(os.path.join("data", filename))

    cutoffs = model.run(df)
    config_df = pd.DataFrame.from_dict(
        {"model": model, "full_dataset": full_dataset}, orient="index", columns=["Value"]
    )
    performance_df = analyze_performance(df, cutoffs)
    cutoffs_df = pd.DataFrame.from_dict(cutoffs, orient="index", columns=["Cutoff value"])

    print("Configuration:")
    print(config_df.to_markdown(tablefmt="psql", floatfmt=".0f"))
    print("Performance:")
    print(performance_df.to_markdown(tablefmt="psql", floatfmt=".2f"))
    print("Cutoffs:")
    print(cutoffs_df.to_markdown(tablefmt="psql", floatfmt=".2f"))

    if to_file:
        filename = f"{model.value}_{full_dataset}.xlsx"
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            config_df.to_excel(writer, sheet_name="Configuration")
            performance_df.to_excel(writer, sheet_name="Performance")
            cutoffs_df.to_excel(writer, sheet_name="Cutoffs")
        print(f"Written to {filename}")


if __name__ == "__main__":
    run_model()
