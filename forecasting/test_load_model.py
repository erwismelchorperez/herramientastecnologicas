from src.models.model_persistence import ModelPersistence

def main():
    persistence = ModelPersistence()

    artifact = persistence.load('capital_vigente_naive.pkl')

    model = artifact['model']
    metadata = artifact['metadata']

    print("\nMODELO RECUPERADO")
    print("-" * 50)
    print(metadata)

    # Generar pronóstico de los próximos 6 meses
    forecast = model.predict(steps=6)

    print("\nPRONÓSTICO DE CAPITAL VIGENTE")
    print(forecast)

if __name__ == '__main__':
    main()