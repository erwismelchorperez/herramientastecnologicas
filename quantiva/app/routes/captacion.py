from flask import Blueprint,render_template,request
from flask_login import login_required

from app.services.filter_service import FilterService
from app.services.captacion_service import CaptacionService

captacion = Blueprint('captacion',__name__,url_prefix='/captacion')
@captacion.route('/dashboard')
@login_required
def dashboard():
    
    ultimo_periodo = CaptacionService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    
    anios = (FilterService.get_available_years_captacion('all'))
    meses = (FilterService.get_available_months_captacion('all',selected_anio))
    sucursales = FilterService.get_available_branches()
    sucursales.insert(0, 'all')
    
    captacion_data = (CaptacionService.get_general_kpis('all',selected_anio,selected_mes))
    #chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('captacion/dashboard.html', anios=anios, meses=meses, sucursales=sucursales)
@captacion.route('/analisisahorradores')
@login_required
def analisisahorradores():
    
    ultimo_periodo = CaptacionService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    
    anios = (FilterService.get_available_years('all'))
    meses = (FilterService.get_available_months_captacion('all',selected_anio))
    sucursales = FilterService.get_available_branches()
    sucursales.insert(0, 'all')
    
    captacion_data = (CaptacionService.get_general_kpis('all',selected_anio,selected_mes))
    #chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('captacion/analisisahorradores.html', anios=anios, meses=meses, sucursales=sucursales)
@captacion.route('/resumen')
@login_required
def resumen():
    ultimo_periodo = CaptacionService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    print("selected_anio",selected_anio)
    print("selected_mes",selected_mes)
    anios = (FilterService.get_available_years_captacion('all'))
    meses = (FilterService.get_available_months_captacion('all',selected_anio))
    sucursales = FilterService.get_available_branches()
    sucursales.insert(0, 'all')
    
    captacion_data = (CaptacionService.get_general_kpis('all',selected_anio,selected_mes))
    #chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('captacion/resumen.html', anios=anios, meses=meses, sucursales=sucursales)
@captacion.route('/sociosconcentracion')
@login_required
def sociosconcentracion():
    ultimo_periodo = CaptacionService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    anios = (FilterService.get_available_years_captacion('all'))
    meses = (FilterService.get_available_months_captacion('all',selected_anio))
    sucursales = FilterService.get_available_branches()
    sucursales.insert(0, 'all')

    return render_template('captacion/sociosconcentracion.html', anios=anios, meses=meses, sucursales=sucursales)