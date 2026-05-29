from flask import Blueprint,render_template,request
from flask_login import login_required

from app.services.filter_service import FilterService
from app.services.cartera_service import CarteraService

forecast_cartera = Blueprint('forecast_cartera',__name__,url_prefix='/forecast_cartera')
@forecast_cartera.route('/forecast_cartera')
@login_required
def dashboard():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template(
        'ia/forecast_cartera.html',
        anios=anios,
        meses=meses,
        selected_anio=selected_anio,
        selected_mes=selected_mes,
        **chart_data
        )
