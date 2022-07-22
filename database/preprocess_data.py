"""
Preprocessing the dataframe for model training.
- Handle non-numeric data
- Handle missing values
- Scale/normalize data
- Split data into train/test
"""

import logging
from typing import Tuple, Union

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

MISSING_VALUE_THRESHOLD = 0.2
SCALER_DICT = {"minmax": MinMaxScaler(), "standard": StandardScaler()}


class PreprocessData:
    """
    Preprocessing the dataframe for model training.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe to be preprocessed.
    test_ratio : float
        Test data ratio.
    shuffle_flag : bool
        Shuffle data or not.
    sel_scaler : str
        Select scaler. "minmax" or "standard".
    target_col : str
        Target column name.
    """

    def __init__(
        self,
        data: pd.DataFrame = pd.DataFrame(),
        test_ratio: float = 0.2,
        shuffle_flag: bool = False,
        target_col: str = "target",
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.data = data
        self.test_ratio = test_ratio
        self.target_col = target_col
        self.shuffle_flag = shuffle_flag
        self.logger.info("PreprocessData object initialized.")

    def handle_non_numeric(self) -> Union[str, np.ndarray]:
        """
        Handle non-numeric data
        """
        cols_to_drop = self.data.select_dtypes(include=["object"]).columns.values
        if len(cols_to_drop) > 0:
            self.data = self.data.drop(cols_to_drop, axis=1)
            self.logger.debug("Dropping non-numeric data for columns: %s", cols_to_drop)
            self.logger.debug("Data shape: %s", self.data.shape)
            return cols_to_drop
        self.logger.debug("No non-numeric data found.")
        return "No non-numeric data found."

    def handle_missing_values(self) -> dict:
        """
        Handle missing values
        """
        missing_values = self.data.isnull().sum() / self.data.shape[0]
        cols_to_drop = missing_values[
            missing_values > MISSING_VALUE_THRESHOLD
        ].index.values
        ms_values: dict = {}
        if len(cols_to_drop) > 0:
            self.data.drop(columns=cols_to_drop, inplace=True)
            self.logger.info(
                "Dropping columns with missing values for columns: %s", cols_to_drop
            )
            ms_values[
                "cols_drop"
            ] = f"Dropping columns with missing values greater than {MISSING_VALUE_THRESHOLD*100} \n{cols_to_drop}%"
            self.logger.info("Data shape: %s", self.data.shape)

        if len(missing_values) - len(cols_to_drop) > 0:
            self.data.dropna(subset=[self.target_col], inplace=True)
            imputer = SimpleImputer(strategy="mean")
            self.data = pd.DataFrame(
                imputer.fit_transform(self.data), columns=self.data.columns
            )
            ms_values[
                "drop_na"
            ] = "Imputed missing values based on strategy SimpleImputer (mean)"
            self.logger.info("Imputed missing values.")

        return ms_values

    def split_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

        X_train, X_test, y_train, y_test = train_test_split(
            self.data.drop(columns=self.target_col),
            self.data[self.target_col],
            test_size=self.test_ratio,
            shuffle=self.shuffle_flag,
        )
        self.logger.info("Data split into train/test.")
        return X_train, X_test, y_train, y_test

    def scale_data(
        self, X_train, X_test, sel_scaler
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Scale/normalize data
        """

        scaler = SCALER_DICT[sel_scaler]
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train), columns=X_train.columns
        )
        X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
        self.logger.info("Scaled data.")
        return X_train_scaled, X_test_scaled

    # def preprocess_handler(
    #     self, return_data: bool = False
    # ) -> Union[None, Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]]:
    #     """
    #     Preprocess data
    #     """
    #     self._handle_non_numeric()
    #     # self._handle_missing_values()
    #     self._split_data()
    #     self._scale_data()
    #     self.logger.info("Preprocess data finished.")
    #     if return_data:
    #         return self.X_train, self.y_train, self.X_test, self.y_test
