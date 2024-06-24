import os
import pandas as pd
import click

from opti_fit.dataset_utils import read_dataset
from opti_fit.model_utils import Model


@click.command()
@click.option("--model", default="simple_hit_mip", help="The model to solve")
@click.option("--full_dataset", default=True, help="Whether to use the full dataset")
@click.option(
    "--mps_filename",
    default=None,
    help="Filename of mps file. Set to None if it should not be written",
)
def run_model(model: str, full_dataset: bool, mps_filename: str | None):
    model = Model(model)

    filename = "full_dataset.csv.gz" if full_dataset else "small_dataset.csv.gz"
    df = read_dataset(os.path.join("data", filename))

    cutoffs, expected_hits = model.run(df, mps_filename)
    print("Cutoffs:")
    cutoffs_df = pd.DataFrame(cutoffs)
    print(cutoffs_df.to_markdown(tablefmt="psql", floatfmt=".1f"))

    print("Cutoffs:")
    expected_hits_df = pd.DataFrame(expected_hits)
    print(expected_hits_df.to_markdown(tablefmt="psql", floatfmt=".0f"))


if __name__ == "__main__":
    run_model()
