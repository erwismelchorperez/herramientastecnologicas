from flask import Blueprint,jsonify,request
from app.services.filter_service import FilterService
from app.services.cartera_service import CarteraService
from app.services.captacion_service import CaptacionService
from app.services.socios_service import SociosService
from app.services.ia_service import ForecastService
from app.services.dashboard_service import DashboardService
from app.services.institution_service import InstitucionService
api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/tipo_institucion')
def tipo_institucion():
    data = InstitucionService.get_tipo_institucion()
    return jsonify(data)
@api.route('/years')
def get_years():
    sucursal = request.args.get('sucursal')
    meses = (FilterService.get_available_years(sucursal))
    return jsonify(meses)
@api.route('/months')
def get_months():
    anio = request.args.get('anio',type=int)
    meses = (FilterService.get_available_months(anio))
    return jsonify(meses)
@api.route('/cartera/kpis')
def cartera_kpis():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    data = CarteraService.get_general_kpis(sucursal,anio,mes)
    return jsonify(data)
@api.route('/cartera/chart')
def cartera_chart():
    sucursal = request.args.get('sucursal')
    print("cartera_chart            ",sucursal)
    anio = request.args.get('anio',type=int)
    data = (CarteraService.get_evolution_chart(sucursal, anio))
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
    sucursal = request.args.get('sucursal')

    data = CarteraService.get_clasificacion_statuschart(sucursal,anio,mes)
    return jsonify(data)
@api.route('/cartera/sucursal-count-chart')
def api_cartera_sucursal_count_chart():
    sucursal = request.args.get('sucursal')
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_sucursal_count_chart(sucursal,anio,mes)
    return jsonify(data)
@api.route('/cartera/sucursal-vigente-chart')
def sucursal_vigente_chart():
    sucursal = request.args.get('sucursal')
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_sucursal_vigente_chart(sucursal,anio,mes)
    return jsonify(data)
@api.route('/cartera/sucursal-vigente-anual-chart')
def sucursal_vigente_anual_chart():
    mes = request.args.get('mes')
    return jsonify(CarteraService.get_sucursal_vigente_anual_chart(mes))
@api.route('/cartera/sucursal-vencido-chart')
def sucursal_vencido_chart():
    sucursal = request.args.get('sucursal')
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CarteraService.get_sucursal_vencido_chart(sucursal,anio,mes)
    return jsonify(data)
@api.route('/cartera/top-productos-vigente-chart')
def top_productos_vigente_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    data = CarteraService.get_top_productos_vigente_chart(sucursal,anio,mes)
    return jsonify(data)
@api.route('/cartera/productos-table')
def productos_table():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    page=request.args.get('page',1,type=int)
    data = CarteraService.get_productos_table(anio,mes,page)
    return jsonify(data)
@api.route('/cartera/sucursal-vigente-vencido-chart')
def sucursal_vigente_vencido_chart():
    anio = request.args.get('anio', type=int)
    mes = request.args.get('mes')
    return jsonify(CarteraService.get_sucursal_vigente_vencido_chart(anio,mes))
@api.route('/cartera/get_monto_original_por_producto_mes')
def get_monto_original_por_producto_mes():
    sucursal = request.args.get('sucursal')
    anio = request.args.get('anio',type=int)
    data = CarteraService.get_monto_original_por_producto_mes(sucursal,anio)
    return jsonify(data)
@api.route('/cartera/evolution-vig-venc-chart')
def get_evolutionvigvenc_chart():

    anio = request.args.get('anio', type=int)
    sucursal = request.args.get('sucursal')

    return jsonify(CarteraService.get_evolutionvigvenc_chart(sucursal,anio))
@api.route('/cartera/get_colocacion_mensual')
def get_colocacion_mensual():
    anio = request.args.get('anio', type=int)
    sucursal = request.args.get('sucursal')
    return jsonify(CarteraService.get_colocacion_mensual(sucursal,anio))
@api.route('/cartera/get_creditos_otorgados_mensual')
def get_creditos_otorgados_mensual():
    anio = request.args.get('anio', type=int)
    sucursal = request.args.get('sucursal')
    return jsonify(CarteraService.get_creditos_otorgados_mensual(sucursal,anio))
@api.route('/cartera/get_montos_por_tipo_garantia')
def get_montos_por_tipo_garantia():
    anio = request.args.get('anio', type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    return jsonify(CarteraService.get_montos_por_tipo_garantia(sucursal,anio))
@api.route('/cartera/get_garantias_por_sucursal')
def get_garantias_por_sucursal():
    anio = request.args.get('anio', type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    return jsonify(CarteraService.get_garantias_por_sucursal(sucursal,anio))
@api.route('/cartera/get_eprc_por_sucursal')
def get_eprc_por_sucursal():
    anio = request.args.get('anio', type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    return jsonify(CarteraService.get_eprc_por_sucursal(sucursal,anio))
@api.route('/cartera/get_eprc_por_clasificacion')
def get_eprc_por_clasificacion():
    sucursal = request.args.get('sucursal', 'all')
    anio = request.args.get('anio')
    mes = request.args.get('mes')
    print("get_eprc_por_clasificacion   ",sucursal,anio,mes)
    resultado = CarteraService.get_eprc_por_clasificacion(sucursal=sucursal,anio=anio,mes=mes)
    return jsonify(resultado)
@api.route('/cartera/get_top_10_acreditados_capital')
def get_top_10_acreditados_capital():
    sucursal = request.args.get('sucursal', 'all')
    anio = request.args.get('anio')
    mes = request.args.get('mes')

    resultado = CarteraService.get_top_10_acreditados_capital(sucursal=sucursal,anio=anio,mes=mes)
    return jsonify(resultado)
@api.route('/cartera/get_top_10_acreditados_capital_vencido')
def get_top_10_acreditados_capital_vencido():
    sucursal = request.args.get('sucursal', 'all')
    anio = request.args.get('anio')
    mes = request.args.get('mes')

    resultado = CarteraService.get_top_10_acreditados_capital_vencido(sucursal=sucursal,anio=anio,mes=mes)
    return jsonify(resultado)
@api.route('/cartera/get_top_20_acreditados_numero_creditos')
def get_top_20_acreditados_numero_creditos():
    sucursal = request.args.get('sucursal', 'all')
    anio = request.args.get('anio')
    mes = request.args.get('mes')

    resultado = CarteraService.get_top_20_acreditados_numero_creditos(sucursal=sucursal,anio=anio,mes=mes)
    return jsonify(resultado)
@api.route('/cartera/get_ranking_creditos_mayor_antiguedad_pago')
def get_ranking_creditos_mayor_antiguedad_pago():
    datos = CarteraService.get_ranking_creditos_mayor_antiguedad_pago(
        sucursal=request.args.get('sucursal', 'all'),
        anio=request.args.get('anio'),
        mes=request.args.get('mes'),
        limite=request.args.get('limite', 20, type=int)
    )
    return jsonify(datos)
"""
    Captación
"""
@api.route('/captacion/years')
def get_years_captacion():
    sucursal = request.args.get('sucursal')
    meses = (FilterService.get_available_years_captacion(sucursal))
    return jsonify(meses)
@api.route('/months_captacion')
def get_months_captacion():
    anio = request.args.get('anio',type=int)
    sucursal = request.args.get('sucursal')
    meses = (FilterService.get_available_months_captacion(sucursal,anio))
    return jsonify(meses)
@api.route('/captacion/kpis')
def captacion_kpis():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    data = CaptacionService.get_general_kpis(sucursal,anio,mes)
    return jsonify(data)
@api.route('/captacion/evolution-chart')
def captacion_evolution_chart():
    anio = request.args.get('anio',type=int)
    sucursal = request.args.get('sucursal')
    data = CaptacionService.get_evolution_chart(sucursal,anio)
    return jsonify(data)
@api.route('/captacion/producto-chart')
def captacion_producto_chart():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    data = CaptacionService.get_producto_chart(sucursal, anio,mes)

    return jsonify(data)
@api.route('/captacion/sucursal-chart')
def captacion_sucursal_chart():
    anio = request.args.get('anio',type=int)
    sucursal = request.args.get('sucursal')
    mes = request.args.get('mes')
    data = CaptacionService.get_sucursal_chart(sucursal,anio,mes)
    return jsonify(data)
@api.route('/captacion/tipo-socio-chart')
def captacion_tipo_socio_chart():
    sucursal = request.args.get('sucursal')
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    data = CaptacionService.get_tipo_socio_chart(sucursal,anio,mes)

    return jsonify(data)
@api.route('/captacion/get_top_ahorradores')
def captacion_get_top_ahorradores():
    anio = request.args.get('anio',type=int)
    mes = request.args.get('mes')
    sucursal = request.args.get('sucursal')
    data = CaptacionService.get_top_ahorradores(sucursal,anio,mes)

    return jsonify(data)
@api.route('/captacion/get_ahorradores_por_sucursal_chart')
def get_ahorradores_por_sucursal_chart():
    anio = request.args.get('anio',type=int)
    sucursal = request.args.get('sucursal')
    mes = request.args.get('mes')
    data = CaptacionService.get_ahorradores_por_sucursal_chart(sucursal,anio,mes)
    return jsonify(data)
@api.route('/captacion/get_composicion_producto')
def get_composicion_producto():
    datos = CaptacionService.get_composicion_captacion_producto(
        sucursal=request.args.get('sucursal', 'all'),
        anio=request.args.get('anio'),
        mes=request.args.get('mes')
    )
    return jsonify(datos)
@api.route('/captacion/get_variacion_mensual')
def get_variacion_mensual():
    datos = CaptacionService.get_variacion_mensual_captacion(
        sucursal=request.args.get('sucursal', 'all'),
        anio=request.args.get('anio')
    )
    return jsonify(datos)
@api.route('/captacion/get_evolucion_socios_ahorradores')
def get_evolucion_socios_ahorradores():
    datos = CaptacionService.get_evolucion_socios_ahorradores(
        sucursal=request.args.get('sucursal', 'all'),
        anio=request.args.get('anio'),
        mes=request.args.get('mes')
    )
    return jsonify(datos)
@api.route('/captacion/get_evolucion_numero_cuentas')
def get_evolucion_numero_cuentas():
    datos = CaptacionService.get_evolucion_numero_cuentas(
        sucursal=request.args.get('sucursal', 'all'),
        anio=request.args.get('anio'),
        mes=request.args.get('mes')
    )
    return jsonify(datos)
@api.route('/captacion/get_numero_cuentas_por_sucursal')
def get_numero_cuentas_por_sucursal():
    datos = CaptacionService.get_numero_cuentas_por_sucursal(sucursal=request.args.get('sucursal', 'all'),anio=request.args.get('anio'),mes=request.args.get('mes'))
    return jsonify(datos)
@api.route('/captacion/get_top_socios_por_numero_cuentas')
def get_top_socios_por_numero_cuentas():
    datos = CaptacionService.get_top_socios_por_numero_cuentas(
        sucursal=request.args.get('sucursal', 'all'),
        anio=request.args.get('anio'),
        mes=request.args.get('mes', 'all')
    )
    return jsonify(datos)
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
@api.route('/socios/escolaridad-chart')
def socios_escolaridad_chart():

    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_escolaridad_chart(anio,mes))
@api.route('/socios/codigopostal-chart')
def socios_codigopostal_chart():

    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_codigopostal_chart(anio,mes))
@api.route('/socios/localidad-chart')
def socios_localidad_chart():

    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_localidad_chart(anio,mes))
@api.route('/socios/municipio-chart')
def socios_municipio_chart():

    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_municipio_chart(anio,mes))
@api.route('/socios/get_kpis_productos')
def get_kpis_productos():
    sucursal=request.args.get('sucursal')
    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')

    return jsonify(SociosService.get_kpis_productos(sucursal,anio,mes))
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
@api.route('/cartera/get_morosidad_por_sucursal')
def get_morosidad_por_sucursal():
    sucursal=request.args.get('sucursal')
    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')
    return jsonify(CarteraService.get_morosidad_por_sucursal(sucursal,anio, mes))
@api.route('/cartera/get_morosidad_por_producto')
def get_morosidad_por_producto():
    sucursal=request.args.get('sucursal')
    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')
    return jsonify(CarteraService.get_morosidad_por_producto(sucursal,anio,mes))
@api.route('/cartera/get_distribucion_dias_mora')
def get_distribucion_dias_mora():#consumo
    sucursal=request.args.get('sucursal')
    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')
    return jsonify(CarteraService.get_distribucion_dias_mora(sucursal,anio,mes))#consumo
@api.route('/cartera/get_cantidad_creditos_por_dias_mora')
def get_cantidad_creditos_por_dias_mora():
    sucursal=request.args.get('sucursal')
    anio=request.args.get('anio',type=int)
    mes=request.args.get('mes')
    return jsonify(CarteraService.get_cantidad_creditos_por_dias_mora(sucursal, anio,mes))    
@api.route('/cartera/get_morosidad_anual')
def get_morosidad_anual():
    sucursal=request.args.get('sucursal')
    anio=request.args.get('anio',type=int)
    return jsonify(CarteraService.get_morosidad_anual(sucursal, anio))    
