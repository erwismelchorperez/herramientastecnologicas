from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from src.models.supervised_model import SupervisedTimeSeriesModel

class LinearRegressionModel(SupervisedTimeSeriesModel):
    def __init__(self):
        super().__init__('LinearRegression')
        self.estimator = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', LinearRegression())
        ])