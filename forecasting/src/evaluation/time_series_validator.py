import pandas as pd

class TimeSeriesValidator:
    def __init__(
        self,
        initial_window=24,
        horizon=1,
        step=1,
        max_splits=None,
        test_size=6
    ):
        self.initial_window = initial_window
        self.horizon = horizon
        self.step = step
        self.max_splits = max_splits
        self.test_size = test_size

        if initial_window < 1 or horizon < 1 or step < 1:
            raise ValueError("Los parámetros deben ser positivos.")

        if test_size < 1:
            raise ValueError("test_size debe ser positivo.")

        if max_splits is not None and max_splits < 1:
            raise ValueError("max_splits debe ser positivo.")

    def _prepare_series(self, series):
        if not isinstance(series, pd.Series):
            raise TypeError("La entrada debe ser una pandas Series.")

        if not isinstance(series.index, pd.DatetimeIndex):
            raise TypeError("La serie debe tener un DatetimeIndex.")

        series = series.sort_index()

        if series.index.has_duplicates:
            raise ValueError("La serie contiene fechas duplicadas.")

        if series.isna().any():
            raise ValueError("La serie contiene valores faltantes.")

        return series

    def split(self, series):
        series = self._prepare_series(series)

        development = series.iloc[:-self.test_size]

        if len(development) < self.initial_window + self.horizon:
            raise ValueError(
                "No hay suficientes observaciones para generar "
                "las divisiones de validación y reservar el conjunto de prueba."
            )

        splits = []

        for train_end in range(
            self.initial_window,
            len(development) - self.horizon + 1,
            self.step
        ):
            splits.append({
                'fold': len(splits) + 1,
                'train': development.iloc[:train_end],
                'validation': development.iloc[
                    train_end:train_end + self.horizon
                ]
            })

        if self.max_splits is not None:
            splits = splits[-self.max_splits:]

        return splits

    def get_test_set(self, series):
        series = self._prepare_series(series)

        return (
            series.iloc[:-self.test_size],
            series.iloc[-self.test_size:]
        )

    def print_splits(self, splits):
        print(f"\nNúmero de divisiones: {len(splits)}")

        for item in splits:
            train = item['train']
            validation = item['validation']

            print(f"\nFold {item['fold']}")
            print(
                f"Entrenamiento: {train.index[0].date()} "
                f"a {train.index[-1].date()} "
                f"({len(train)} observaciones)"
            )
            print(
                f"Validación: {validation.index[0].date()} "
                f"a {validation.index[-1].date()} "
                f"({len(validation)} observaciones)"
            )