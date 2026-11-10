import numpy as np
import pandas as pd
from abc import abstractmethod
from src.models.base_model import BaseModel

class SupervisedTimeSeriesModel(BaseModel):
    def __init__(self, name):
        super().__init__(name)
        self.estimator = None
        self.max_lag = 12

    def _create_features(self, history, target_date, time_step):
        values = history.to_numpy(dtype=float)

        features = {
            'trend': time_step,
            'month_sin': np.sin(2 * np.pi * target_date.month / 12),
            'month_cos': np.cos(2 * np.pi * target_date.month / 12)
        }

        for lag in [1, 2, 3, 6, 12]:
            features[f'lag_{lag}'] = values[-lag]

        for window in [3, 6, 12]:
            features[f'rolling_mean_{window}'] = np.mean(
                values[-window:]
            )

        return features

    def fit(self, series):
        self.series = self._prepare_series(series)

        if len(self.series) < self.max_lag + 12:
            raise ValueError(
                f"Se necesitan al menos {self.max_lag + 12} "
                "observaciones para entrenar este modelo."
            )

        X = []
        y = []

        for i in range(self.max_lag, len(self.series)):
            history = self.series.iloc[:i]
            target_date = self.series.index[i]

            features = self._create_features(
                history,
                target_date,
                i
            )

            X.append(list(features.values()))
            y.append(self.series.iloc[i])

        self.estimator.fit(np.asarray(X), np.asarray(y))

        self.last_date = self.series.index[-1]
        self.is_fitted = True

        return self

    def predict(self, steps):
        self._validate_steps(steps)

        history = self.series.copy()
        future_dates = self._future_index(steps)
        predictions = []

        for i, date in enumerate(future_dates):
            features = self._create_features(
                history,
                date,
                len(history)
            )

            X = np.asarray([list(features.values())])
            predicted = float(self.estimator.predict(X)[0])

            predictions.append(predicted)

            history.loc[date] = predicted

        return pd.Series(
            predictions,
            index=future_dates,
            name='forecast'
        )
    """
    @abstractmethod
    def _build_estimator(self):
        pass
    """