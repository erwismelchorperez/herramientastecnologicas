CREATE TABLE forecast_features(

    id BIGSERIAL PRIMARY KEY,

    fecha_corte DATE UNIQUE,

    cartera_total NUMERIC(18,2),
    capital_vigente NUMERIC(18,2),
    capital_vencido NUMERIC(18,2),
    morosidad NUMERIC(10,4),

    captacion_total NUMERIC(18,2),
    depositos_mes INT,
    retiros_mes INT,

    socios_activos INT,
    capital_social NUMERIC(18,2),

    crecimiento_cartera NUMERIC(10,4),
    crecimiento_captacion NUMERIC(10,4),
    crecimiento_socios NUMERIC(10,4),

    ratio_morosidad NUMERIC(10,4),
    ratio_captacion_cartera NUMERIC(10,4),

    lag_1_cartera NUMERIC(18,2),
    lag_3_cartera NUMERIC(18,2),
    lag_6_cartera NUMERIC(18,2),

    target_cartera_1m NUMERIC(18,2)
);

----- Insert -----
INSERT INTO forecast_features(

fecha_corte,

cartera_total,
capital_vigente,
capital_vencido,
morosidad,

captacion_total,
depositos_mes,
retiros_mes,

socios_activos,
capital_social,

crecimiento_cartera,
crecimiento_captacion,
crecimiento_socios,

ratio_morosidad,
ratio_captacion_cartera,

lag_1_cartera,
lag_3_cartera,
lag_6_cartera,

target_cartera_1m
)

SELECT

fecha_corte,

cartera_total,
capital_vigente,
capital_vencido,
morosidad,

captacion_total,
depositos_mes,
retiros_mes,

socios_activos,
capital_social,

(
cartera_total
-
LAG(cartera_total)
OVER(
ORDER BY fecha_corte
)
)
/

NULLIF(

LAG(cartera_total)
OVER(
ORDER BY fecha_corte
),

0

),

(
captacion_total
-
LAG(captacion_total)
OVER(
ORDER BY fecha_corte
)
)
/

NULLIF(

LAG(captacion_total)
OVER(
ORDER BY fecha_corte
),

0

),

(
socios_activos
-
LAG(socios_activos)
OVER(
ORDER BY fecha_corte
)
)
/

NULLIF(

LAG(socios_activos)
OVER(
ORDER BY fecha_corte
),

0

),

capital_vencido
/
NULLIF(
cartera_total,
0
),

captacion_total
/
NULLIF(
cartera_total,
0
),

LAG(
cartera_total,
1
)
OVER(
ORDER BY fecha_corte
),

LAG(
cartera_total,
3
)
OVER(
ORDER BY fecha_corte
),

LAG(
cartera_total,
6
)
OVER(
ORDER BY fecha_corte
),

LEAD(
cartera_total,
1
)
OVER(
ORDER BY fecha_corte
)

FROM forecast_dataset

ORDER BY fecha_corte;