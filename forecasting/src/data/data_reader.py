import pandas as pd
from pathlib import Path

class DataReader:
    def __init__(self, encoding='utf-8-sig', separator=','):
        self.encoding = encoding
        self.separator = separator

    def read_csv(self, path):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {path}")

        df = pd.read_csv(
            path,
            sep=self.separator,
            decimal='.',
            encoding=self.encoding
        )

        df.columns = df.columns.str.strip().str.lower()

        # Diagnóstico temporal
        print('\n--- INFORMACIÓN DEL ARCHIVO ---')
        print(f'Archivo: {path.resolve()}')
        print(f'Registros: {len(df)}')
        print(f'Años disponibles: {sorted(df["anio"].unique())}')
        print(f'Último año: {df["anio"].max()}')

        print('\nRegistros del último año:')
        print(df[df['anio'] == df['anio'].max()].groupby('mes').size())

        return df