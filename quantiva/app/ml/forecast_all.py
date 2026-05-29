"""
    python -m app.ml.forecast_all
"""
import joblib
import pandas as pd

from pathlib import Path
from pandas.tseries.offsets import MonthEnd
from sqlalchemy.orm.attributes import flag_modified

from app import db,create_app
from app.models.forecast_prediction import ForecastPrediction,ForecastModelMetrics


class ForecastPredictor:

    @staticmethod
    def forecast_all():

        app=create_app()

        with app.app_context():

            ROOT=Path(__file__).resolve().parent

            query="""
            SELECT *
            FROM forecast_features
            ORDER BY fecha_corte DESC
            LIMIT 1
            """

            df=pd.read_sql(query,db.engine)

            actual=float(df.iloc[0]['cartera_total'])

            fecha=pd.to_datetime(df.iloc[0]['fecha_corte'])

            fecha_prediccion=(fecha+MonthEnd(1)).date()

            X=df.drop(
                columns=[
                    'id',
                    'fecha_corte',
                    'target_cartera_1m'
                ]
            )

            metricas={
                str(x.modelo).strip().lower():x
                for x in ForecastModelMetrics.query.all()
            }

            for archivo in (ROOT/'models').glob('*.pkl'):
                modelo=archivo.stem.lower()
                print(f'Forecast {modelo}')
                predictor=joblib.load(archivo)
                forecast=float(predictor.predict(X)[0])
                crecimiento=0

                if actual>0:
                    crecimiento=((forecast-actual)/actual)*100

                registro=ForecastPrediction.query.filter_by(
                    modelo=modelo,
                    fecha_prediccion=fecha_prediccion
                ).first()

                if registro:
                    print(f'UPDATE -> {modelo}')
                    print("Registro:            ", registro)
                else:
                    print(f'INSERT -> {modelo}')
                    registro=ForecastPrediction(
                        modelo=modelo,
                        fecha_prediccion=fecha_prediccion
                    )

                registro.fecha_base=fecha.date()
                registro.horizonte_meses=1
                registro.cartera_real=None
                registro.cartera_predicha=round(float(forecast),2)
                registro.error_absoluto=None
                registro.error_porcentual=None
                registro.estado='PENDIENTE'
                registro.crecimiento_esperado=round(float(crecimiento),4)

                if modelo in metricas:
                    print("      metricas[modelo]   ", metricas[modelo])
                    m=metricas[modelo]
                    registro.mae=float(m.mae) if m.mae is not None else None
                    registro.rmse=float(m.rmse) if m.rmse is not None else None
                    registro.mape=float(m.mape) if m.mape is not None else None
                    registro.r2=float(m.r2) if m.r2 is not None else None

                    print(
                        f'Metricas -> '
                        f'MAE={registro.mae} '
                        f'RMSE={registro.rmse} '
                        f'MAPE={registro.mape} '
                        f'R2={registro.r2}'
                    )


                db.session.flush()

                flag_modified(registro,'mae')
                flag_modified(registro,'rmse')
                flag_modified(registro,'mape')
                flag_modified(registro,'r2')
                #db.session.merge(registro)

            db.session.commit()

            print(f'Forecasts guardados {fecha_prediccion}')

if __name__=='__main__':

    ForecastPredictor.forecast_all()