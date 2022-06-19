import time
import random
import numpy as np

class randomDateGen():

    def __init__(self, n_samples, seed=101):
        self.seed = seed
        self.n_samples = n_samples
        self._get_start_datetime()
        self._get_timedelta()

    def _get_start_datetime(self):
        random.seed(self.seed)
        self.start_date = np.random.randint(1, time.time())
    
    def _get_timedelta(self):
        random.seed(self.seed)
        self.time_delta = np.random.randint(1, 7*24*60*60)
    
    def datetime_ls(self):
        return [self.start_date + i*self.time_delta for i in range(self.n_samples)]
    
    def format_ls(self, fmt='%Y-%m-%d %H:%M:%S'):
        datetime_ls = self.datetime_ls()
        return [time.strftime(fmt, time.localtime(i)) for i in datetime_ls]