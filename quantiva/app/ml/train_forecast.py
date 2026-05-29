"""
    colocarnos a nivel del proyecto y ejecutar de la siguiente manera (debemos estar a nivel de donde iniciamos entorno virtual)
    python -m app.ml.train_forecast
"""

import pandas as pd
import joblib

from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from xgboost import XGBRegressor

from app import create_app
from pathlib import Path


class ForecastTrainer:

    @staticmethod
    def train_cartera_model():

        app=create_app()

        with app.app_context():

            engine=create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

            query="""
                SELECT *
                FROM forecast_features
                WHERE target_cartera_1m IS NOT NULL
                ORDER BY fecha_corte
            """

            df=pd.read_sql(query,engine)

            X=df.drop(columns=['id','fecha_corte','target_cartera_1m'])

            y=df['target_cartera_1m']

            df['fecha_corte']=pd.to_datetime(df['fecha_corte'])
            ultima_fecha=df['fecha_corte'].max()
            fecha_test=(ultima_fecha-pd.DateOffset(months=11))

            train=df[df['fecha_corte']<fecha_test]
            test=df[df['fecha_corte']>=fecha_test]

            X_train=train.drop(columns=['id','fecha_corte','target_cartera_1m'])
            y_train=train['target_cartera_1m']
            X_test=test.drop(columns=['id','fecha_corte','target_cartera_1m'])
            y_test=test['target_cartera_1m']

            print(f'Train: {len(train)} meses')
            print(f'Test: {len(test)} meses')
            print(f'Train hasta: {train["fecha_corte"].max()}')
            print(f'Test desde: {test["fecha_corte"].min()}')

            model=XGBRegressor(n_estimators=300,max_depth=4,learning_rate=0.03,subsample=0.9,colsample_bytree=0.8,random_state=42)

            model.fit(X_train,y_train)
            pred=model.predict(X_test)
            mae=mean_absolute_error(y_test,pred)
            rmse=(mean_squared_error(y_test,pred))**0.5
            r2=r2_score(y_test,pred)

            print('RESULTADOS')
            print(f'MAE: {mae:,.2f}')
            print(f'RMSE: {rmse:,.2f}')
            print(f'R²: {r2:.4f}')

            
            ROOT=Path(__file__).resolve().parent
            model_dir=ROOT / 'models'
            model_dir.mkdir(exist_ok=True)

            model_path=model_dir / 'cartera_forecast.pkl'
            joblib.dump(model,model_path)

            print('Modelo guardado')

            return model


if __name__=='__main__':

    ForecastTrainer.train_cartera_model()