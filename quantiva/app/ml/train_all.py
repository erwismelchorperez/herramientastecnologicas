"""
    python -m app.ml.train_all
"""
import joblib
import pandas as pd

from pathlib import Path

from sklearn.metrics import(
mean_absolute_error,
mean_squared_error,
r2_score
)

from sklearn.linear_model import(
LinearRegression,
Ridge
)

from sklearn.ensemble import(
RandomForestRegressor
)

from sklearn.svm import(
SVR
)

from xgboost import(
XGBRegressor
)

from app import db,create_app
from app.models.forecast_prediction import ForecastModelMetrics


class ForecastTrainer:


    MODELS={

    'xgboost':
    XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05
    ),

    'rf':
    RandomForestRegressor(
        n_estimators=300,
        random_state=42
    ),

    'linear':
    LinearRegression(),

    'ridge':
    Ridge(
        alpha=1
    ),

    'svr':
    SVR(
        C=100,
        epsilon=0.1
    )

    }


    @staticmethod
    def train_all():

        app=create_app()

        with app.app_context():

            ROOT=Path(__file__).resolve().parent

            query="""
            SELECT *
            FROM forecast_features
            ORDER BY fecha_corte
            """

            df=pd.read_sql(
                query,
                db.engine
            )

            df['fecha_corte']=pd.to_datetime(
                df['fecha_corte']
            )

            df=df.dropna(
                subset=[
                    'target_cartera_1m'
                ]
            )

            df=df.fillna(
                0
            )

            max_fecha=df[
                'fecha_corte'
            ].max()

            corte=max_fecha-pd.DateOffset(
                months=12
            )

            train=df[
                df['fecha_corte']<corte
            ]

            test=df[
                df['fecha_corte']>=corte
            ]

            print(f'Train: {train["fecha_corte"].min()} → {train["fecha_corte"].max()}')
            print(f'Test: {test["fecha_corte"].min()} → {test["fecha_corte"].max()}')

            X_train=train.drop(
                columns=[
                    'id',
                    'fecha_corte',
                    'target_cartera_1m'
                ]
            )

            y_train=train[
                'target_cartera_1m'
            ]

            X_test=test.drop(
                columns=[
                    'id',
                    'fecha_corte',
                    'target_cartera_1m'
                ]
            )

            y_test=test[
                'target_cartera_1m'
            ]

            resultados=[]

            for nombre,modelo in ForecastTrainer.MODELS.items():

                print(f'Entrenando {nombre}')

                modelo.fit(
                    X_train,
                    y_train
                )

                pred=modelo.predict(
                    X_test
                )

                mae=float(
                    mean_absolute_error(
                        y_test,
                        pred
                    )
                )

                rmse=float(
                    (
                        mean_squared_error(
                            y_test,
                            pred
                        )
                    )**0.5
                )

                mape=float(
                    (
                        abs(
                            (
                                y_test-
                                pred
                            )
                            /
                            y_test
                        )
                    ).mean()*100
                )

                r2=float(
                    r2_score(
                        y_test,
                        pred
                    )
                )

                resultados.append({

                    'modelo':nombre,
                    'mae':round(mae,2),
                    'rmse':round(rmse,2),
                    'mape':round(mape,2),
                    'r2':round(r2,4)

                })

                registro=ForecastModelMetrics.query.filter_by(
                    modelo=nombre
                ).first()

                if not registro:

                    registro=ForecastModelMetrics(
                        modelo=nombre
                    )

                    db.session.add(
                        registro
                    )

                registro.train_inicio=train[
                    'fecha_corte'
                ].min().date()

                registro.train_fin=train[
                    'fecha_corte'
                ].max().date()

                registro.test_inicio=test[
                    'fecha_corte'
                ].min().date()

                registro.test_fin=test[
                    'fecha_corte'
                ].max().date()

                registro.mae=round(mae,4)
                registro.rmse=round(rmse,4)
                registro.mape=round(mape,4)
                registro.r2=round(r2,4)

                db.session.commit()

                joblib.dump(
                    modelo,
                    ROOT/
                    'models'/
                    f'{nombre}.pkl'
                )

                print(f'MAPE={mape:.2f}% RMSE={rmse:,.0f}')

            resultados=pd.DataFrame(
                resultados
            ).sort_values(
                'mape'
            )

            print('\nRanking')
            print(resultados)

            return resultados


if __name__=='__main__':

    ForecastTrainer.train_all()