import pandas as pd
import numpy as np

class DataProcessor:
    MONTHS = {
        'ene': 1, 'enero': 1,
        'feb': 2, 'febrero': 2,
        'mar': 3, 'marzo': 3,
        'abr': 4, 'abril': 4,
        'may': 5, 'mayo': 5,
        'jun': 6, 'junio': 6,
        'jul': 7, 'julio': 7,
        'ago': 8, 'agosto': 8,
        'sep': 9, 'sept': 9, 'septiembre': 9,
        'oct': 10, 'octubre': 10,
        'nov': 11, 'noviembre': 11,
        'dic': 12, 'diciembre': 12
    }

    def __init__(self):
        self.required_columns = [
            'anio', 'mes', 'sucursal',
            'monto', 'cvigente', 'cvencido'
        ]

    def process(self, df):
        df = df.copy()

        # Validar columnas
        missing = set(self.required_columns) - set(df.columns)

        if missing:
            raise ValueError(f"Faltan columnas: {missing}")

        # Normalizar información
        df['anio'] = pd.to_numeric(df['anio'], errors='raise').astype(int)
        df['mes'] = df['mes'].astype(str).str.strip().str.lower()
        df['sucursal'] = df['sucursal'].astype(str).str.strip()

        # Convertir meses
        df['mes_num'] = df['mes'].map(self.MONTHS)

        if df['mes_num'].isna().any():
            invalid = df.loc[df['mes_num'].isna(), 'mes'].unique()
            raise ValueError(f"Meses no reconocidos: {invalid}")

        df['mes_num'] = df['mes_num'].astype(int)

        # Convertir importes
        for column in ['monto', 'cvigente', 'cvencido']:
            df[column] = pd.to_numeric(df[column], errors='raise')

        # Crear fecha al cierre del mes
        df['fecha'] = (
            pd.to_datetime(
                dict(year=df['anio'], month=df['mes_num'], day=1)
            ) + pd.offsets.MonthEnd(0)
        )

        # Indicadores derivados
        df['cartera_total'] = df['cvigente'] + df['cvencido']

        df['morosidad'] = np.where(
            df['cartera_total'] > 0,
            (df['cvencido'] / df['cartera_total']) * 100,
            np.nan
        )

        # Ordenar información
        df = df.sort_values(
            ['sucursal', 'fecha']
        ).reset_index(drop=True)

        return df