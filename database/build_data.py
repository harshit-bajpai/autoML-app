"""
This is a docs string for the buildData.py file.
"""
import logging

import pandas as pd
from sklearn.datasets import make_regression

from database.random_dategen import RandomDateGen


class BuildData:
    """
    Building data for model training
    """

    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name
        self.data = pd.DataFrame()
        logging.info("Experiment %s buildData object initialized.", experiment_name)

    def _create_df_xy(self) -> None:
        """
        Create dataframe with X and y
        """
        self.data = pd.DataFrame(
            self.x, columns=[f"feat_{i}" for i in range(self.x.shape[1])]
        )
        self.data["target"] = self.y

    def _create_id(self) -> None:
        """
        Create Id column
        """
        self.data.loc[:, "id"] = "id_" + self.data.index.astype(str)

    def _create_timestamp(self) -> None:
        """
        Create timestamp column
        """
        random_date_gen = RandomDateGen(self.data.shape[0])
        self.data.loc[:, "timestamp"] = random_date_gen.format_ls()

    def regression_data(
        self,
        n_samples: int,
        n_features: int,
        n_informative: int,
        n_targets: int = 1,
        noise: float = 0.0,
        shuffle: bool = False,
        random_state: int = 101,
        id_col: bool = False,
        timestamp_col: bool = False,
    ) -> pd.DataFrame:
        """
        Generate data for regression
        """
        self.x, self.y, self.coef = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_informative,
            n_targets=n_targets,
            noise=noise,
            shuffle=shuffle,
            random_state=random_state,
        )
        self._create_df_xy()
        if id_col:
            self._create_id()
        if timestamp_col:
            self._create_timestamp()
        return self.data

    def data_profile(self) -> None:
        """
        Print data profile
        """
        if self.data.empty:
            print("Data is empty.")
        else:
            print(f"Shape of data: {self.data.shape}")
            print(f"Data columns: \n{self.data.columns}")
