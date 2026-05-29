from app import db

class ForecastPrediction(db.Model):
    __tablename__='forecast_prediction'
    id=db.Column(db.BigInteger,primary_key=True)
    modelo=db.Column(db.String(100),nullable=False)
    fecha_generacion=db.Column(db.DateTime)
    fecha_base=db.Column(db.Date,nullable=False)
    fecha_prediccion=db.Column(db.Date,nullable=False)
    horizonte_meses=db.Column(db.Integer,default=1)
    cartera_real=db.Column(db.Numeric(18,2))
    cartera_predicha=db.Column(db.Numeric(18,2),nullable=False)
    crecimiento_esperado=db.Column(db.Numeric(10,4))
    error_absoluto=db.Column(db.Numeric(18,2))
    error_porcentual=db.Column(db.Numeric(10,4))
    estado=db.Column(db.String(20),default='PENDIENTE')

    mae=db.Column(db.Numeric(18,4))
    rmse=db.Column(db.Numeric(18,4))
    mape=db.Column(db.Numeric(18,4))
    r2=db.Column(db.Numeric(18,4))

class ForecastModelMetrics(db.Model):

    __tablename__='forecast_model_metrics'
    id=db.Column(db.BigInteger,primary_key=True)
    modelo=db.Column(db.String(100),nullable=False)
    train_inicio=db.Column(db.Date,nullable=False)
    train_fin=db.Column(db.Date,nullable=False)
    test_inicio=db.Column(db.Date,nullable=False)
    test_fin=db.Column(db.Date,nullable=False)
    mae=db.Column(db.Numeric(18,4))
    rmse=db.Column(db.Numeric(18,4))
    mape=db.Column(db.Numeric(18,4))
    r2=db.Column(db.Numeric(18,4))