from pathlib import Path
import pandas as pd

from src.evaluation.model_evaluator import ModelEvaluator

# 1. Cargar resultados del entrenamiento
results = pd.read_csv(
    'data/results/resultados_entrenamiento.csv'
)

# 2. Evaluar modelos
evaluator = ModelEvaluator()
metrics = evaluator.evaluate(results)

# 3. Mostrar comparación
evaluator.print_report()

# 4. Guardar métricas
output_dir = Path('data/results')
output_dir.mkdir(parents=True, exist_ok=True)

metrics.to_csv(
    output_dir / 'metricas_modelos.csv',
    index=False,
    encoding='utf-8-sig'
)

print("\nEvaluación finalizada.")