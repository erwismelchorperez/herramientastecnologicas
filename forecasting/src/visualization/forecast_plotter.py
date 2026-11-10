from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt


class ForecastPlotter:
    def __init__(self, output_dir='data/plots'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot(self, history, forecast, target, history_periods=24, ylabel=None):
        if not isinstance(history, pd.Series):
            raise TypeError("history debe ser una pandas Series.")

        if not isinstance(history.index, pd.DatetimeIndex):
            raise TypeError("history debe tener un DatetimeIndex.")

        if history.empty:
            raise ValueError("La serie histórica está vacía.")

        if not isinstance(forecast, pd.DataFrame):
            raise TypeError("forecast debe ser un pandas DataFrame.")

        required = {'fecha', 'forecast'}
        missing = required - set(forecast.columns)
        if missing:
            raise ValueError(f"Faltan columnas en forecast: {missing}")

        if forecast.empty:
            raise ValueError("No existen pronósticos para graficar.")

        if history_periods <= 0:
            raise ValueError("history_periods debe ser positivo.")

        history = history.sort_index().tail(history_periods)
        forecast = forecast.copy()
        forecast['fecha'] = pd.to_datetime(forecast['fecha'])
        forecast = forecast.sort_values('fecha')

        if history.isna().any() or forecast['forecast'].isna().any():
            raise ValueError("Existen valores faltantes en los datos.")

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(
            history.index,
            history.values,
            marker='o',
            label='Histórico'
        )

        ax.plot(
            forecast['fecha'],
            forecast['forecast'],
            marker='o',
            linestyle='--',
            label='Pronóstico'
        )

        ax.axvline(
            history.index[-1],
            linestyle=':',
            color='gray',
            label='Inicio del pronóstico'
        )

        ax.set_title(f"Pronóstico de {target}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel(ylabel or target)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend()

        fig.autofmt_xdate()
        fig.tight_layout()

        safe_target = re.sub(r'[^a-zA-Z0-9_-]+', '_', target.lower())
        filename = self.output_dir / f"pronostico_{safe_target}.png"

        fig.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)

        print(f"Gráfica guardada: {filename}")
        return filename