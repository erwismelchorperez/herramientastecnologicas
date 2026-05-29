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
    
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    
    captacion_data = (CaptacionService.get_general_kpis())
    #chart_data = CarteraService.get_evolution_chart(selected_anio)

    return render_template('captacion/dashboard.html', anios=anios, meses=meses)