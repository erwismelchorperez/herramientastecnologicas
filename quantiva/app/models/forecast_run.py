from app import db
from sqlalchemy import ForeignKeyConstraint


class ForecastRun(db.Model):

    __tablename__ = 'forecast_run'

    __table_args__ = (
        ForeignKeyConstraint(
            ['model_id', 'institucion_id'],
            [
                'forecast_model.id',
                'forecast_model.institucion_id'
            ],
            name='fk_forecast_run_model'
        ),
    )

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    model_id = db.Column(
        db.BigInteger,
        nullable=False
    )

    institucion_id = db.Column(
        db.BigInteger,
        nullable=False
    )

    forecast_origin_date = db.Column(
        db.Date,
        nullable=False
    )

    generated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )

    horizon = db.Column(
        db.SmallInteger,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default='COMPLETED'
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )

    # Relaciones
    model = db.relationship(
        'ForecastModel',
        back_populates='runs'
    )

    values = db.relationship(
        'ForecastValue',
        back_populates='forecast_run',
        cascade='all, delete-orphan',
        order_by='ForecastValue.forecast_date'
    )

    def __repr__(self):
        return (
            f'<ForecastRun '
            f'id={self.id}, '
            f'model_id={self.model_id}, '
            f'institucion_id={self.institucion_id}, '
            f'origin={self.forecast_origin_date}, '
            f'horizon={self.horizon}>'
        )