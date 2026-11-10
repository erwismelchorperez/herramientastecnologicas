from datetime import datetime

from app import db


class ForecastModelMetric(db.Model):

    __tablename__ = 'forecast_model_metric'

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    model_id = db.Column(
        db.BigInteger,
        db.ForeignKey('forecast_model.id', ondelete='CASCADE'),
        nullable=False
    )

    evaluation_stage = db.Column(
        db.String(20),
        nullable=False
    )

    metric_name = db.Column(
        db.String(20),
        nullable=False
    )

    metric_value = db.Column(
        db.Numeric(20, 8),
        nullable=False
    )

    fold = db.Column(
        db.SmallInteger,
        nullable=False,
        default=0
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )

    # Relaciones
    model = db.relationship(
        'ForecastModel',
        back_populates='metrics'
    )

    def __repr__(self):
        return (
            f'<ForecastModelMetric '
            f'model_id={self.model_id}, '
            f'metric={self.metric_name}, '
            f'value={self.metric_value}>'
        )