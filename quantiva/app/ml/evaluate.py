"""
    python -m app.ml.evaluate
"""
import pandas as pd
from sqlalchemy import create_engine,text
from app import create_app


class ForecastEvaluator:


    @staticmethod
    def update_predictions():

        app=create_app()

        with app.app_context():

            engine=create_engine(
                app.config[
                    'SQLALCHEMY_DATABASE_URI'
                ]
            )

            query="""

            SELECT

            p.id,
            p.fecha_prediccion,
            p.cartera_predicha,

            d.cartera_total

            FROM forecast_prediction p

            INNER JOIN forecast_dataset d

            ON p.fecha_prediccion=
            d.fecha_corte

            WHERE p.estado='PENDIENTE'

            """

            df=pd.read_sql(
                query,
                engine
            )

            conn=engine.connect()

            for _,row in df.iterrows():

                real=float(
                    row[
                        'cartera_total'
                    ]
                )

                pred=float(
                    row[
                        'cartera_predicha'
                    ]
                )

                error_abs=abs(
                    real-
                    pred
                )

                error_pct=0

                if real>0:

                    error_pct=(
                        error_abs
                        /
                        real
                    )*100

                conn.execute(

                text("""

                UPDATE
                forecast_prediction

                SET

                cartera_real=:real,

                error_absoluto=:abs,

                error_porcentual=:pct,

                estado='EVALUADO'

                WHERE id=:id

                """),

                {

                'real':real,

                'abs':error_abs,

                'pct':error_pct,

                'id':int(
                    row[
                        'id'
                    ]
                )

                }

                )

            conn.commit()

            print(
                f'{len(df)} predicciones evaluadas'
            )


if __name__=='__main__':

    ForecastEvaluator.update_predictions()