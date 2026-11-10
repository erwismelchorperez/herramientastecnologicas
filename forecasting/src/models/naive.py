import pandas as pd
from src.models.base_model import BaseModel

class NaiveModel(BaseModel):
    def __init__(self):
        super().__init__('Naive')
        self.last_value = None

    def fit(self, series):
        self.series = self._prepare_series(series)
        self.last_date = self.series.index[-1]
        self.last_value = self.series.iloc[-1]
        self.is_fitted = True
        return self

    def predict(self, steps):
        self._validate_steps(steps)

        return pd.Series(
            [self.last_value] * steps,
            index=self._future_index(steps),
            name='forecast'
        )