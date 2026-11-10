import pandas as pd

from src.evaluation.model_selector import ModelSelector
from src.models.final_model_trainer import FinalModelTrainer

def main():
    # 1. Cargar datos históricos
    df = pd.read_csv('data/processed/cartera_institucion.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])

    series = (
        df.set_index('fecha')['cvigente']
        .sort_index()
        .astype(float)
    )

    # 2. Recuperar modelo seleccionado durante la validación
    metrics = pd.read_csv('data/results/metricas_modelos.csv')

    selector = ModelSelector(metric='WAPE')
    selection = selector.select(metrics)

    model_name = selection['best_model']
    ranking = selection['ranking']

    metric_column = selector.metric_columns[selector.metric]
    metric_value = float(
        ranking.loc[ranking['model'] == model_name, metric_column].iloc[0]
    )

    print(f"\nModelo seleccionado: {model_name}")
    print(f"WAPE de validación: {metric_value:.4f}%")

    # 3. Entrenar modelo definitivo
    trainer = FinalModelTrainer()

    result = trainer.train(
        series=series,
        model_name=model_name,
        target='capital_vigente',
        metric='WAPE',
        metric_value=metric_value
    )

    print("\nMODELO DEFINITIVO")
    print("-" * 50)

    for key, value in result['metadata'].items():
        print(f"{key}: {value}")

    print(f"\nArchivo generado: {result['filename']}")

if __name__ == '__main__':
    main()