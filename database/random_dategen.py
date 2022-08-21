"""
"random_dategen" is a module that generates random list of dates.
"""
import random
import time

import numpy as np

DAYS_TO_SEC = 24 * 60 * 60


class RandomDateGen:
    """
    Generate a list of random dates.co

    Parameters
    ----------
    n_samples : int
        Number of samples to generate.
    seed : int
        Seed for random number generator.
    max_num_days : int
        Upper bound for random time delta generator.
    """

    def __init__(self, n_samples: int, seed: int = 101, max_n_days: int = 7):
        self.seed = seed
        self.n_samples = n_samples
        self.max_n_days = max_n_days
        self.start_datetime: int = self._get_start_datetime()
        self.timedelta: int = self._get_timedelta()
        self.datetime_list: list[int] = self._datetime_ls()

    def _get_start_datetime(self) -> int:
        random.seed(self.seed)
        return np.random.randint(1, int(time.time()))

    def _get_timedelta(self) -> int:
        random.seed(self.seed)
        return np.random.randint(1, self.max_n_days * DAYS_TO_SEC)

    def _datetime_ls(self) -> list[int]:
        return [self.start_datetime + i * self.timedelta for i in range(self.n_samples)]

    def format_ls(self, fmt: str = "%Y-%m-%d %H:%M:%S") -> list:
        """
        Returns a list of formatted datetime strings.

        Parameters
        ----------
        fmt : str
            Format string for datetime.strftime.
        """
        return [time.strftime(fmt, time.localtime(i)) for i in self.datetime_list]
