from datetime import datetime
import pandas as pd

from src.models.model_factory import ModelFactory
from src.models.model_persistence import ModelPersistence


class FinalModelTrainer:

    def __init__(self, factory=None, persistence=None):

        self.factory = factory or ModelFactory()
        self.persistence = persistence or ModelPersistence()

        self.model = None
        self.metadata = None

    def train(
        self,
        series,
        model_name,
        target,
        metric=None,
        metric_value=None
    ):

        if not isinstance(series, pd.Series) or series.empty:
            raise ValueError(
                "La serie temporal está vacía o no es válida."
            )

        if not target or not isinstance(target, str):
            raise ValueError(
                "El nombre de la variable objetivo no es válido."
            )

        trained_at = datetime.now()

        # Crear y entrenar el modelo
        self.model = self.factory.create_model(model_name)

        self.model.fit(series)

        # Diagnósticos del entrenamiento
        diagnostics = getattr(
            self.model,
            'training_diagnostics_',
            {}
        )

        self.metadata = {
            'model_name': model_name,
            'target': target,

            'metric': metric,
            'metric_value': metric_value,

            'training_start': str(series.index.min().date()),
            'training_end': str(series.index.max().date()),
            'training_observations': len(series),

            'trained_at': trained_at.isoformat(),

            'training_diagnostics': diagnostics
        }

        timestamp = trained_at.strftime('%Y%m%d_%H%M%S')

        filename = (
            f"{target}_{model_name.lower()}_{timestamp}.pkl"
        )

        self.persistence.save(
            model=self.model,
            filename=filename,
            metadata=self.metadata
        )

        return {
            'model': self.model,
            'metadata': self.metadata,
            'filename': filename
        }