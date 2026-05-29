from sqlalchemy import func

from app import db
from app.models.forecast_prediction import ForecastPrediction,  ForecastModelMetrics


class ForecastService:
    @staticmethod
    def get_resume_cards(modelo='xgboost'):
        ultimo=(
            db.session.query(
                ForecastPrediction
            )
            .filter(
                ForecastPrediction.modelo==modelo
            )
            .order_by(
                ForecastPrediction.fecha_prediccion.desc()
            )
            .first()
        )
        print("ultimo           ", ultimo)
        if not ultimo:
            return{
                'forecast':0,
                'crecimiento':0,
                'mape':0,
                'precision':0
            }

        precision=max(0,100-float(ultimo.mape or 0))

        return{
            'forecast':float(ultimo.cartera_predicha or 0),
            'crecimiento':float(ultimo.crecimiento_esperado or 0),
            'mape':float(ultimo.mape or 0),
            'precision':round(precision,2)
        }