import pandas as pd

class ModelSelector:
    def __init__(self, metric='WAPE'):
        self.metric = metric.upper()
        self.metric_columns = {
            'MAE': 'MAE',
            'RMSE': 'RMSE',
            'SMAPE': 'sMAPE',
            'WAPE': 'WAPE'
        }
        if self.metric not in self.metric_columns:
            raise ValueError(
                f"Métrica no válida. Opciones: {list(self.metric_columns)}"
            )
        self.best_model = None
        self.ranking = None

    def select(self, metrics):
        if metrics.empty:
            raise ValueError("No existen métricas para seleccionar.")

        metric_column = self.metric_columns[self.metric]

        if metric_column not in metrics.columns:
            raise ValueError(f"No existe la métrica {metric_column}.")

        ranking = metrics.dropna(subset=[metric_column]).copy()

        if ranking.empty:
            raise ValueError("No existen modelos con métricas válidas.")

        ranking = ranking.sort_values(
            metric_column,
            ascending=True
        ).reset_index(drop=True)

        ranking['ranking'] = range(1, len(ranking) + 1)

        self.ranking = ranking
        self.best_model = ranking.iloc[0]['model']

        return {
            'best_model': self.best_model,
            'ranking': self.ranking
        }

    def print_report(self):
        if self.ranking is None:
            raise RuntimeError("Primero debes ejecutar select().")

        metric_column = self.metric_columns[self.metric]

        print("\nSELECCIÓN DEL MODELO")
        print("-" * 65)
        print(f"Criterio: {metric_column}")
        print(self.ranking.to_string(index=False))
        print(f"\nModelo seleccionado: {self.best_model}")