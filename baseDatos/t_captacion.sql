-- =====================================================
-- TABLA: captacion
-- Gestión de captación (depósitos, cuentas de ahorro, inversiones)
-- Columnas ordenadas según archivo Excel origen
-- =====================================================

DROP TABLE IF EXISTS captacion;
CREATE TABLE captacion (
    id BIGSERIAL PRIMARY KEY,
    numero_socio VARCHAR(100) NOT NULL,                              -- 1. Numero de socio
    nombre_socio VARCHAR(255) NOT NULL,                              -- 2. Nombre del socio
    num_contrato_cuenta VARCHAR(100) UNIQUE NOT NULL,                -- 3. Núm. Contrato o Cuenta
    sucursal VARCHAR(100),                                           -- 4. Sucursal
    fecha_apertura_contratacion DATE NOT NULL,                       -- 5. Fecha de apertura o contratación
    tipo_deposito_cuenta_producto VARCHAR(100),                      -- 6. Tipo de deposito (cuenta o producto)
    fecha_retiro_ultimo DATE,                                        -- 7. Fecha del retiro (ultimo)
    fecha_deposito_ultimo DATE,                                      -- 8. Fecha del deposito (ultimo)
    fecha_vencimiento varchar(20),                                          -- 9. Fecha de vencimiento
    plazo_deposito_dias INTEGER DEFAULT 0,                           -- 10. Plazo del deposito (días)
    forma_pago_rendimientos_dias INTEGER,                            -- 11. Forma de pago de rendimientos (días)
    tasa_interes_nominal_pactada_anual NUMERIC(10, 4) DEFAULT 0,     -- 12. Tasa de interés nominal pactada (anual)
    saldo_promedio NUMERIC(18, 2) DEFAULT 0,                         -- 13. Saldo Promedio (para determinar intereses mens)
    monto_ahorro_deposito_plazo_capital NUMERIC(18, 2) DEFAULT 0,    -- 14. Monto del Ahorro o Depósito Plazo (capital)
    intereses_devengados_no_pagados_cierre_mes NUMERIC(18, 2) DEFAULT 0, -- 15. Intereses Devengados No Pagados al Cierre del mes Dep a Plazo
    saldo_total_cierre_mes NUMERIC(18, 2) DEFAULT 0,                 -- 16. Saldo Total al cierre del mes
    intereses_generados_mes NUMERIC(18, 2) DEFAULT 0,                -- 17. Intereses Generados en el mes
    promotor VARCHAR(150),                                           -- 18. Promotor
    no_socio_padre_tutor VARCHAR(100),                               -- 19. No. Socio del Padre ó Tutor
    anio INTEGER NOT NULL,                                           -- 20. anio
    mes VARCHAR(3)
);
