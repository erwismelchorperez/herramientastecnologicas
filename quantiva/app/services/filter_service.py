from app import db
from app.models.creditos import Credito
from app.models.captacion import Captacion
from app.models.socios import Socios
from app.utils.months import month_case

class FilterService:
    @staticmethod
    def get_available_years():
        anios = db.session.query(
            Credito.anio
        ).distinct().order_by(
            Credito.anio.desc()
        ).all()
        return [
            row.anio for row in anios
        ]
    @staticmethod
    def get_available_months(anio=None):
        mes_orden = month_case(Credito.mes)

        query = db.session.query(
            Credito.mes,
            mes_orden.label('mes_num')
        )
        print("ultimo anio:             ", anio)
        if anio:
            query = query.filter(Credito.anio == anio)
        
        meses = query.distinct().order_by("mes_num").all()

        return [
            row.mes for row in meses
        ]
    @staticmethod
    def get_available_months_captacion(anio=None):
        mes_orden = month_case(Captacion.mes)
        query = db.session.query(Captacion.mes,mes_orden.label('mes_num'))
        print("ultimo anio:             ", anio)
        if anio:
            query = query.filter(Captacion.anio == anio)
        meses = query.distinct().order_by("mes_num").all()
        return [row.mes for row in meses]
    @staticmethod
    def get_available_months_socios(anio=None):
        mes_orden = month_case(Socios.mes)
        query = db.session.query(Socios.mes,mes_orden.label('mes_num'))
        print("ultimo anio:             ", anio)
        if anio:
            query = query.filter(Socios.anio == anio)
        meses = query.distinct().order_by("mes_num").all()
        return [row.mes for row in meses]