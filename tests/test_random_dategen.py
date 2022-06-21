"""
Unit tests for random_dategen module.
"""
import sys
import time

from database.random_dategen import RandomDateGen

sys.path.insert(1, "./database/")


def test_random_dategen() -> None:
    """
    Test default randomDataGen
    """
    rdg = RandomDateGen(10)
    assert rdg.n_samples == 10
    assert rdg.seed == 101
    assert rdg.max_n_days == 7
    assert rdg.start_datetime < time.time()
    assert rdg.start_datetime > 0
    assert rdg.timedelta > 0
    assert rdg.timedelta < rdg.max_n_days * 24 * 60 * 60
    assert len(rdg.datetime_list) == 10
    assert len(rdg.format_ls()) == 10
    assert rdg.format_ls()[0] == time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(rdg.datetime_list[0])
    )
