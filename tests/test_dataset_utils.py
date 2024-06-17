from opti_fit.dataset_utils import read_dataset


def test_read_dataset():
    read_dataset("data/small_dataset.csv.gz")
