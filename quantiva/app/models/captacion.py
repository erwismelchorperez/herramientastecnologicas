from app import db

class Captacion(db.Model):

    __tablename__ = 'captacion'
    id = db.Column(db.BigInteger,primary_key=True)
    anio = db.Column(db.Integer,nullable=False)
    mes = db.Column(db.String(10),nullable=False)
    numero_socio = db.Column(db.String(20),nullable=False)
    saldo_total_cierre_mes = db.Column(db.Numeric(14,2),nullable=True)
    fecha_apertura_contratacion = db.Column(db.Date,nullable=False)
    fecha_retiro_ultimo = db.Column(db.Date,nullable=False)
    fecha_deposito_ultimo = db.Column(db.Date,nullable=False)
    tipo_deposito_cuenta_producto = db.Column(db.String(100),nullable=False)
    sucursal = db.Column(db.String(100),nullable=False)
    no_socio_padre_tutor = db.Column(db.String(100),nullable=False)