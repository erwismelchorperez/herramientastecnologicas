from abc import ABC, abstractmethod
from numbers import Integral
import numpy as np
import pandas as pd

class BaseModel(ABC):
    def __init__(self, name):
        self.name = name
        self.series = None
        self.last_date = None
        self.is_fitted = False

    def _prepare_series(self, series):
        if not isinstance(series, pd.Series):
            raise TypeError("La entrada debe ser una pandas Series.")

        if not isinstance(series.index, pd.DatetimeIndex):
            raise TypeError("La serie debe tener un DatetimeIndex.")

        series = series.sort_index().astype(float)

        if series.empty:
            raise ValueError("La serie temporal está vacía.")

        if series.index.has_duplicates:
            raise ValueError("La serie contiene fechas duplicadas.")

        if series.isna().any():
            raise ValueError("La serie contiene valores faltantes.")

        if not np.isfinite(series.to_numpy()).all():
            raise ValueError("La serie contiene valores infinitos.")

        freq = pd.infer_freq(series.index)

        if freq is None:
            raise ValueError(
                "No se pudo inferir la frecuencia. "
                "Verifica que no existan periodos faltantes."
            )

        if not pd.tseries.frequencies.to_offset(freq).freqstr.startswith('ME'):
            raise ValueError(
                "La serie debe tener frecuencia mensual."
            )

        series.index = pd.DatetimeIndex(
            series.index,
            freq=freq,
            name=series.index.name
        )

        return series

    def _validate_steps(self, steps):
        if isinstance(steps, bool) or not isinstance(steps, Integral) or steps <= 0:
            raise ValueError("steps debe ser un entero positivo.")

        if not self.is_fitted:
            raise RuntimeError("El modelo todavía no ha sido entrenado.")

    def _future_index(self, steps):
        return pd.date_range(
            start=self.last_date + pd.offsets.MonthEnd(1),
            periods=steps,
            freq='ME',
            name='fecha'
        )

    @abstractmethod
    def fit(self, series):
        pass

    @abstractmethod
    def predict(self, steps):
        pass