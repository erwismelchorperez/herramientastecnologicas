CREATE TABLE forecast_prediction(

    id BIGSERIAL PRIMARY KEY,

    modelo VARCHAR(100) NOT NULL,

    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    fecha_base DATE NOT NULL,

    fecha_prediccion DATE NOT NULL,

    horizonte_meses INT DEFAULT 1,

    cartera_real NUMERIC(18,2),

    cartera_predicha NUMERIC(18,2) NOT NULL,

    error_absoluto NUMERIC(18,2),

    error_porcentual NUMERIC(10,4),

    estado VARCHAR(20) DEFAULT 'PENDIENTE',

    UNIQUE(
        modelo,
        fecha_prediccion
    )
);

ALTER TABLE forecast_prediction ADD COLUMN crecimiento_esperado NUMERIC(10,4);
ALTER TABLE forecast_prediction ADD COLUMN mae NUMERIC(18,4);
ALTER TABLE forecast_prediction ADD COLUMN rmse NUMERIC(18,4);
ALTER TABLE forecast_prediction ADD COLUMN mape NUMERIC(18,4);
ALTER TABLE forecast_prediction ADD COLUMN r2 NUMERIC(10,4);