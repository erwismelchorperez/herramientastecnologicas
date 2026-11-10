import numpy as np
import pandas as pd
from numbers import Integral
from src.models.base_model import BaseModel

class SeasonalNaiveModel(BaseModel):
    def __init__(self, seasonal_periods=12):
        super().__init__('SeasonalNaive')

        if (
            isinstance(seasonal_periods, bool)
            or not isinstance(seasonal_periods, Integral)
            or seasonal_periods < 1
        ):
            raise ValueError(
                "seasonal_periods debe ser un entero positivo."
            )

        self.seasonal_periods = seasonal_periods
        self.last_season = None

    def fit(self, series):
        self.series = self._prepare_series(series)

        if len(self.series) < self.seasonal_periods:
            raise ValueError(
                f"Se necesitan al menos {self.seasonal_periods} "
                "observaciones para entrenar Seasonal Naive."
            )

        self.last_date = self.series.index[-1]
        self.last_season = self.series.iloc[
            -self.seasonal_periods:
        ].to_numpy()

        self.is_fitted = True
        return self

    def predict(self, steps):
        self._validate_steps(steps)

        values = np.resize(self.last_season, steps)

        return pd.Series(
            values,
            index=self._future_index(steps),
            name='forecast'
        )