import pandas as pd
from src.models.model_factory import ModelFactory
from src.evaluation.time_series_validator import TimeSeriesValidator

# 1. Cargar serie institucional
df = pd.read_csv('data/processed/cartera_institucion.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

series = (
    df.set_index('fecha')['cvigente']
    .sort_index()
)

# 2. Crear fábrica de modelos
factory = ModelFactory()

print("Modelos disponibles:")
for name in factory.get_available_models():
    print(f"- {name}")

# 3. Generar divisiones temporales
validator = TimeSeriesValidator(
    initial_window=24,
    horizon=1,
    step=1,
    test_size=6
)

splits = validator.split(series)
validator.print_splits(splits)

# 4. Consultar conjunto de prueba
train, test = validator.get_test_set(series)

print("\nConjunto de prueba final:")
print(f"Entrenamiento: {train.index[0].date()} a {train.index[-1].date()}")
print(f"Prueba: {test.index[0].date()} a {test.index[-1].date()}")
print(f"Observaciones de prueba: {len(test)}")

# 5. Comprobar creación de modelos
models = factory.get_models()

print("\nInstancias creadas:")
for model in models:
    print(model.name)