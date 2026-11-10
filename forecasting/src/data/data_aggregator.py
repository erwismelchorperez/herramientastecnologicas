import pandas as pd


class DataAggregator:

    def __init__(self):
        self.value_columns = [
            'monto',
            'cvigente',
            'cvencido'
        ]

    def aggregate_by_branch(self, df):
        """
        Agrupa los registros por fecha y sucursal.
        """

        result = (
            df.groupby(
                ['fecha', 'sucursal'],
                as_index=False
            )[self.value_columns]
            .sum(min_count=1)
        )

        return (
            result.sort_values(['sucursal', 'fecha'])
            .reset_index(drop=True)
        )

    def complete_months(self, df):
        """
        Completa el calendario mensual de todas las sucursales.

        Los meses sin registros se consideran con saldo cero.
        """

        if df.empty:
            return df.copy()

        # Periodo histórico global
        start_date = df['fecha'].min()
        end_date = df['fecha'].max()

        dates = pd.date_range(
            start=start_date,
            end=end_date,
            freq='ME'
        )

        results = []

        for branch, group in df.groupby('sucursal'):

            group = group.sort_values('fecha').copy()

            # Completar calendario mensual
            group = (
                group.set_index('fecha')
                .reindex(dates)
                .rename_axis('fecha')
                .reset_index()
            )

            group['sucursal'] = branch

            # Reemplazar valores faltantes por cero
            group[self.value_columns] = (
                group[self.value_columns].fillna(0)
            )

            results.append(group)

        result = pd.concat(
            results,
            ignore_index=True
        )

        return (
            result.sort_values(['sucursal', 'fecha'])
            .reset_index(drop=True)
        )

    def aggregate_institution(self, branches):
        """
        Calcula los valores institucionales sumando
        los saldos de todas las sucursales.
        """

        result = (
            branches.groupby('fecha')[self.value_columns]
            .sum()
            .reset_index()
        )

        result['sucursal'] = 'TOTAL INSTITUCION'

        return (
            result[
                ['fecha', 'sucursal'] + self.value_columns
            ]
            .sort_values('fecha')
            .reset_index(drop=True)
        )

    def aggregate(self, df):
        """
        Genera las series históricas por sucursal
        y para toda la institución.
        """

        # 1. Agrupar por sucursal
        branches = self.aggregate_by_branch(df)

        # 2. Completar meses y sustituir NaN por cero
        branches = self.complete_months(branches)

        # 3. Calcular el total institucional
        institution = self.aggregate_institution(branches)

        return {
            'branches': branches,
            'institution': institution
        }