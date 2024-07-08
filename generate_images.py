from opti_fit.dataset_utils import read_dataset
import pandas as pd
from tqdm import tqdm
import plotly.express as px
from plotly.io import to_json


def generate_hit_images():
    df = read_dataset("data/full_dataset.csv.gz", validate=False)
    payment_df = df.groupby("payment_case_id", group_keys=True)[["is_payment_true_hit", "is_hit_true_hit"]].apply(
        lambda row: row
    )
    payment_ids = payment_df.index.get_level_values("payment_case_id").unique()
    data = []
    for payment_id in tqdm(payment_ids):
        hit_df = payment_df.loc[payment_id]
        data.append([payment_id, hit_df["is_payment_true_hit"].all(), len(hit_df), hit_df["is_hit_true_hit"].sum()])
    data_df = pd.DataFrame.from_records(
        data, columns=["payment_case_id", "is_payment_true_hit", "number_of_hits", "number_of_true_hits"]
    )

    fig = px.histogram(
        data_df[data_df["is_payment_true_hit"]],
        x="number_of_hits",
        title="Number of hits per true positive payment",
    )
    fig.update_layout(
        xaxis_title="Number of Hits",
        yaxis_title="Count",
    )
    with open("docs/hit_distribution_true_positive.json", "w") as file:
        file.write(to_json(fig))

    fig = px.histogram(
        data_df[~data_df["is_payment_true_hit"]],
        x="number_of_hits",
        title="Number of hits per false positive payment",
    )
    fig.update_layout(
        xaxis_title="Number of Hits",
        yaxis_title="Count",
    )
    with open("docs/hit_distribution_false_positive.json", "w") as file:
        file.write(to_json(fig))


def generate_relaxed_solution_image():
    _ = pd.read_json("results/")
