CREATE TABLE credit_risk_prediction (

    id                  BIGSERIAL PRIMARY KEY,

    reports             INTEGER         NOT NULL,
    age                 NUMERIC(8,4)    NOT NULL,
    income              NUMERIC(12,4)   NOT NULL,
    share               NUMERIC(12,8)   NOT NULL,
    expenditure         NUMERIC(14,2)   NOT NULL DEFAULT 0,

    owner               BOOLEAN         NOT NULL,
    selfemp             BOOLEAN         NOT NULL,

    dependents          INTEGER         NOT NULL,
    months              INTEGER         NOT NULL,
    majorcards          INTEGER         NOT NULL,
    active              INTEGER         NOT NULL,

    prediction          VARCHAR(20),
    probability         NUMERIC(6,4),

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by          VARCHAR(50)
);

CREATE TABLE credit_risk_prediction_explanation(

    id BIGSERIAL PRIMARY KEY,

    prediction_id BIGINT NOT NULL,

    pattern TEXT,

    explanation TEXT,

    confidence NUMERIC(8,4),

    support INTEGER,

    score NUMERIC(10,4),

    FOREIGN KEY(prediction_id)
        REFERENCES credit_risk_prediction(id)

);