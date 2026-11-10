from pathlib import Path
import pandas as pd

from src.models.model_factory import ModelFactory
from src.models.final_model_trainer import FinalModelTrainer
from src.evaluation.time_series_validator import TimeSeriesValidator
from src.models.model_trainer import ModelTrainer
from src.evaluation.model_evaluator import ModelEvaluator
from src.models.model_tester import ModelTester
from src.forecasting.forecaster import Forecaster
from src.visualization.forecast_plotter import ForecastPlotter


def main():

    # Configuración del indicador que se desea pronosticar
    target_column = 'cvencido'
    target_name = 'capital_vencido'
    target_label = 'Capital vencido'

    output_dir = Path('data/results')
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Cargar histórico actualizado
    df = pd.read_csv('data/processed/cartera_institucion.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    df = df.sort_values('fecha')

    if target_column not in df.columns:
        raise ValueError(
            f"La columna '{target_column}' no existe en el histórico."
        )

    series = (
        df.set_index('fecha')[target_column]
        .astype(float)
        .sort_index()
    )

    if series.empty:
        raise ValueError("No existen datos históricos para generar el pronóstico.")

    if series.index.has_duplicates:
        raise ValueError("Existen fechas duplicadas en la serie histórica.")

    print("\nDIAGNÓSTICO DE LA SERIE")
    print("-" * 55)

    print(f"Total de observaciones: {len(series)}")
    print(f"Valores faltantes: {series.isna().sum()}")

    if series.isna().any():
        print("\nFechas con valores faltantes:")
        print(series[series.isna()])

    print("\nEstadísticas:")
    print(series.describe())

    print("\nREGISTROS DEL HISTÓRICO PROCESADO")
    print("-" * 65)

    print(
        df.loc[
            df['cvigente'].isna(),
            ['fecha', 'cvigente']
        ].to_string(index=False)
    )

    print("\nREGISTROS COMPLETOS DE DICIEMBRE 2023 A MAYO 2024")
    print("-" * 65)

    print(
        df.loc[
            (df['fecha'] >= '2023-12-01') &
            (df['fecha'] <= '2024-05-31')
        ].to_string(index=False)
    )


    print("\n" + "=" * 65)
    print("PRONÓSTICO DE CAPITAL VIGENTE")
    print("=" * 65)
    print(f"Primer periodo histórico: {series.index[0].date()}")
    print(f"Último periodo histórico: {series.index[-1].date()}")
    print(f"Observaciones disponibles: {len(series)}")

    # 2. Configurar modelos y validación temporal
    factory = ModelFactory(seasonal_periods=12)

    validator = TimeSeriesValidator(initial_window=18,horizon=3,step=1, max_splits=6,test_size=6)

    # 3. Entrenar y comparar modelos mediante validación temporal
    print("\n[1/6] Comparando modelos candidatos...")

    trainer = ModelTrainer(
        factory=factory,
        validator=validator
    )

    print("\nDIAGNÓSTICO DE VALIDACIÓN TEMPORAL")
    print("-" * 60)

    print(f"Observaciones de la serie: {len(series)}")
    print(f"Ventana inicial: {validator.initial_window}")
    print(f"Horizonte: {validator.horizon}")
    print(f"Paso: {validator.step}")
    print(f"Tamaño del conjunto de prueba: {validator.test_size}")

    development = series.iloc[:-validator.test_size]

    print(f"Observaciones para desarrollo: {len(development)}")
    print(
        "Observaciones mínimas necesarias:",
        validator.initial_window + validator.horizon
    )

    print(
        "¿Es posible generar divisiones?:",
        len(development) >= validator.initial_window + validator.horizon
    )

    training_results = trainer.train(series)

    if training_results['results'].empty:
        raise RuntimeError("Ningún modelo pudo completar la validación temporal.")

    training_results['results'].to_csv(
        output_dir / f'resultados_validacion_{target_name}.csv',
        index=False
    )

    if not training_results['failures'].empty:
        training_results['failures'].to_csv(
            output_dir / f'fallos_modelos_{target_name}_failures.csv',
            index=False
        )

    # 4. Evaluar y seleccionar el mejor modelo
    print("\n[2/6] Evaluando modelos...")

    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate(training_results['results'])

    metrics.to_csv(
        output_dir / 'metricas_modelos.csv',
        index=False
    )

    print("\nCOMPARACIÓN DE MODELOS")
    print("-" * 75)
    print(metrics.to_string(index=False))

    valid_metrics = metrics[
        metrics['WAPE'].notna() &
        metrics['WAPE'].map(lambda value: pd.notna(value) and value >= 0)
    ]

    if valid_metrics.empty:
        raise RuntimeError("No existen modelos con métricas WAPE válidas.")

    best = valid_metrics.iloc[0]
    best_model = best['model']
    best_wape = best['WAPE']

    print(f"\nModelo seleccionado: {best_model}")
    print(f"WAPE de validación: {best_wape:.4f}%")

    # 5. Evaluar el modelo seleccionado con el conjunto de prueba final
    print("\n[3/6] Evaluando el modelo con los últimos seis meses...")

    tester = ModelTester(
        factory=factory,
        validator=validator
    )

    test_output = tester.test(
        series=series,
        model_name=best_model
    )

    print("\nContenido devuelto por ModelTester:")
    print(test_output.keys())

    test_results = test_output['results']


    if test_results.empty:
        raise RuntimeError("No se generaron resultados para el conjunto de prueba.")

    test_results.to_csv(
        output_dir / f'resultados_prueba_final_{target_name}.csv',
        index=False
    )

    test_evaluator = ModelEvaluator()
    test_metrics = test_evaluator.evaluate(test_results)

    test_metrics.to_csv(
        output_dir / f'metricas_prueba_final_{target_name}.csv',
        index=False
    )

    print("\nRESULTADOS DEL CONJUNTO DE PRUEBA")
    print("-" * 75)
    print(test_metrics.to_string(index=False))

    # 6. Entrenar el modelo definitivo con todo el histórico
    print("\n[4/6] Entrenando el modelo definitivo...")

    final_trainer = FinalModelTrainer(factory=factory)

    training = final_trainer.train(
        series=series,
        model_name=best_model,
        target=target_name,
        metric='WAPE',
        metric_value=float(best_wape)
    )

    filename = training['filename']

    print(f"\nModelo definitivo guardado: {filename}")

    # 7. Generar pronóstico de los siguientes seis meses
    print("\n[5/6] Generando pronóstico...")

    forecaster = Forecaster()
    forecast = forecaster.forecast(
        filename=filename,
        steps=6
    )

    first_date = forecast['fecha'].min()
    last_date = forecast['fecha'].max()

    forecast_filename = (
        f"pronostico_{target_name}_"
        f"{first_date:%Y%m}_{last_date:%Y%m}.csv"
    )

    forecast_path = output_dir / forecast_filename
    forecast.to_csv(forecast_path, index=False)

    print("\nPRONÓSTICO DE CAPITAL VIGENTE")
    print("-" * 65)
    print(forecast.to_string(index=False))

    # 8. Generar gráfica
    print("\n[6/6] Generando gráfica...")

    plotter = ForecastPlotter()

    plot_path = plotter.plot(
        history=series,
        forecast=forecast,
        target=target_label,
        history_periods=24,
        ylabel='Capital ($)'
    )

    print("\n" + "=" * 65)
    print("PROCESO FINALIZADO")
    print("=" * 65)
    print(f"Modelo seleccionado: {best_model}")
    print(f"Modelo guardado: {filename}")
    print(f"Pronóstico: {forecast_path}")
    print(f"Gráfica: {plot_path}")


if __name__ == '__main__':
    main()