"""
Unit test for build_data module.
"""
import sys

from database.build_data import BuildData

sys.path.insert(1, "./database/")


def test_build_data_default() -> None:
    """
    Test default buildData
    """
    bd = BuildData("test")
    assert bd.experiment_name == "test"
    assert bd.data.empty


def test_build_reg_data() -> None:
    """
    Test buildRegData
    """
    bd = BuildData("test")
    n_samples = 100
    n_features = 10
    n_informative = 5
    df = bd.regression_data(
        n_samples=n_samples, n_features=n_features, n_informative=n_informative
    )
    assert df.shape == bd.data.shape
    assert bd.data.shape == (n_samples, n_features + 1)
    assert bd.data.columns.tolist() == [f"feat_{i}" for i in range(n_features)] + [
        "target"
    ]
