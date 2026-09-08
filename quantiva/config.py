class Config:

    SECRET_KEY = 'super_secret_key'

    SQLALCHEMY_DATABASE_URI = (
        'postgresql://emelchor:Emelch0r1*@127.0.0.1/quantiva'# BaseDatos Lachao
        #'postgresql://emelchor:Emelch0r1*@127.0.0.1/quantiva_waacachi'# BaseDatos Bedardo
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False