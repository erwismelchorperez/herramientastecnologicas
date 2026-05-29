DROP TABLE IF EXISTS creditos;
CREATE TABLE creditos (
    -- 1. Identificación del acreditado y crédito
    nombre_acreditado VARCHAR(255) NOT NULL,                     -- "Nombre del Acreditado"
    numero_socio_cliente VARCHAR(100),                           -- "Número de Socio y/o Cliente"
    numero_credito VARCHAR(100),                 -- "Número de Crédito"
    sucursal VARCHAR(100),                                       -- "Sucursal"
    
    -- 2. Clasificación y características del crédito
    clasificacion_credito VARCHAR(50),                           -- "Clasificacion de Crédito"
    producto_credito VARCHAR(100),                               -- "Producto de Crédito"
    tipo_cuota VARCHAR(100),                                      -- "Tipo de Cuota"
    
    -- 3. Fechas y montos originales
    fecha_otorgamiento DATE NOT NULL,                            -- "Fecha de Otorgamiento"
    monto_original NUMERIC(18, 2) NOT NULL CHECK (monto_original >= 0), -- "Monto Original"
    fecha_vencimiento DATE NOT NULL,                             -- "Fecha de Vencimiento"
    
    -- 4. Tasas de interés
    tasa_ord_nom_anual NUMERIC(10, 4) NOT NULL,                  -- "Tasa Ord. Nom. Anual"
    tasa_moratoria_nom_anual NUMERIC(10, 4) DEFAULT 0,           -- "Tasa Moratoria Nominal Anual %"
    
    -- 5. Plazo y frecuencias de pago
    plazo_credito VARCHAR(50) NOT NULL,                              -- "Plazo del Credito"
    frecuencia_pago_capital VARCHAR(50),                         -- "Frecuencia de Pago Capital"
    frecuencia_pago_intereses VARCHAR(50),                       -- "Frecuencia de Pago Intereses"
    
    -- 6. Situación de mora y saldos
    dias_mora_cartera INTEGER DEFAULT 0,                         -- "Dias de Mora Cartera"
    capital_vigente NUMERIC(18, 2) DEFAULT 0 CHECK (capital_vigente >= 0),   -- "Capital Vigente"
    capital_vencido NUMERIC(18, 2) DEFAULT 0 CHECK (capital_vencido >= 0),    -- "Capital Vencido"
    
    -- 7. Intereses devengados no cobrados
    intereses_moratorios_devengados_no_cobrados NUMERIC(18, 2) DEFAULT 0,     -- "Intereses Moratorios Devengados No Cobrados"
    intereses_ordinarios_devengados_no_cobrados_vigente NUMERIC(18, 2) DEFAULT 0, -- "Intereses Ordinarios Devengados No Cobrados Vigente"
    intereses_devengados_no_cobrados_vencido NUMERIC(18, 2) DEFAULT 0,        -- "Intereses Devengados No Cobrados Vencido"
    intereses_devengados_no_cobrados_cuentas_orden NUMERIC(18, 2) DEFAULT 0,  -- "Intereses Devengados No Cobrados Cuentas de Orden"
    
    -- 8. Últimos pagos realizados
    fecha_ultimo_pago_capital DATE,                             -- "Fecha de Ultimo Pago de Capital"
    monto_ultimo_pago_capital NUMERIC(18, 2) DEFAULT 0,         -- "Monto Ultimo Pago de Capital"
    fecha_ultimo_pago_interes DATE,                             -- "Fecha de Ultimo Pago de Interes"
    monto_ultimo_pago_interes NUMERIC(18, 2) DEFAULT 0,         -- "Monto Ultimo Pago de Interes"
    
    -- 9. Estatus del crédito
    renovado_reestructurado_normal VARCHAR(50),                 -- "Renovado, reestructurado ó normal"
    emproblemado BOOLEAN DEFAULT FALSE,                         -- "Emproblemado"
    vigente_vencido VARCHAR(20),                                -- "Vigente ó vencido"
    
    -- 10. Parte relacionada (art. 26 LRASCAP)
    cargo_parte_relacionada BOOLEAN DEFAULT FALSE,              -- "CARGO DEL ACREDITADO PARTE RELACIONADA art. 26 LRASCAP"
    
    -- 11. Garantías
    monto_garantia_liquida NUMERIC(18, 2) DEFAULT 0,            -- "Monto Garantia Liquida"
    cuentas_garantia_liquida VARCHAR(50),                            -- "CUENTA(S) SOBRE LA(S) QUE SE CONSITUYO GARANTIA LIQUIDA"
    monto_garantia_prendaria NUMERIC(18, 2) DEFAULT 0,          -- "MONTO GARANTIA PRENDARIA"
    monto_garantia_hipotecaria NUMERIC(18, 2) DEFAULT 0,        -- "MONTO GARANTIA HIPOTECARIA"
    
    -- 12. Estimaciones Preventivas para Riesgos Crediticios (EPRC)
    eprc_para_parte_cubierta NUMERIC(18, 2) DEFAULT 0,          -- "EPRC PARA PARTE CUBIERTA"
    eprc_para_parte_expuesta NUMERIC(18, 2) DEFAULT 0,          -- "EPRC PARA PARTE EXPUESTA"
    eprc_intereses_cave NUMERIC(18, 2) DEFAULT 0,               -- "EPRC X INTERESES DE CaVe"
    
    -- 13. Dimensiones temporales para reportes
    anio INTEGER NOT NULL,                                      -- "anio"
    mes VARCHAR(3),         -- "mes"

    -- 15. Auditoría
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);