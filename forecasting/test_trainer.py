from pathlib import Path
import pandas as pd

from src.models.model_factory import ModelFactory
from src.models.model_trainer import ModelTrainer
from src.evaluation.time_series_validator import TimeSeriesValidator

# 1. Cargar serie institucional
df = pd.read_csv('data/processed/cartera_institucion.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

series = (
    df.set_index('fecha')['cvigente']
    .sort_index()
)

# 2. Configurar componentes
factory = ModelFactory()

validator = TimeSeriesValidator(
    initial_window=24,
    horizon=1,
    step=1,
    test_size=6
)

trainer = ModelTrainer(
    factory=factory,
    validator=validator
)

# 3. Entrenar y evaluar en las divisiones temporales
output = trainer.train(series)

# 4. Mostrar resultados
trainer.print_report()

# 5. Guardar resultados
output_dir = Path('data/results')
output_dir.mkdir(parents=True, exist_ok=True)

output['results'].to_csv(
    output_dir / 'resultados_entrenamiento.csv',
    index=False,
    encoding='utf-8-sig'
)

if not output['failures'].empty:
    output['failures'].to_csv(
        output_dir / 'errores_entrenamiento.csv',
        index=False,
        encoding='utf-8-sig'
    )

print("\nPrimeros resultados:")
print(output['results'].head(10).to_string(index=False))

print("\nProceso finalizado.")