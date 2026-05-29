CREATE TABLE forecast_model_metrics(
    id BIGSERIAL PRIMARY KEY,
    modelo VARCHAR(100),
    train_inicio DATE,
    train_fin DATE,
    test_inicio DATE,
    test_fin DATE,
    mae NUMERIC(18,4),
    rmse NUMERIC(18,4),
    mape NUMERIC(18,4),
    r2 NUMERIC(18,4),
    created_at TIMESTAMP DEFAULT NOW()
);