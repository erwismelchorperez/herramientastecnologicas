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

alter table socios add COLUMN escolaridad VARCHAR(20);
alter table socios add COLUMN codigopostal INTEGER;
alter table socios add COLUMN localidad VARCHAR(150);
alter table socios add COLUMN municipio VARCHAR(150);
alter table socios add COLUMN estado VARCHAR(100);

GRANT USAGE ON SCHEMA public TO emelchor;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE public.institucion
TO emelchor;