import pandas as pd

from src.evaluation.model_selector import ModelSelector
from src.visualization.model_plotter import ModelPlotter

def main():
    metrics = pd.read_csv('data/results/metricas_modelos.csv')

    # 1. Selección del modelo
    selector = ModelSelector(metric='WAPE')
    selection = selector.select(metrics)
    selector.print_report()

    # 2. Guardar ranking
    selection['ranking'].to_csv(
        'data/results/ranking_modelos.csv',
        index=False
    )

    # 3. Generar gráficas
    plotter = ModelPlotter()
    plotter.plot_metrics(metrics)

    print("\nProceso finalizado.")
    print(f"Modelo seleccionado: {selection['best_model']}")

if __name__ == '__main__':
    main()