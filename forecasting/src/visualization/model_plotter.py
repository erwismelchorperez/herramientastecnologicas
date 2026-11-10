from pathlib import Path
import matplotlib.pyplot as plt

class ModelPlotter:
    def __init__(self, output_dir='data/plots'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_metrics(self, metrics):
        if metrics.empty:
            raise ValueError("No existen métricas para graficar.")

        metric_columns = ['MAE', 'RMSE', 'sMAPE', 'WAPE']

        for metric in metric_columns:
            if metric not in metrics.columns:
                continue

            data = metrics.sort_values(metric, ascending=True)
            fig, ax = plt.subplots(figsize=(9, 5))
            bars = ax.bar(data['model'], data[metric])

            ax.set_title(f"Comparación de modelos - {metric}")
            ax.set_xlabel("Modelo")
            ax.set_ylabel(metric)
            ax.grid(axis='y', linestyle='--', alpha=0.4)
            ax.bar_label(bars, fmt='%.3f', padding=3)

            plt.xticks(rotation=15)
            plt.tight_layout()

            filename = self.output_dir / f"comparacion_{metric.lower()}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"Gráfica guardada: {filename}")

    def plot_forecasts(self, results, model_name):
        data = results[results['model'] == model_name].copy()

        if data.empty:
            raise ValueError(f"No hay resultados para el modelo {model_name}.")

        data = data.sort_values('fecha')
        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(
            data['fecha'],
            data['actual'],
            marker='o',
            label='Valor real'
        )

        ax.plot(
            data['fecha'],
            data['forecast'],
            marker='o',
            linestyle='--',
            label='Pronóstico'
        )

        ax.set_title(f"Valores reales vs pronósticos - {model_name}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Valor")
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = self.output_dir / f"pronosticos_{model_name.lower()}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Gráfica guardada: {filename}")