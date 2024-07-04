import pandas as pd
from opti_fit.utils.dataset_utils import ALGORITHMS, OVERVIEW_COLUMNS
from pytest import fixture


@fixture
def simple_df():
    columns = OVERVIEW_COLUMNS + ALGORITHMS
    data = [
        (1, True, True, 100, 100, 100, 100, 100, 100),
        (1, True, False, 60, 70, 80, 75, 85, 90),
        (2, False, False, 95, 91, 90, 88, 92, 91),
        (3, False, False, 80, 90, 85, 75, 85, 90),
        (3, False, False, 10, 43, 66, 85, 89, 95),
        (3, False, False, 91, 80, 80, 92, 85, 90),
        (4, True, True, 91, 89, 92, 90, 88, 93),
        (4, True, False, 92, 90, 93, 95, 89, 88),
    ]
    df = pd.DataFrame(data=data, columns=columns)
    df.index.rename("hit_id", inplace=True)
    return df
