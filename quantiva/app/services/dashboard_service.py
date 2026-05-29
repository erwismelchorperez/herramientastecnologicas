from app.services.cartera_service import CarteraService
from app.services.captacion_service import CaptacionService
from app.utils.months import month_case
from app import db
from app.models.creditos import Credito
from sqlalchemy import func, desc
class DashboardService:
    @staticmethod
    def get_dashboard_data():
        cartera_data = (CarteraService.get_general_kpis())
        captacion_data = (CaptacionService.get_general_kpis())
        chart_data = CarteraService.get_evolution_chart()
        return {**cartera_data,**captacion_data, **chart_data}
    @staticmethod
    def get_evolution_cartera(anio=None):
        if not anio:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio

        mes_orden = month_case(Credito.mes)
        datos = db.session.query(
            Credito.mes,
            func.sum(
                Credito.capital_vigente
            ).label('total')
        ).filter(
            Credito.anio == anio
        ).group_by(
            Credito.mes
        ).order_by(
            mes_orden.asc()
        ).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.mes.upper())
            series.append(float(row.total))
        return {
            'chart_labels': labels,
            'chart_series': series
        }