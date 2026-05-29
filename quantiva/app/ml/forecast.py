"""
     python -m app.ml.forecast
"""
import joblib
import pandas as pd
from pathlib import Path
from pandas.tseries.offsets import MonthEnd
from app import db,create_app
from app.models.forecast_prediction import ForecastPrediction


class ForecastPredictor:

    @staticmethod
    def forecast_next_month():

        app=create_app()

        with app.app_context():

            ROOT=Path(__file__).resolve().parent

            model=joblib.load(ROOT/'models'/'cartera_forecast.pkl')

            query="""
            SELECT *
            FROM forecast_features
            ORDER BY fecha_corte DESC
            LIMIT 1
            """

            df=pd.read_sql(query,db.engine)

            actual=float(df.iloc[0]['cartera_total'])
            fecha=df.iloc[0]['fecha_corte']

            X=df.drop(columns=['id','fecha_corte','target_cartera_1m'])

            forecast=float(model.predict(X)[0])

            crecimiento=0

            if actual>0:
                crecimiento=((forecast-actual)/actual)*100

            print(f'Periodo base: {fecha}')
            print(f'Cartera actual: ${actual:,.2f}')
            print(f'Forecast siguiente mes: ${forecast:,.2f}')
            print(f'Crecimiento esperado: {crecimiento:.2f}%')

            fecha_prediccion=(pd.to_datetime(fecha)+MonthEnd(1)).date()

            registro=ForecastPrediction.query.filter_by(
                modelo='xgboost',
                fecha_prediccion=fecha_prediccion
            ).first()

            if registro:

                registro.fecha_base=fecha
                registro.cartera_predicha=forecast
                registro.crecimiento_esperado=round(crecimiento,4)

            else:

                registro=ForecastPrediction(
                    modelo='xgboost',
                    fecha_base=fecha,
                    fecha_prediccion=fecha_prediccion,
                    cartera_predicha=forecast,
                    crecimiento_esperado=round(crecimiento,4)
                )

                db.session.add(registro)

            db.session.commit()

            print(f'Predicción guardada para {fecha_prediccion}')

            return{
                'periodo':str(fecha),
                'actual':actual,
                'forecast':forecast,
                'crecimiento':round(crecimiento,2)
            }
if __name__=='__main__':

    ForecastPredictor.forecast_next_month()