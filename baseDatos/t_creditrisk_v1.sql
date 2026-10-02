
DROP TABLE IF EXISTS credit_risk_prediction_explanation;
DROP TABLE IF EXISTS credit_risk_prediction;

CREATE TABLE credit_risk_prediction (
    id BIGSERIAL PRIMARY KEY,

    edad INTEGER NOT NULL,
    codigo_postal VARCHAR(10) NOT NULL,
    tipovivienda VARCHAR(30) NOT NULL,
    dependientes INTEGER NOT NULL,
    estadocivil VARCHAR(30) NOT NULL,
    genero VARCHAR(10) NOT NULL,
    claveactividad VARCHAR(30) NOT NULL,
    nivelacademico VARCHAR(30) NOT NULL,
    telefono VARCHAR(20) NOT NULL,

    ingreso NUMERIC(14,2) NOT NULL,
    egreso NUMERIC(14,2) NOT NULL,

    tipoprestamo VARCHAR(10) NOT NULL,

    tasainteres NUMERIC(8,4) NOT NULL,
    tasamoratoria NUMERIC(8,4) NOT NULL,

    monto NUMERIC(14,2) NOT NULL,

    num_avales INTEGER NOT NULL,
    creditostrabajados INTEGER NOT NULL,

    bien VARCHAR(100) NOT NULL,
    montogarantia NUMERIC(14,2) NOT NULL,

    finalidad VARCHAR(30) NOT NULL,
    remesas VARCHAR(10) NOT NULL,

    plazo INTEGER NOT NULL,

    prediction VARCHAR(20),
    probability NUMERIC(6,4),

    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',
    model_version VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50)
);

CREATE TABLE credit_risk_prediction_explanation (
    id BIGSERIAL PRIMARY KEY,

    prediction_id BIGINT NOT NULL,

    pattern TEXT,
    explanation TEXT,
    confidence DOUBLE PRECISION,
    support INTEGER,
    score DOUBLE PRECISION,

    CONSTRAINT fk_credit_risk_prediction_explanation
        FOREIGN KEY (prediction_id)
        REFERENCES credit_risk_prediction(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_credit_risk_prediction_created_at
    ON credit_risk_prediction(created_at);

CREATE INDEX idx_credit_risk_prediction_explanation_prediction_id
    ON credit_risk_prediction_explanation(prediction_id);


    SELECT
    tablename,
    tableowner
FROM pg_tables
WHERE tablename IN (
    'credit_risk_prediction',
    'credit_risk_prediction_explanation'
);

GRANT ALL PRIVILEGES ON TABLE credit_risk_prediction TO emelchor;
GRANT ALL PRIVILEGES ON TABLE credit_risk_prediction_explanation TO emelchor;

GRANT ALL PRIVILEGES ON SEQUENCE credit_risk_prediction_id_seq TO emelchor;
GRANT ALL PRIVILEGES ON SEQUENCE credit_risk_prediction_explanation_id_seq TO emelchor;