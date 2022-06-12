import pandas as pd
from database.buildData import buildData

dataObj = buildData("laughing mantee")

df = dataObj.sklearn_regression_data(n_samples=100, n_features=2, 
        n_informative=1, n_targets=1)

print(df.shape)