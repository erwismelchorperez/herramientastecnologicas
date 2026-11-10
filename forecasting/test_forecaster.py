from pathlib import Path
import pandas as pd

from src.forecasting.forecaster import Forecaster
from src.visualization.forecast_plotter import ForecastPlotter

def main():
    Path('data/results').mkdir(parents=True, exist_ok=True)

    # 1. Cargar historial
    df = pd.read_csv('data/processed/cartera_institucion.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])

    history = (
        df.set_index('fecha')['cvigente']
        .sort_index()
        .astype(float)
    )

    # 2. Generar pronósticos
    forecaster = Forecaster()

    forecast = forecaster.forecast(
        filename='capital_vigente_naive.pkl',
        steps=6
    )

    print("\nPRONÓSTICOS GENERADOS")
    print("-" * 60)
    print(forecast.to_string(index=False))

    # 3. Guardar resultados
    forecaster.save('data/results/pronostico_capital_vigente.csv')

    # 4. Generar gráfica
    plotter = ForecastPlotter()

    plotter.plot(
        history=history,
        forecast=forecast,
        target='capital_vigente',
        history_periods=24
    )

    print("\nProceso finalizado.")

if __name__ == '__main__':
    main()