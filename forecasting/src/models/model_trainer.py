import pandas as pd
from src.models.model_factory import ModelFactory
from src.evaluation.time_series_validator import TimeSeriesValidator

class ModelTrainer:
    def __init__(self, factory=None, validator=None):
        self.factory = factory or ModelFactory()
        self.validator = validator or TimeSeriesValidator()
        self.results = None
        self.failures = None

    def train(self, series, model_names=None):
        splits = self.validator.split(series)

        if model_names is None:
            model_names = self.factory.get_available_models()

        results = []
        failures = []

        for model_name in model_names:
            print(f"\nEvaluando modelo: {model_name}")

            for split in splits:
                try:
                    model = self.factory.create_model(model_name)

                    train = split['train']
                    validation = split['validation']

                    model.fit(train)
                    forecast = model.predict(steps=len(validation))

                    if len(forecast) != len(validation):
                        raise ValueError(
                            "El número de pronósticos no coincide "
                            "con el horizonte de validación."
                        )

                    for date, actual, predicted in zip(
                        validation.index,
                        validation.to_numpy(),
                        forecast.to_numpy()
                    ):
                        results.append({
                            'model': model_name,
                            'fold': split['fold'],
                            'fecha': date,
                            'actual': actual,
                            'forecast': predicted,
                            'error': actual - predicted
                        })

                except Exception as e:
                    failures.append({
                        'model': model_name,
                        'fold': split['fold'],
                        'error': str(e)
                    })

            print(f"Divisiones procesadas: {len(splits)}")

        self.results = pd.DataFrame(results)
        self.failures = pd.DataFrame(failures)

        return {
            'results': self.results,
            'failures': self.failures
        }

    def print_report(self):
        if self.results is None:
            raise RuntimeError("Primero debes ejecutar train().")

        print("\nRESULTADOS DEL ENTRENAMIENTO")
        print("-" * 45)

        if self.results.empty:
            print("No se generaron resultados.")
        else:
            summary = (
                self.results.groupby('model')
                .agg(
                    observaciones=('actual', 'count'),
                    error_medio=('error', 'mean'),
                    error_absoluto_medio=('error', lambda x: x.abs().mean())
                )
                .reset_index()
            )

            print(summary.to_string(index=False))

        if self.failures is not None and not self.failures.empty:
            print("\nMODELOS CON ERRORES")
            print(self.failures.to_string(index=False))