from datetime import datetime

from app import db


class ForecastComparison(db.Model):

    __tablename__ = 'forecast_comparison'

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    forecast_value_id = db.Column(
        db.BigInteger,
        db.ForeignKey('forecast_value.id', ondelete='CASCADE'),
        nullable=False,
        unique=True
    )

    actual_value = db.Column(
        db.Numeric(20, 4),
        nullable=False
    )

    error = db.Column(
        db.Numeric(20, 4),
        nullable=False
    )

    absolute_error = db.Column(
        db.Numeric(20, 4),
        nullable=False
    )

    absolute_percentage_error = db.Column(
        db.Numeric(20, 8),
        nullable=True
    )

    evaluated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )

    # Relaciones
    forecast_value = db.relationship(
        'ForecastValue',
        back_populates='comparison'
    )

    def __repr__(self):
        return (
            f'<ForecastComparison '
            f'forecast_value_id={self.forecast_value_id}, '
            f'actual={self.actual_value}, '
            f'error={self.error}>'
        )