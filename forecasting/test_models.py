from pathlib import Path
import pandas as pd

from src.models.model_factory import ModelFactory
from src.evaluation.time_series_validator import TimeSeriesValidator
from src.models.model_trainer import ModelTrainer
from src.evaluation.model_evaluator import ModelEvaluator
from src.evaluation.model_selector import ModelSelector
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

    # 2. Configurar modelos y validación
    factory = ModelFactory()

    validator = TimeSeriesValidator(
        initial_window=24,
        horizon=1,
        step=1,
        test_size=6
    )

    # 3. Entrenar y evaluar mediante validación temporal
    trainer = ModelTrainer(
        factory=factory,
        validator=validator
    )

    training_results = trainer.train(series)
    trainer.print_report()

    results = training_results['results']
    failures = training_results['failures']

    results.to_csv(
        'data/results/resultados_entrenamiento.csv',
        index=False
    )

    if not failures.empty:
        failures.to_csv(
            'data/results/errores_entrenamiento.csv',
            index=False
        )

    # 4. Calcular métricas
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate(results)
    evaluator.print_report()

    metrics.to_csv(
        'data/results/metricas_modelos.csv',
        index=False
    )

    # 5. Seleccionar modelo
    selector = ModelSelector(metric='WAPE')
    selection = selector.select(metrics)
    selector.print_report()

    selection['ranking'].to_csv(
        'data/results/ranking_modelos.csv',
        index=False
    )

    # 6. Generar gráficas
    plotter = ModelPlotter()

    plotter.plot_metrics(metrics)

    for model_name in metrics['model']:
        plotter.plot_forecasts(results, model_name)

    print("\nCOMPARACIÓN FINALIZADA")
    print(f"Modelo seleccionado: {selection['best_model']}")

if __name__ == '__main__':
    main()