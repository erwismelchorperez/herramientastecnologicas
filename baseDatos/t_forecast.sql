CREATE TABLE forecast_dataset(

    id BIGSERIAL PRIMARY KEY,

    anio INT NOT NULL,

    mes VARCHAR(3) NOT NULL,

    fecha_corte DATE NOT NULL,

    cartera_total NUMERIC(18,2),
    capital_vigente NUMERIC(18,2),
    capital_vencido NUMERIC(18,2),
    morosidad NUMERIC(10,4),

    creditos_vigentes INT,
    creditos_vencidos INT,
    reestructurados INT,
    credito_promedio NUMERIC(18,2),

    captacion_total NUMERIC(18,2),
    depositos_mes INT,
    retiros_mes INT,
    saldo_promedio NUMERIC(18,2),

    socios_activos INT,
    socios_altas INT,
    socios_bajas INT,
    capital_social NUMERIC(18,2),

    edad_promedio NUMERIC(10,2),
    antiguedad_promedio NUMERIC(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_forecast_dataset
    UNIQUE(
        anio,
        mes
    )
);



----- Insert a tabla -----
INSERT INTO forecast_dataset(

    anio,
    mes,
    fecha_corte,

    cartera_total,
    capital_vigente,
    capital_vencido,
    morosidad,

    creditos_vigentes,
    creditos_vencidos,
    reestructurados,
    credito_promedio,

    captacion_total,
    depositos_mes,
    retiros_mes,
    saldo_promedio,

    socios_activos,
    socios_altas,
    socios_bajas,
    capital_social,

    edad_promedio,
    antiguedad_promedio
)

WITH cartera AS(

SELECT

anio,
mes,

SUM(capital_vigente+capital_vencido) cartera_total,

SUM(capital_vigente) capital_vigente,

SUM(capital_vencido) capital_vencido,

CASE
WHEN SUM(capital_vigente+capital_vencido)>0
THEN
SUM(capital_vencido)
/
SUM(capital_vigente+capital_vencido)
*100
ELSE 0
END morosidad,

COUNT(
CASE
WHEN vigente_vencido='VIGENTE'
THEN 1
END
) creditos_vigentes,

COUNT(
CASE
WHEN vigente_vencido='VENCIDO'
THEN 1
END
) creditos_vencidos,

COUNT(
CASE
WHEN renovado_reestructurado_normal=
'RE-ESTRUCTURADO X CONTINGENCIA'
THEN 1
END
) reestructurados,

AVG(
monto_original
) credito_promedio

FROM creditos

GROUP BY
anio,
mes

),

captacion_data AS(

SELECT

anio,
mes,

SUM(
saldo_total_cierre_mes
) captacion_total,

COUNT(
fecha_deposito_ultimo
) depositos_mes,

COUNT(
fecha_retiro_ultimo
) retiros_mes,

AVG(
saldo_promedio
) saldo_promedio

FROM captacion

GROUP BY
anio,
mes

),

socios_data AS(

SELECT

anio,
mes,

COUNT(
CASE
WHEN fecha_baja IS NULL
THEN 1
END
) socios_activos,

COUNT(
CASE
WHEN EXTRACT(
MONTH
FROM fecha_ingreso
)=CASE mes
WHEN 'ene' THEN 1
WHEN 'feb' THEN 2
WHEN 'mar' THEN 3
WHEN 'abr' THEN 4
WHEN 'may' THEN 5
WHEN 'jun' THEN 6
WHEN 'jul' THEN 7
WHEN 'ago' THEN 8
WHEN 'sep' THEN 9
WHEN 'oct' THEN 10
WHEN 'nov' THEN 11
WHEN 'dic' THEN 12
END
THEN 1
END
) socios_altas,

COUNT(
CASE
WHEN fecha_baja IS NOT NULL
THEN 1
END
) socios_bajas,

SUM(
capital_social
) capital_social,

AVG(
EXTRACT(
YEAR
FROM AGE(
CURRENT_DATE,
fecha_nacimiento
)
)
) edad_promedio,

AVG(
EXTRACT(
YEAR
FROM AGE(
CURRENT_DATE,
fecha_ingreso
)
)
) antiguedad_promedio

FROM socios

GROUP BY
anio,
mes

)

SELECT

c.anio,

c.mes,

make_date(

c.anio,

CASE c.mes
WHEN 'ene' THEN 1
WHEN 'feb' THEN 2
WHEN 'mar' THEN 3
WHEN 'abr' THEN 4
WHEN 'may' THEN 5
WHEN 'jun' THEN 6
WHEN 'jul' THEN 7
WHEN 'ago' THEN 8
WHEN 'sep' THEN 9
WHEN 'oct' THEN 10
WHEN 'nov' THEN 11
WHEN 'dic' THEN 12
END,

1

),

c.cartera_total,
c.capital_vigente,
c.capital_vencido,
c.morosidad,

c.creditos_vigentes,
c.creditos_vencidos,
c.reestructurados,
c.credito_promedio,

cp.captacion_total,
cp.depositos_mes,
cp.retiros_mes,
cp.saldo_promedio,

s.socios_activos,
s.socios_altas,
s.socios_bajas,
s.capital_social,

s.edad_promedio,
s.antiguedad_promedio

FROM cartera c

LEFT JOIN captacion_data cp
ON c.anio=cp.anio
AND c.mes=cp.mes

LEFT JOIN socios_data s
ON c.anio=s.anio
AND c.mes=s.mes

ON CONFLICT(
anio,
mes
)

DO NOTHING;

---- Update ----
UPDATE forecast_dataset
SET fecha_corte=

CASE mes

WHEN 'ene'
THEN make_date(anio,1,1)+interval '1 month'-interval '1 day'

WHEN 'feb'
THEN make_date(anio,2,1)+interval '1 month'-interval '1 day'

WHEN 'mar'
THEN make_date(anio,3,1)+interval '1 month'-interval '1 day'

WHEN 'abr'
THEN make_date(anio,4,1)+interval '1 month'-interval '1 day'

WHEN 'may'
THEN make_date(anio,5,1)+interval '1 month'-interval '1 day'

WHEN 'jun'
THEN make_date(anio,6,1)+interval '1 month'-interval '1 day'

WHEN 'jul'
THEN make_date(anio,7,1)+interval '1 month'-interval '1 day'

WHEN 'ago'
THEN make_date(anio,8,1)+interval '1 month'-interval '1 day'

WHEN 'sep'
THEN make_date(anio,9,1)+interval '1 month'-interval '1 day'

WHEN 'oct'
THEN make_date(anio,10,1)+interval '1 month'-interval '1 day'

WHEN 'nov'
THEN make_date(anio,11,1)+interval '1 month'-interval '1 day'

WHEN 'dic'
THEN make_date(anio,12,1)+interval '1 month'-interval '1 day'

END;