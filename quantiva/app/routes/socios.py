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
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))

    return render_template(
        'socios/dashboard.html',
        anios=anios,
        meses=meses,
        selected_anio=selected_anio,
        selected_mes=selected_mes
        )
