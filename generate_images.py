from opti_fit.dataset_utils import read_dataset
import pandas as pd
from tqdm import tqdm
import plotly.express as px
from plotly.io import to_json
import json

hash_value = "e1c2a078d4abcdf595e7723689d4213d6a8c24dc"


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
    with open(f"results/relaxed_hit_GUROBI_[0.95, 0.96, 0.97, 0.98, 0.99, 0.999]_{hash_value}.json") as file:
        data = json.load(file)

    results = pd.DataFrame.from_dict(data[1], orient="index")  # The first entry is the configuration
    results["slack"] = 1 - results["slack"]

    with open(f"results/simple_hit_GUROBI_{hash_value}.json") as file:
        data = json.load(file)

    simple_results = pd.DataFrame.from_dict(data[1], orient="index")  # The first entry is the configuration
    simple_results["slack"] = 0
    results = pd.concat([results, simple_results])

    false_removed = pd.concat(
        [results["removed_false_positive_hits_percent"], results["removed_false_positive_payments_percent"]]
    )
    false_removed.rename("False positives removed [%]", inplace=True)
    false_removed = false_removed.reset_index()

    true_removed = pd.concat(
        [results["removed_true_positive_hits_percent"], results["removed_true_positive_payments_percent"]]
    )
    true_removed.rename("True positives removed [%]", inplace=True)
    true_removed = true_removed.reset_index()

    slacks = pd.concat([results["slack"], results["slack"]])
    slacks = slacks.reset_index()

    types = pd.concat([pd.Series(["Hit"] * len(results["slack"])), pd.Series(["Payment"] * len(results["slack"]))])
    types.rename("Type", inplace=True)
    types = types.reset_index()

    df = pd.concat(
        [
            slacks["slack"],
            false_removed["False positives removed [%]"],
            true_removed["True positives removed [%]"],
            types["Type"],
        ],
        axis=1,
    )

    fig = px.line(
        df,
        x="slack",
        y="False positives removed [%]",
        color="Type",
        title="False positives removed when introducing slack",
        markers=True,
    )
    fig.update_layout(xaxis_range=[0, 0.05], yaxis_range=[0, 45])
    with open("docs/relaxed-hit-model-results.json", "w") as file:
        file.write(to_json(fig))

    fig = px.line(
        df,
        y="False positives removed [%]",
        x="True positives removed [%]",
        color="Type",
        title="Pareto curve for introducing slack ",
        markers=True,
    )
    fig.show()
    with open("docs/relaxed-hit-model-pareto.json", "w") as file:
        file.write(to_json(fig))
