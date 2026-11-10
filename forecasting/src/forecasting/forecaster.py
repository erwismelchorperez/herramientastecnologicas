from numbers import Integral
from pathlib import Path
import pandas as pd

from src.models.model_persistence import ModelPersistence

class Forecaster:
    def __init__(self, persistence=None):
        self.persistence = persistence or ModelPersistence()
        self.results = None
        self.metadata = None

    def forecast(self, filename, steps=6):
        if (
            isinstance(steps, bool)
            or not isinstance(steps, Integral)
            or steps <= 0
        ):
            raise ValueError("steps debe ser un entero positivo.")

        artifact = self.persistence.load(filename)

        model = artifact['model']
        self.metadata = artifact['metadata']

        required = {'target', 'model_name'}
        missing = required - set(self.metadata)

        if missing:
            raise ValueError(
                f"Faltan metadatos del modelo: {missing}"
            )

        predictions = model.predict(steps=int(steps))

        if predictions.empty:
            raise ValueError("El modelo no generó pronósticos.")

        if predictions.isna().any():
            raise ValueError("El modelo generó pronósticos faltantes.")

        self.results = pd.DataFrame({
            'fecha': predictions.index,
            'forecast': predictions.to_numpy(),
            'target': self.metadata['target'],
            'model': self.metadata['model_name']
        })

        return self.results

    def save(self, filepath):
        if self.results is None:
            raise RuntimeError("Primero debes ejecutar forecast().")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        self.results.to_csv(filepath, index=False)

        print(f"Pronósticos guardados: {filepath}")
        return filepath