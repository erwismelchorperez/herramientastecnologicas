from pathlib import Path
from src.data.data_reader import DataReader
from src.data.data_processor import DataProcessor
from src.data.data_validator import DataValidator
from src.data.data_aggregator import DataAggregator
import pandas as pd

def main():
    # Crear directorio de salida
    output_dir = Path('data/processed')
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Lectura
    reader = DataReader()
    df = reader.read_csv('data/raw/carteradb_waacachi.csv')

    # 2. Procesamiento
    processor = DataProcessor()
    df = processor.process(df)

    # Diagnóstico de cobertura mensual
    print("\nCOBERTURA DE INFORMACIÓN MENSUAL")
    print("-" * 70)

    diagnostico = (
        df.groupby('fecha')
        .agg(
            registros=('sucursal', 'size'),
            sucursales=('sucursal', 'nunique'),
            monto_validos=('monto', 'count'),
            cvigente_validos=('cvigente', 'count'),
            cvencido_validos=('cvencido', 'count')
        )
    )

    fechas = pd.date_range(
        start=df['fecha'].min(),
        end=df['fecha'].max(),
        freq='ME'
    )

    diagnostico = diagnostico.reindex(fechas)
    diagnostico.index.name = 'fecha'

    print(diagnostico.to_string())

    # -------------------------------------------------
    # Auditoría de cobertura por sucursal
    # -------------------------------------------------

    print("\nAUDITORÍA DE COBERTURA POR SUCURSAL")
    print("-" * 70)

    cobertura = (
        df.pivot_table(
            index='fecha',
            columns='sucursal',
            values='monto',
            aggfunc='count'
        )
        .fillna(0)
    )

    print(cobertura.to_string())

    print("\nMESES CON COBERTURA INCOMPLETA")
    print("-" * 70)

    for fecha, row in cobertura.iterrows():
        sucursales_ausentes = row[row == 0].index.tolist()

        if sucursales_ausentes:
            print(
                f"{fecha:%Y-%m}: "
                f"Sin registros para {sucursales_ausentes}"
            )

    # 3. Validación
    validator = DataValidator()
    report = validator.validate(df)
    validator.print_report(report)

    if not report['valid']:
        raise ValueError("Los datos contienen errores. Revisar validación.")

    # 4. Agregación
    aggregator = DataAggregator()
    series = aggregator.aggregate(df)

    # 5. Guardar resultados
    df.to_csv(output_dir / 'cartera_procesada.csv', index=False, encoding='utf-8-sig')

    series['branches'].to_csv(
        output_dir / 'cartera_sucursales.csv',
        index=False,
        encoding='utf-8-sig'
    )

    series['institution'].to_csv(
        output_dir / 'cartera_institucion.csv',
        index=False,
        encoding='utf-8-sig'
    )

    print("\nProcesamiento finalizado.")
    print(f"Registros originales: {len(df)}")
    print(f"Series por sucursal: {len(series['branches'])}")
    print(f"Series institucionales: {len(series['institution'])}")

if __name__ == '__main__':
    main()