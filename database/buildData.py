import pandas as pd
import numpy as np
from randomDateGen import randomDateGen

class buildData:
    """ 
    Building data for model training
    """ 
    
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.data = pd.DataFrame()
        print(f"Experiment {self.experiment_name} initialized.")
    
    def _create_df_Xy(self):
        """
        Create dataframe with X and y
        """
        self.data = pd.DataFrame(self.X, 
                columns= [f"feat_{i}" for i in range(self.X.shape[1])])
        self.data['target'] = self.y
        
    def _create_id(self):
        """
        Create Id column
        """
        self.data.loc[:,'id'] = "id_" + self.data.index.astype(str)
        
    def _create_timestamp(self):
        """
        Create timestamp column
        """
        random_date_gen = randomDateGen(self.data.shape[0])
        self.data.loc[:,'timestamp'] = random_date_gen.format_ls()
        
    
    def regression_data(self, n_samples, n_features, 
                n_informative, n_targets=1, noise=0.0, 
                shuffle=False, random_state=101, 
                id_col=False, timestamp_col=False):
        """
        Generate data for regression
        """
        from sklearn.datasets import make_regression
        self.X, self.y = make_regression(n_samples=n_samples, n_features=n_features,
                                n_informative=n_informative, n_targets=n_targets,
                                noise=noise, shuffle=shuffle, random_state=random_state)             
        self._create_df_Xy()
        if id_col:self._create_id()
        if timestamp_col:self._create_timestamp()
        return self.data
    
    def data_profile(self):
        """
        Print data profile
        """
        if self.data.empty:
            print("Data is empty.")
        else:
            print(f"Shape of data: {self.data.shape}")
            print(f"Data columns: \n{self.data.columns}")