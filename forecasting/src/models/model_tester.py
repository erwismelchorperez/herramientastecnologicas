import pandas as pd
from src.models.model_factory import ModelFactory
from src.evaluation.time_series_validator import TimeSeriesValidator

class ModelTester:
    def __init__(self, factory=None, validator=None):
        self.factory = factory or ModelFactory()
        self.validator = validator or TimeSeriesValidator()
        self.results = None
        self.failures = None

    def test(self, series, model_name):
        train, test = self.validator.get_test_set(series)

        results = []
        failures = []

        print(f"\nEvaluando modelo: {model_name}")
        print(
            f"Entrenamiento: {train.index[0].date()} "
            f"a {train.index[-1].date()}"
        )
        print(
            f"Periodo de prueba: {test.index[0].date()} "
            f"a {test.index[-1].date()}"
        )

        try:
            model = self.factory.create_model(model_name)
            model.fit(train)

            forecast = model.predict(steps=len(test))

            if len(forecast) != len(test):
                raise ValueError(
                    "El número de pronósticos no coincide "
                    "con el conjunto de prueba."
                )

            if not forecast.index.equals(test.index):
                raise ValueError(
                    "Las fechas pronosticadas no coinciden "
                    "con las fechas del conjunto de prueba."
                )

            for date, actual, predicted in zip(
                test.index,
                test.to_numpy(),
                forecast.to_numpy()
            ):
                results.append({
                    'model': model_name,
                    'fecha': date,
                    'actual': float(actual),
                    'forecast': float(predicted),
                    'error': float(actual - predicted)
                })

        except Exception as e:
            failures.append({
                'model': model_name,
                'error': str(e)
            })

        self.results = pd.DataFrame(results)
        self.failures = pd.DataFrame(failures)

        return {
            'results': self.results,
            'failures': self.failures
        }

    def print_report(self):
        if self.results is None:
            raise RuntimeError("Primero debes ejecutar test().")

        print("\nRESULTADOS DE PRUEBA")
        print("-" * 75)

        if self.results.empty:
            print("No se generaron pronósticos.")
        else:
            print(self.results.to_string(index=False))

        if self.failures is not None and not self.failures.empty:
            print("\nERRORES")
            print(self.failures.to_string(index=False))