import pandas as pd

class buildData:
    """ 
    Building data for model training
    """ 
    
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.data = pd.DataFrame()
        print(f"Experiment {self.experiment_name} initialized.")
    
    def create_df_Xy(self):
        """
        Create dataframe with X and y
        """
        self.data = pd.DataFrame(self.X, 
                columns= [f"feat_{i}" for i in range(self.X.shape[1])])
        self.data['target'] = self.y
        return self.data
    
    def sklearn_regression_data(self, n_samples, n_features, 
                n_informative, n_targets, noise=0.0, 
                shuffle=False, random_state=101):
        """
        Generate data for sklearn regression
        """
        from sklearn.datasets import make_regression
        self.X, self.y = make_regression(n_samples=n_samples, n_features=n_features,
                                n_informative=n_informative, n_targets=n_targets,
                                noise=noise, shuffle=shuffle, random_state=random_state)             
        return self.create_df_Xy()
    
    def data_profile(self):
        """
        Print data profile
        """
        if self.data.empty:
            print("Data is empty.")
        else:
            print(f"Shape of data: {self.data.shape}")
            print(f"Data columns: \n{self.data.columns}")