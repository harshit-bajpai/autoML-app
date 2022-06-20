import time
import random
import numpy as np

class randomDateGen():
    """
    Generate a list of random dates.

    Parameters
    ----------
    n_samples : int
        Number of samples to generate.
    seed : int
        Seed for random number generator.
    max_num_days : int
        Upper bound for time delta randomizer.
    """

    def __init__(self, n_samples:int, seed:int=101 , max_n_days:int=7):
        self.seed = seed
        self.n_samples = n_samples
        self.max_n_days = max_n_days
        self.start_datetime = self._get_start_datetime()
        self.timedelta = self._get_timedelta()
        self.datetime_ls = self.datetime_ls()

    def _get_start_datetime(self) -> int:
        random.seed(self.seed)
        return np.random.randint(1, time.time())
    
    def _get_timedelta(self) -> int:
        random.seed(self.seed)
        DAY_TOTAL_SEC = 24*60*60
        return np.random.randint(1, self.max_n_days*DAY_TOTAL_SEC)
    
    def datetime_ls(self) -> list:
        return [self.start_datetime + 
            i*self.timedelta for i in range(self.n_samples)]
    
    def format_ls(self, fmt:str='%Y-%m-%d %H:%M:%S') -> list:
        return [time.strftime(fmt, time.localtime(i)) \
             for i in self.datetime_ls]