from app import db

class Socios(db.Model):

    __tablename__ = 'socios'
    id = db.Column(db.BigInteger,primary_key=True)
    anio = db.Column(db.Integer,nullable=False)
    mes = db.Column(db.String(10),nullable=False)
    numero_socio = db.Column(db.String(20),nullable=False)
    capital_social = db.Column(db.Numeric(14,2),nullable=True)
    fecha_ingreso = db.Column(db.Date,nullable=False)
    fecha_baja = db.Column(db.Date,nullable=False)
    sexo = db.Column(db.String(10),nullable=False)
    sucursal = db.Column(db.String(100),nullable=False)
    fecha_nacimiento = db.Column(db.Date,nullable=False)