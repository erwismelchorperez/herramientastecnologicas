from flask import Blueprint,render_template,request
from flask_login import login_required

from app.services.filter_service import FilterService
from app.services.socios_service import SociosService

socios = Blueprint('socios',__name__,url_prefix='/socios')
@socios.route('/dashboard')
@login_required
def dashboard():
    ultimo_periodo = SociosService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years_socios('all'))
    meses = (FilterService.get_available_months_socios(selected_anio))

    return render_template(
        'socios/dashboard.html',
        anios=anios,
        meses=meses,
        selected_anio=selected_anio,
        selected_mes=selected_mes
        )
@socios.route('/perfil')
@login_required
def perfil():
    ultimo_periodo = SociosService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years_socios('all'))
    meses = (FilterService.get_available_months(selected_anio))

    return render_template(
        'socios/perfil.html',
        anios=anios,
        meses=meses,
        selected_anio=selected_anio,
        selected_mes=selected_mes
        )
@socios.route('/vinculacion')
@login_required
def vinculacion():
    ultimo_periodo = SociosService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years_socios(sucursal='all'))
    print("anios:             ", anios)
    meses = (FilterService.get_available_months_socios(selected_anio))
    sucursales = FilterService.get_available_branches()
    sucursales.insert(0, 'all')
    return render_template(
        'socios/vinculacion.html',
        anios=anios,
        meses=meses,
        selected_anio=selected_anio,
        selected_mes=selected_mes,
        sucursales=sucursales)