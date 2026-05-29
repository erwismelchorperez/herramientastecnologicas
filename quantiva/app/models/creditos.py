from app import db

class Credito(db.Model):

    __tablename__ = 'creditos'
    id = db.Column(db.BigInteger,primary_key=True)
    anio = db.Column(db.Integer,nullable=False)
    mes = db.Column(db.String(10),nullable=False)
    capital_vigente = db.Column(db.Numeric(14,2),nullable=True)
    capital_vencido = db.Column(db.Numeric(14,2),nullable=True)
    producto_credito = db.Column(db.String(100),nullable=False)
    clasificacion_credito = db.Column(db.String(100),nullable=False)
    sucursal = db.Column(db.String(100),nullable=False)
    numero_credito = db.Column(db.String(100),nullable=False)
    vigente_vencido = db.Column(db.String(20),nullable=False)
    renovado_reestructurado_normal = db.Column(db.String(20),nullable=False)
    monto_original = db.Column(db.Numeric(14,2),nullable=True)