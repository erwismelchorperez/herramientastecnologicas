from datetime import datetime
from app import db
class ForecastModel(db.Model):
    __tablename__ = 'forecast_model'

    id = db.Column(db.BigInteger,primary_key=True,autoincrement=True)
    institucion_id = db.Column(db.BigInteger,db.ForeignKey('institucion.id'),nullable=False)
    target = db.Column(db.String(50),nullable=False)
    algorithm = db.Column(db.String(80),nullable=False)
    version = db.Column(db.Integer,nullable=False,default=1)
    artifact_path = db.Column(db.Text,nullable=False)
    training_start_date = db.Column(db.Date,nullable=True)
    training_end_date = db.Column(db.Date,nullable=True)
    training_observations = db.Column(db.Integer,nullable=True)
    status = db.Column(db.String(20),nullable=False,default='TRAINED')
    created_at = db.Column(db.DateTime(timezone=True),nullable=False,server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True),nullable=False,server_default=db.func.now(),onupdate=db.func.now())
    # Relaciones
    institucion = db.relationship('Institucion',backref=db.backref('forecast_models',lazy=True))
    metrics = db.relationship('ForecastModelMetric',back_populates='model',cascade='all, delete-orphan')
    runs = db.relationship('ForecastRun',back_populates='model')
    def __repr__(self):
        return (
            f'<ForecastModel '
            f'id={self.id}, '
            f'target={self.target}, '
            f'algorithm={self.algorithm}, '
            f'version={self.version}>')