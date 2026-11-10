from datetime import datetime

from app import db


class ForecastValue(db.Model):

    __tablename__ = 'forecast_value'

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    forecast_run_id = db.Column(
        db.BigInteger,
        db.ForeignKey('forecast_run.id', ondelete='CASCADE'),
        nullable=False
    )

    forecast_date = db.Column(
        db.Date,
        nullable=False
    )

    step = db.Column(
        db.SmallInteger,
        nullable=False
    )

    predicted_value = db.Column(
        db.Numeric(20, 4),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )

    # Relaciones
    forecast_run = db.relationship(
        'ForecastRun',
        back_populates='values'
    )

    comparison = db.relationship(
        'ForecastComparison',
        back_populates='forecast_value',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (
            f'<ForecastValue '
            f'id={self.id}, '
            f'date={self.forecast_date}, '
            f'predicted={self.predicted_value}>'
        )