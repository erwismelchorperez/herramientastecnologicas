import pandas as pd

class DataValidator:
    def __init__(self):
        self.required_columns = [
            'anio', 'mes', 'sucursal',
            'monto', 'cvigente', 'cvencido',
            'fecha'
        ]

        self.numeric_columns = [
            'monto', 'cvigente', 'cvencido'
        ]

    def validate(self, df):
        errors = []
        warnings = []

        # Verificar columnas
        missing = set(self.required_columns) - set(df.columns)

        if missing:
            errors.append(f"Columnas faltantes: {missing}")
            return {'valid': False, 'errors': errors, 'warnings': warnings}

        # Verificar valores nulos
        nulls = df[self.required_columns].isnull().sum()
        nulls = nulls[nulls > 0]

        if not nulls.empty:
            errors.append(f"Valores nulos:\n{nulls}")

        # Verificar tipos numéricos
        for column in self.numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[column]):
                errors.append(f"La columna {column} no es numérica")

        # Verificar importes negativos
        for column in self.numeric_columns:
            if (df[column].dropna() < 0).any():
                warnings.append(f"Existen valores negativos en {column}")

        # Verificar duplicados por sucursal y fecha
        duplicated = df.duplicated(
            subset=['sucursal', 'fecha'],
            keep=False
        )

        if duplicated.any():
            warnings.append(
                f"Existen {duplicated.sum()} registros duplicados "
                "por sucursal y fecha"
            )

        # Verificar fechas
        if not pd.api.types.is_datetime64_any_dtype(df['fecha']):
            errors.append("La columna fecha no es de tipo datetime")

        report = {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'total_records': len(df)
        }

        return report

    def print_report(self, report):
        print("\n========== VALIDACIÓN DE DATOS ==========")
        print(f"Registros: {report['total_records']}")
        print(f"Estado: {'CORRECTO' if report['valid'] else 'ERROR'}")

        for error in report['errors']:
            print(f"[ERROR] {error}")

        for warning in report['warnings']:
            print(f"[ADVERTENCIA] {warning}")

        if not report['errors'] and not report['warnings']:
            print("No se encontraron problemas.")

        print("=========================================\n")