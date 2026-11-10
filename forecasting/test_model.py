from pathlib import Path
import pandas as pd

from src.models.model_factory import ModelFactory
from src.evaluation.time_series_validator import TimeSeriesValidator
from src.evaluation.model_selector import ModelSelector
from src.models.model_tester import ModelTester
from src.evaluation.model_evaluator import ModelEvaluator
from src.visualization.model_plotter import ModelPlotter

def main():
    Path('data/results').mkdir(parents=True, exist_ok=True)

    # 1. Cargar serie temporal
    df = pd.read_csv('data/processed/cartera_institucion.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])

    series = (
        df.set_index('fecha')['cvigente']
        .sort_index()
        .astype(float)
    )

    # 2. Recuperar el modelo seleccionado
    metrics = pd.read_csv('data/results/metricas_modelos.csv')

    selector = ModelSelector(metric='WAPE')
    selection = selector.select(metrics)
    model_name = selection['best_model']

    print(f"\nModelo seleccionado: {model_name}")

    # 3. Configurar evaluación temporal
    factory = ModelFactory()
    validator = TimeSeriesValidator(
        initial_window=24,
        horizon=1,
        step=1,
        test_size=6
    )

    # 4. Evaluar modelo en el conjunto de prueba
    tester = ModelTester(
        factory=factory,
        validator=validator
    )

    test_results = tester.test(series, model_name)
    tester.print_report()

    results = test_results['results']
    failures = test_results['failures']

    # 5. Guardar pronósticos y errores
    results.to_csv(
        'data/results/resultados_prueba.csv',
        index=False
    )

    if not failures.empty:
        failures.to_csv(
            'data/results/errores_prueba.csv',
            index=False
        )

    # 6. Calcular métricas del conjunto de prueba
    if len(results) != 6:
        raise ValueError(
            "La evaluación no generó los seis pronósticos esperados. "
            "Revisa los errores antes de continuar."
        )

    evaluator = ModelEvaluator()
    test_metrics = evaluator.evaluate(results)
    evaluator.print_report()

    test_metrics.to_csv(
        'data/results/metricas_prueba.csv',
        index=False
    )

    # 7. Generar gráfica
    plotter = ModelPlotter()
    plotter.plot_forecasts(results, model_name)

    print("\nEvaluación independiente finalizada.")

if __name__ == '__main__':
    main()