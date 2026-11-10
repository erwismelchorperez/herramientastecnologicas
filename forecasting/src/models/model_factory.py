from src.models.naive import NaiveModel
from src.models.seasonal_naive import SeasonalNaiveModel
from src.models.exponential_smoothing import ExponentialSmoothingModel
from src.models.linear_regression import LinearRegressionModel
from src.models.random_forest import RandomForestModel

class ModelFactory:
    def __init__(self, seasonal_periods=12):
        self.seasonal_periods = seasonal_periods

        self.available_models = {
            'naive': NaiveModel,
            'seasonal_naive': lambda: SeasonalNaiveModel(
                seasonal_periods=self.seasonal_periods
            ),
            'ses': lambda: ExponentialSmoothingModel(),
            'holt': lambda: ExponentialSmoothingModel(
                trend='add'
            ),
            'holt_damped': lambda: ExponentialSmoothingModel(
                trend='add',
                damped_trend=True
            ),
            'holt_winters_add': lambda: ExponentialSmoothingModel(
                trend='add',
                seasonal='add',
                seasonal_periods=self.seasonal_periods
            ),
            'holt_winters_mul': lambda: ExponentialSmoothingModel(
                trend='add',
                seasonal='mul',
                seasonal_periods=self.seasonal_periods
            ),
            'linear_regression': LinearRegressionModel,
            'random_forest': RandomForestModel
        }

    def create_model(self, model_name):
        model_name = model_name.lower()

        if model_name not in self.available_models:
            raise ValueError(f"Modelo no disponible: {model_name}")

        return self.available_models[model_name]()

    def get_models(self, model_names=None):
        if model_names is None:
            model_names = self.get_available_models()

        return [
            self.create_model(name)
            for name in model_names
        ]

    def get_available_models(self):
        return list(self.available_models.keys())