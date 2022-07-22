import logging
from typing import Union

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

SUPPORTED_MODELS_DICT = {"Linear Regression": LinearRegression}


class ModelTrain:
    def __init__(
        self,
        X_train: pd.DataFrame = pd.DataFrame(),
        y_train: pd.Series = pd.Series(),
        X_test: pd.DataFrame = pd.DataFrame(),
        y_test: pd.Series = pd.Series(),
        model_name: str = "LinearRegression",
        model_params: Union[dict, None] = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.model_name = model_name
        self.model_params = model_params
        self.logger.info("ModelTrain object initialized.")

    def _validate_model_name(self) -> Union[LinearRegression, None]:
        if self.model_name in SUPPORTED_MODELS_DICT:
            self.logger.debug(f"Model {self.model_name} is called.")
            return self._model_init_()
        else:
            raise ValueError("Model name not supported.")

    def _model_init_(self) -> Union[LinearRegression, None]:
        if self.model_params is None:
            return SUPPORTED_MODELS_DICT[self.model_name]()
        return SUPPORTED_MODELS_DICT[self.model_name](**self.model_params)

    def train(self) -> None:
        self.model = self._validate_model_name()
        self.logger.debug(f"Model {self.model_name} is called.")
        self.model.fit(self.X_train, self.y_train)
        self.logger.info("Model training done.")

    def evaluate(self) -> None:
        self.logger.info("Model evaluation.")
        self.y_pred = self.model.predict(self.X_test)
        self.logger.info("Model evaluation done.")

    def get_metrics(self) -> str:
        metrics = f"Mean squared error: {mean_squared_error(self.y_test, self.y_pred)}"
        self.logger.info(f"Model metrics: {metrics}")
        return metrics
