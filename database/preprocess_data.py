"""
Preprocessing the dataframe for model training.
- Handle non-numeric data
- Handle missing values
- Scale/normalize data
- Split data into train/test
"""

import logging
from typing import Tuple, Union

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
        sel_scaler: str = "minmax",
        target_col: str = "target",
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.data = data
        self.test_ratio = test_ratio
        self.target_col = target_col
        self.shuffle_flag = shuffle_flag
        self.sel_scaler = sel_scaler
        self.X_train = pd.DataFrame()
        self.y_train = pd.Series(dtype="object")
        self.X_test = pd.DataFrame()
        self.y_test = pd.Series(dtype="object")
        self.logger.info("PreprocessData object initialized.")

    def _handle_non_numeric(self) -> None:
        """
        Handle non-numeric data
        """
        cols_to_drop = self.data.select_dtypes(include=["object"]).columns.values
        self.data = self.data.drop(cols_to_drop, axis=1)
        self.logger.info("Dropping non-numeric data for columns: %s", cols_to_drop)
        self.logger.info("Data shape: %s", self.data.shape)

    def _handle_missing_values(self) -> None:
        """
        Handle missing values
        """
        missing_values = self.data.isnull().sum() / self.data.shape[0]
        cols_to_drop = missing_values[
            missing_values > MISSING_VALUE_THRESHOLD
        ].index.values
        if len(cols_to_drop) > 0:
            self.data.drop(columns=cols_to_drop, inplace=True)
            self.logger.info(
                "Dropping columns with missing values for columns: %s", cols_to_drop
            )
            self.logger.info("Data shape: %s", self.data.shape)

        if len(missing_values) - len(cols_to_drop) > 0:
            self.data.dropna(subset=[self.target_col], inplace=True)
            imputer = SimpleImputer(strategy="mean")
            self.data = pd.DataFrame(
                imputer.fit_transform(self.data), columns=self.data.columns
            )
            self.logger.info("Imputed missing values.")

    def _split_data(self) -> None:

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.data.drop(columns=self.target_col),
            self.data[self.target_col],
            test_size=self.test_ratio,
            shuffle=self.shuffle_flag,
        )
        self.logger.info("Data split into train/test.")

    def _scale_data(self) -> None:
        """
        Scale/normalize data
        """

        scaler = SCALER_DICT[self.sel_scaler]
        self.X_train = pd.DataFrame(
            scaler.fit_transform(self.X_train), columns=self.X_train.columns
        )
        self.X_test = pd.DataFrame(
            scaler.transform(self.X_test), columns=self.X_test.columns
        )
        self.logger.info("Scaled data.")

    def preprocess_handler(
        self, return_data: bool = False
    ) -> Union[None, Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]]:
        """
        Preprocess data
        """
        self._handle_non_numeric()
        self._handle_missing_values()
        self._split_data()
        self._scale_data()
        self.logger.info("Preprocess data finished.")
        if return_data:
            return self.X_train, self.y_train, self.X_test, self.y_test
