drop table instituciones;
CREATE TABLE institucion (
    id BIGSERIAL PRIMARY KEY,
    nameshort VARCHAR(50) NOT NULL,
    namelarge VARCHAR(255) NOT NULL,
    direction VARCHAR(255),
    tipo VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
select * from institucion;
insert into institucion(nameshort, namelarge, direction, tipo) values('Waa Cachi', 'Waa Cachi S.F.C., S.A. de C.V.','Colonia Vicente Guerrero, Municipio de Xochistlahuaca, Estado de Guerrero, C.P. 41770.','SOFINCO');