"""
Unit test for preprocess_data.py
"""
import sys

import pandas as pd
from database.preprocess_data import PreprocessData

sys.path.insert(1, "./database/")


def test_preprocess_data_default():
    """
    Test default PreprocessData
    """
    ppd = PreprocessData()
    assert ppd.data.empty
    assert ppd.test_ratio == 0.2
    assert ppd.shuffle_flag is False
    assert ppd.sel_scaler == "minmax"
    assert ppd.X_train.empty
    assert ppd.y_train.empty
    assert ppd.X_test.empty
    assert ppd.y_test.empty
    assert ppd.logger is not None


def test_preprocess_data_dummy():
    """
    Test PreprocessData with dummy data
    """
    df = pd.read_csv("./tests/dummy_preprocess_data.csv")
    ppd = PreprocessData(data=df)
    ppd.preprocess_handler()
    assert ppd.data.shape == (94, 11)
    assert ppd.X_train.shape == (75, 10)
    assert ppd.y_train.shape == (75,)
    assert ppd.X_test.shape == (19, 10)
    assert ppd.y_test.shape == (19,)
