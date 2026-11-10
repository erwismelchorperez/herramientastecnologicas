import numpy as np
import pandas as pd

class ModelEvaluator:
    def __init__(self):
        self.results = None
        self.metrics = None

    def _calculate_metrics(self, group):
        actual = group['actual'].to_numpy(dtype=float)
        forecast = group['forecast'].to_numpy(dtype=float)

        errors = actual - forecast
        abs_errors = np.abs(errors)

        mae = np.mean(abs_errors)
        rmse = np.sqrt(np.mean(errors ** 2))

        denominator = np.abs(actual) + np.abs(forecast)
        smape_values = np.divide(
            200 * abs_errors,
            denominator,
            out=np.zeros_like(abs_errors),
            where=denominator != 0
        )
        smape = np.mean(smape_values)

        total_actual = np.sum(np.abs(actual))
        wape = (
            np.sum(abs_errors) / total_actual * 100
            if total_actual != 0 else np.nan
        )

        return {
            'observations': len(actual),
            'MAE': mae,
            'RMSE': rmse,
            'sMAPE': smape,
            'WAPE': wape
        }

    def evaluate(self, results):
        required = {'model', 'actual', 'forecast'}
        missing = required - set(results.columns)

        if missing:
            raise ValueError(f"Faltan columnas: {missing}")

        if results.empty:
            raise ValueError("No existen resultados para evaluar.")

        if results[list(required)].isna().any().any():
            raise ValueError("Existen valores faltantes en los resultados.")

        if not np.isfinite(
            results[['actual', 'forecast']].to_numpy(dtype=float)
        ).all():
            raise ValueError("Existen valores infinitos en los resultados.")

        self.results = results.copy()

        metrics = []

        for model_name, group in self.results.groupby('model'):
            row = {'model': model_name}
            row.update(self._calculate_metrics(group))
            metrics.append(row)

        self.metrics = pd.DataFrame(metrics)

        self.metrics = (
            self.metrics
            .sort_values('WAPE', ascending=True)
            .reset_index(drop=True)
        )

        return self.metrics

    def print_report(self):
        if self.metrics is None:
            raise RuntimeError("Primero debes ejecutar evaluate().")

        print("\nCOMPARACIÓN DE MODELOS")
        print("-" * 75)
        print(self.metrics.to_string(index=False, float_format=lambda x: f"{x:,.4f}"))
        print("\nModelo con menor WAPE:")
        print(self.metrics.iloc[0]['model'])