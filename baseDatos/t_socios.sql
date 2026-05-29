CREATE TABLE socios (
    id BIGSERIAL PRIMARY KEY,
    sucursal VARCHAR(100),
    numero_socio VARCHAR(50) NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    sexo VARCHAR(10),
    fecha_nacimiento DATE,
    curp VARCHAR(20),
    ife VARCHAR(50), -- Puede ser credencial de elector o identificación oficial
    estado_civil VARCHAR(20),
    fecha_ingreso DATE,
    fecha_baja DATE,
    capital_social DECIMAL(12,2),
    anio INT,
    mes VARCHAR(3)
);
