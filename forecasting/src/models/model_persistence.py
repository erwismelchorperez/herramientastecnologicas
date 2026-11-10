from pathlib import Path
import pickle

class ModelPersistence:
    def __init__(self, output_dir='data/models'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, model, filename, metadata=None):
        path = self.output_dir / filename

        if path.suffix != '.pkl':
            raise ValueError("El archivo debe tener extensión .pkl.")

        artifact = {
            'model': model,
            'metadata': metadata or {}
        }

        with open(path, 'wb') as file:
            pickle.dump(artifact, file)

        print(f"Modelo guardado: {path}")
        return path

    def load(self, filename):
        path = self.output_dir / filename

        if not path.exists():
            raise FileNotFoundError(f"No existe el modelo: {path}")

        with open(path, 'rb') as file:
            artifact = pickle.load(file)

        if not isinstance(artifact, dict):
            raise ValueError("El archivo no contiene un artefacto válido.")

        if 'model' not in artifact or 'metadata' not in artifact:
            raise ValueError("El artefacto no contiene las claves esperadas.")

        return artifact

    def load_model(self, filename):
        artifact = self.load(filename)
        return artifact['model']

    def list_models(self):
        return sorted(
            self.output_dir.glob('*.pkl'),
            key=lambda path: path.stat().st_mtime,
            reverse=True
        )