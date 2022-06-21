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
