CREATE TABLE forecast_model (
    id BIGSERIAL PRIMARY KEY,

    institucion_id BIGINT NOT NULL,

    target VARCHAR(50) NOT NULL,
    algorithm VARCHAR(80) NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,

    artifact_path TEXT NOT NULL,

    training_start_date DATE,
    training_end_date DATE,
    training_observations INTEGER,

    status VARCHAR(20) NOT NULL DEFAULT 'TRAINED',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_forecast_model_institucion
        FOREIGN KEY (institucion_id)
        REFERENCES institucion(id),

    CONSTRAINT uq_forecast_model_version
        UNIQUE (institucion_id, target, version),

    CONSTRAINT uq_forecast_model_id_institucion
        UNIQUE (id, institucion_id),

    CONSTRAINT ck_forecast_model_target
        CHECK (
            target IN (
                'capital_vigente',
                'capital_vencido',
                'cartera_total',
                'morosidad'
            )
        ),

    CONSTRAINT ck_forecast_model_status
        CHECK (
            status IN ('TRAINED', 'ACTIVE', 'INACTIVE')
        ),

    CONSTRAINT ck_forecast_model_version
        CHECK (version > 0),

    CONSTRAINT ck_forecast_model_observations
        CHECK (
            training_observations IS NULL
            OR training_observations > 0
        )
);
CREATE UNIQUE INDEX uq_forecast_model_active
ON forecast_model (institucion_id, target)
WHERE status = 'ACTIVE';
CREATE TABLE forecast_model_metric (
    id BIGSERIAL PRIMARY KEY,

    model_id BIGINT NOT NULL,

    evaluation_stage VARCHAR(20) NOT NULL,
    metric_name VARCHAR(20) NOT NULL,
    metric_value NUMERIC(20,8) NOT NULL,

    fold SMALLINT NOT NULL DEFAULT 0,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_forecast_metric_model
        FOREIGN KEY (model_id)
        REFERENCES forecast_model(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_forecast_model_metric
        UNIQUE (
            model_id,
            evaluation_stage,
            metric_name,
            fold
        ),

    CONSTRAINT ck_forecast_metric_stage
        CHECK (
            evaluation_stage IN ('VALIDATION', 'HOLDOUT')
        ),

    CONSTRAINT ck_forecast_metric_name
        CHECK (
            metric_name IN ('MAE', 'RMSE', 'sMAPE', 'WAPE')
        ),

    CONSTRAINT ck_forecast_metric_fold
        CHECK (fold >= 0)
);

CREATE TABLE forecast_run (
    id BIGSERIAL PRIMARY KEY,

    model_id BIGINT NOT NULL,
    institucion_id BIGINT NOT NULL,

    forecast_origin_date DATE NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    horizon SMALLINT NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_forecast_run_model
        FOREIGN KEY (model_id, institucion_id)
        REFERENCES forecast_model(id, institucion_id),

    CONSTRAINT ck_forecast_run_horizon
        CHECK (horizon > 0),

    CONSTRAINT ck_forecast_run_status
        CHECK (
            status IN ('PENDING', 'COMPLETED', 'FAILED')
        )
);

CREATE TABLE forecast_value (
    id BIGSERIAL PRIMARY KEY,

    forecast_run_id BIGINT NOT NULL,

    forecast_date DATE NOT NULL,
    step SMALLINT NOT NULL,

    predicted_value NUMERIC(20,4) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_forecast_value_run
        FOREIGN KEY (forecast_run_id)
        REFERENCES forecast_run(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_forecast_value_date
        UNIQUE (forecast_run_id, forecast_date),

    CONSTRAINT uq_forecast_value_step
        UNIQUE (forecast_run_id, step),

    CONSTRAINT ck_forecast_value_step
        CHECK (step > 0)
);

CREATE TABLE forecast_comparison (
    id BIGSERIAL PRIMARY KEY,

    forecast_value_id BIGINT NOT NULL,

    actual_value NUMERIC(20,4) NOT NULL,

    error NUMERIC(20,4) NOT NULL,
    absolute_error NUMERIC(20,4) NOT NULL,
    absolute_percentage_error NUMERIC(20,8),

    evaluated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_forecast_comparison_value
        FOREIGN KEY (forecast_value_id)
        REFERENCES forecast_value(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_forecast_comparison_value
        UNIQUE (forecast_value_id),

    CONSTRAINT ck_forecast_comparison_absolute_error
        CHECK (absolute_error >= 0),

    CONSTRAINT ck_forecast_comparison_percentage_error
        CHECK (
            absolute_percentage_error IS NULL
            OR absolute_percentage_error >= 0
        )
);

CREATE INDEX idx_forecast_model_institucion
ON forecast_model (institucion_id);

CREATE INDEX idx_forecast_metric_model
ON forecast_model_metric (model_id);

CREATE INDEX idx_forecast_run_institucion
ON forecast_run (institucion_id);

CREATE INDEX idx_forecast_run_model
ON forecast_run (model_id);

CREATE INDEX idx_forecast_value_run_date
ON forecast_value (forecast_run_id, forecast_date);

CREATE INDEX idx_forecast_comparison_evaluated
ON forecast_comparison (evaluated_at);