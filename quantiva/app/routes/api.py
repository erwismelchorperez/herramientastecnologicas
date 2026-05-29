from flask import Blueprint,jsonify,request
from app.services.filter_service import FilterService
from app.services.cartera_service import CarteraService
from app.services.captacion_service import CaptacionService
from app.services.socios_service import SociosService
from app.services.ia_service import ForecastService
from app.services.dashboard_service import DashboardService
api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/months')
def get_months():
    anio = request.args.get('anio',type=int)
    meses = (FilterService.get_available_months(anio))
    return jsonify(meses)
@api.route('/cartera/kpis')
def cartera_kpis():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_general_kpis(anio,mes)

    return jsonify(data)
@api.route('/cartera/chart')
def cartera_chart():
    anio = request.args.get('anio',type=int)
    data = (CarteraService.get_evolution_chart(anio))

    return jsonify(data)
@api.route('/cartera/product-chart')
def cartera_product_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')

    data = CarteraService.get_product_chart(anio,mes)
    return jsonify(data)
@api.route('/cartera/clasificacion-chart')
def cartera_clasificacion_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')

    data = CarteraService.get_clasificacion_chart(anio,mes)
    return jsonify(data)
@api.route('/cartera/branch-chart')
def cartera_branch_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_branch_chart(anio,mes)

    return jsonify(data)
@api.route('/cartera/clasificacion-status-chart')
def cartera_clasificacion_statuschart():
    anio = request.args.get('anio',type=int)

    mes = request.args.get('mes')

    data = CarteraService.get_clasificacion_statuschart(anio,mes)
    return jsonify(data)
@api.route('/cartera/sucursal-count-chart')
def api_cartera_sucursal_count_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_sucursal_count_chart(anio,mes)
    return jsonify(data)
@api.route('/cartera/sucursal-vigente-chart')
def sucursal_vigente_chart():

    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')

    data = CarteraService.get_sucursal_vigente_chart(anio,mes)
    return jsonify(data)
@api.route('/cartera/sucursal-vencido-chart')
def sucursal_vencido_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_sucursal_vencido_chart(anio,mes)
    return jsonify(data)
@api.route('/cartera/top-productos-vigente-chart')
def top_productos_vigente_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_top_productos_vigente_chart(anio,mes)
    return jsonify(data)
@api.route('/cartera/productos-table')
def productos_table():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_productos_table(anio,mes)
    return jsonify(data)
"""
    Captación
"""
@api.route('/months_captacion')
def get_months_captacion():
    anio = request.args.get('anio',type=int)
    meses = (FilterService.get_available_months_captacion(anio))
    return jsonify(meses)
@api.route('/captacion/kpis')
def captacion_kpis():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CaptacionService.get_general_kpis(anio,mes)
    return jsonify(data)
@api.route('/captacion/evolution-chart')
def captacion_evolution_chart():
    anio = request.args.get('anio',type=int)
    data = CaptacionService.get_evolution_chart(anio)
    return jsonify(data)
@api.route('/captacion/producto-chart')
def captacion_producto_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CaptacionService.get_producto_chart(anio,mes)

    return jsonify(data)
@api.route('/captacion/sucursal-chart')
def captacion_sucursal_chart():
    anio = request.args.get('anio',type=int)

    mes = request.args.get('mes')
    data = CaptacionService.get_sucursal_chart(anio,mes)

    return jsonify(data)
@api.route('/captacion/tipo-socio-chart')
def captacion_tipo_socio_chart():

    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CaptacionService.get_tipo_socio_chart(anio,mes)

    return jsonify(data)
"""
    Socios
"""
@api.route('/months_socios')
def get_months_socios():
    anio = request.args.get('anio',type=int)
    meses = (FilterService.get_available_months_socios(anio))
    return jsonify(meses)
@api.route('/socios/kpis')
def socios_kpis():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = SociosService.get_general_kpis(anio,mes)
    return jsonify(data)
@api.route('/socios/sucursal-chart')
def socios_sucursal_chart():
    anio=request.args.get('anio', type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_sucursal_chart(anio, mes ) )
@api.route('/socios/sexo-chart')
def socios_sexo_chart():
    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_sexo_chart(anio,mes))
@api.route('/socios/edad-chart')
def socios_edad_chart():

    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_edad_chart(anio,mes))
@api.route('/socios/antiguedad-chart')
def socios_antiguedad_chart():

    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_antiguedad_chart(anio,mes))
"""
    Forecast
"""
@api.route('/forecast_cartera/cards')
def get_cards():
    modelo=request.args.get('modelo','xgboost')
    print("     forecast_cartera        ", modelo)
    return jsonify(ForecastService.get_resume_cards(modelo))
"""
    Dashboard inicial
"""
@api.route('/dashboard/cartera')
def get_evolution_cartera(anio=None):
    return jsonify(DashboardService.get_evolution_cartera(anio))