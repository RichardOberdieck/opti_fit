from glob import glob
from os import path

from opti_fit.utils.dataset_utils import read_dataset


def test_read_dataset_works_for_files():
    for file in glob(path.join("data", "*.csv.gz")):
        read_dataset(file)
