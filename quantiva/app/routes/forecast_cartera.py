from flask import Blueprint,render_template,request
from flask_login import login_required, current_user

from app.services.filter_service import FilterService
from app.services.cartera_service import CarteraService
from app.services.forecast_dashboard_service import ForecastDashboardService

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
@forecast_cartera.route('/resumen')
@login_required
def resumen():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    anios = (FilterService.get_available_years('all'))
    meses = (FilterService.get_available_months(selected_anio))
    chart_data = CarteraService.get_evolution_chart('all',selected_anio)
    forecast_data = ForecastDashboardService.get_dashboard_data(current_user.institucion_id)
    print("Forecast active models:      ", forecast_data)
    return render_template('forecasting/dashboard.html',anios=anios,meses=meses,selected_anio=selected_anio,**chart_data, **forecast_data)
@forecast_cartera.route('/generar')
@login_required
def generar():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('ia/forecast_cartera.html',anios=anios,meses=meses,selected_anio=selected_anio,selected_mes=selected_mes,**chart_data)
@forecast_cartera.route('/institucion')
@login_required
def institucion():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('ia/forecast_cartera.html',anios=anios,meses=meses,selected_anio=selected_anio,selected_mes=selected_mes,**chart_data)
@forecast_cartera.route('/sucursales')
@login_required
def sucursales():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('ia/forecast_cartera.html',anios=anios,meses=meses,selected_anio=selected_anio,selected_mes=selected_mes,**chart_data)
@forecast_cartera.route('/historial')
@login_required
def historial():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('ia/forecast_cartera.html',anios=anios,meses=meses,selected_anio=selected_anio,selected_mes=selected_mes,**chart_data)
@forecast_cartera.route('/modelos_institucionales')
@login_required
def modelos_institucionales():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('ia/forecast_cartera.html',anios=anios,meses=meses,selected_anio=selected_anio,selected_mes=selected_mes,**chart_data)
@forecast_cartera.route('/modelos_sucursal')
@login_required
def modelos_sucursal():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('ia/forecast_cartera.html',anios=anios,meses=meses,selected_anio=selected_anio,selected_mes=selected_mes,**chart_data)
@forecast_cartera.route('/evaluacion_modelos')
@login_required
def evaluacion_modelos():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('ia/forecast_cartera.html',anios=anios,meses=meses,selected_anio=selected_anio,selected_mes=selected_mes,**chart_data)