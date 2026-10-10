from flask import Blueprint,render_template,request
from flask_login import login_required

from app.services.filter_service import FilterService
from app.services.cartera_service import CarteraService
from app.services.institution_service import InstitucionService

cartera = Blueprint('cartera',__name__,url_prefix='/cartera')
@cartera.route('/dashboard')
@login_required
def dashboard():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years('all'))
    meses = (FilterService.get_available_months(selected_anio))
    sucursales = FilterService.get_available_branches()
    sucursales.insert(0, 'all')
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart('all',selected_anio)
    print("Sucursales       ",sucursales, "         ", type(sucursales) )
    print(" get_general_kpis        ", chart_data)
    return render_template(
        'cartera/dashboard.html',
        anios=anios,
        meses=meses,
        sucursales = sucursales,
        selected_anio=selected_anio,
        selected_mes=selected_mes,
        **chart_data
        )
@cartera.route('/sucursales')
@login_required
def sucursales():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years('all'))
    meses = (FilterService.get_available_months(selected_anio))
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart('all',selected_anio)

    return render_template(
        'cartera/sucursales.html',
        anios=anios,
        meses=meses,
        selected_anio=selected_anio,
        selected_mes=selected_mes,
        **chart_data
        )
@cartera.route('/calidad')
@login_required
def calidad():
    ultimo_periodo = CarteraService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years('all'))
    meses = (FilterService.get_available_months(selected_anio))
    sucursales = FilterService.get_available_branches()
    tipo_institucion = InstitucionService.get_tipo_institucion()
    sucursales.insert(0, 'all')
    cartera_data = (CarteraService.get_general_kpis())
    chart_data = CarteraService.get_evolution_chart('all',selected_anio)
    print("tipo institucion         ", tipo_institucion)
    return render_template(
        'cartera/calidad.html',
        anios=anios,
        meses=meses,
        sucursales=sucursales,
        selected_anio=selected_anio,
        selected_mes=selected_mes,
        tipo_institucion=tipo_institucion,
        **chart_data
        )