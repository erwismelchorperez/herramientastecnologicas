from app import db
from sqlalchemy.sql import func

class CreditRiskPrediction(db.Model):

    __tablename__ = "credit_risk_prediction"

    id = db.Column(db.BigInteger, primary_key=True)

    edad = db.Column(db.Integer, nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    tipovivienda = db.Column(db.String(30), nullable=False)
    dependientes = db.Column(db.Integer, nullable=False)
    estadocivil = db.Column(db.String(30), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    claveactividad = db.Column(db.String(30), nullable=False)
    nivelacademico = db.Column(db.String(30), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    ingreso = db.Column(db.Numeric(14, 2), nullable=False)
    egreso = db.Column(db.Numeric(14, 2), nullable=False)

    tipoprestamo = db.Column(db.String(10), nullable=False)

    tasainteres = db.Column(db.Numeric(8, 4), nullable=False)
    tasamoratoria = db.Column(db.Numeric(8, 4), nullable=False)

    monto = db.Column(db.Numeric(14, 2), nullable=False)

    num_avales = db.Column(db.Integer, nullable=False)
    creditostrabajados = db.Column(db.Integer, nullable=False)

    bien = db.Column(db.String(100), nullable=False)
    montogarantia = db.Column(db.Numeric(14, 2), nullable=False)

    finalidad = db.Column(db.String(30), nullable=False)
    remesas = db.Column(db.String(10), nullable=False)

    plazo = db.Column(db.Integer, nullable=False)

    prediction = db.Column(db.String(20), nullable=True)
    probability = db.Column(db.Numeric(6, 4), nullable=True)

    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    created_by = db.Column(db.String(50), nullable=True)


class CreditRiskPredictionExplanation(db.Model):

    __tablename__ = "credit_risk_prediction_explanation"

    id = db.Column(db.BigInteger, primary_key=True)

    prediction_id = db.Column(db.BigInteger,db.ForeignKey("credit_risk_prediction.id"),nullable=False)
    pattern = db.Column(db.Text)
    explanation = db.Column(db.Text)
    confidence = db.Column(db.Float)
    support = db.Column(db.Integer)
    score = db.Column(db.Float)


"""
class CreditRiskPrediction(db.Model):

    __tablename__ = "credit_risk_prediction"

    id = db.Column(db.BigInteger,primary_key=True)
    reports = db.Column(db.Integer,nullable=False)
    age = db.Column(db.Numeric(8, 4),nullable=False)
    income = db.Column(db.Numeric(12, 4),nullable=False)
    share = db.Column(db.Numeric(12, 8),nullable=False)
    expenditure = db.Column(db.Numeric(14, 2),nullable=False,default=0)
    owner = db.Column(db.Boolean,nullable=False)
    selfemp = db.Column(db.Boolean,nullable=False)
    dependents = db.Column(db.Integer,nullable=False)
    months = db.Column(db.Integer,nullable=False)
    majorcards = db.Column(db.Integer,nullable=False)
    active = db.Column(db.Integer,nullable=False)
    prediction = db.Column(db.String(20),nullable=True)
    probability = db.Column(db.Numeric(6, 4),nullable=True)
    created_at = db.Column(db.DateTime,server_default=func.now())
    created_by = db.Column(db.String(50),nullable=True)
"""

"""
    # esto quizas podamos utilizarlo
    status = db.Column(db.String(20),nullable=False,default="PENDING")
    model_version = db.Column(db.String(30),nullable=True)
"""

"""
class CreditRiskPredictionExplanation(db.Model):
    __tablename__ = "credit_risk_prediction_explanation"
    id = db.Column(db.BigInteger,primary_key=True)
    prediction_id = db.Column(db.BigInteger,db.ForeignKey("credit_risk_prediction.id"),nullable=False)
    pattern = db.Column(db.Text)
    explanation = db.Column(db.Text)
    confidence = db.Column(db.Float)
    support = db.Column(db.Integer)
    score = db.Column(db.Float)
"""