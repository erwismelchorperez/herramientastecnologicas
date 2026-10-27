from sqlalchemy import func, desc, case, distinct
from app import db
from app.models.creditos import Credito
from app.services.filter_service import FilterService
from app.utils.months import month_case
from app.utils.formatters import format_currency_short
from collections import defaultdict
class CarteraService:

    @staticmethod
    def get_latest_period():
        mes_orden = month_case(Credito.mes)
        return db.session.query(Credito.anio,Credito.mes).order_by(Credito.anio.desc(),mes_orden.desc()).first()
    @staticmethod
    def get_general_kpis(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        filtros = [
            Credito.anio == anio,
            Credito.mes == mes
        ]

        if sucursal and sucursal != 'all':
            filtros.append(Credito.sucursal == sucursal)

        morosidad_data = db.session.query(
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(*filtros).first()

        capital_vigente = float(morosidad_data.vigente or 0)
        capital_vencido = float(morosidad_data.vencido or 0)
        total_cartera = capital_vigente + capital_vencido
        morosidad = (capital_vencido / total_cartera * 100) if total_cartera > 0 else 0

        creditos_vigentes = db.session.query(
            func.count(Credito.vigente_vencido)
        ).filter(
            *filtros,
            func.upper(func.trim(Credito.vigente_vencido)) == 'VIGENTE'
        ).scalar()
        creditos_vencidos = db.session.query(
            func.count(Credito.vigente_vencido)
        ).filter(
            *filtros,
            func.upper(func.trim(Credito.vigente_vencido)) == 'VENCIDO'
        ).scalar()
        creditos_reestructurados = db.session.query(
            func.count(Credito.renovado_reestructurado_normal)
        ).filter(
            *filtros,
            func.upper(func.trim(Credito.renovado_reestructurado_normal)) == 'RE-ESTRUCTURADO X CONTINGENCIA'
        ).scalar()
        credito_promedio = db.session.query(
            func.avg(Credito.monto_original)
        ).filter(*filtros).scalar()
        credito_promedio = float(credito_promedio or 0)

        return {
            'cartera_total': format_currency_short(total_cartera),
            'cartera_total_title': total_cartera,
            'capital_vigente': format_currency_short(capital_vigente),
            'capital_vigente_title': capital_vigente,
            'capital_vencido': format_currency_short(capital_vencido),
            'capital_vencido_title': capital_vencido,
            'morosidad': morosidad,
            'creditos_vigentes': int(creditos_vigentes or 0),
            'creditos_vencidos': int(creditos_vencidos or 0),
            'creditos_reestructurados': int(creditos_reestructurados or 0),
            'credito_promedio': format_currency_short(credito_promedio),
            'credito_promedio_title': credito_promedio,
            'ultimo_anio': anio,
            'ultimo_mes': mes
        }
    @staticmethod
    def get_evolution_chart(sucursal='all', anio=None):
        print("get_evolution_chart      ",sucursal)
        if not anio:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio

        mes_orden = month_case(Credito.mes)
        query = db.session.query(
            Credito.mes,
            func.sum(
                Credito.capital_vigente
            ).label('total')
        ).filter(
            Credito.anio == anio
        )

        if sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        datos = query.group_by(
            Credito.mes
        ).order_by(
            mes_orden.asc()
        ).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.mes.upper())
            series.append(float(row.total))

        return {'chart_labels': labels,'chart_series': series}
    @staticmethod
    def get_product_chart(anio=None, mes=None):
        # ====================================
        # ÚLTIMO PERIODO
        # ====================================
        if not anio or not mes:
            ultimo_periodo = (CarteraService.get_latest_period())
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes
        # ====================================
        # QUERY
        # ====================================
        datos = db.session.query(
            Credito.producto_credito,
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
            Credito.producto_credito
        ).all()
        # ====================================
        # ARMAR SERIES
        # ====================================
        labels = []
        vigente = []
        vencido = []
        for row in datos:
            labels.append(row.producto_credito)
            vigente.append(float(row.vigente or 0))
            vencido.append(float(row.vencido or 0))
        return {
            'labels': labels,
            'vigente': vigente,
            'vencido': vencido
        }
    @staticmethod
    def get_clasificacion_chart(anio=None, mes=None):
        # ====================================
        # ÚLTIMO PERIODO
        # ====================================
        if not anio or not mes:
            ultimo_periodo = (CarteraService.get_latest_period())
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes
        # ====================================
        # QUERY
        # ====================================
        datos = db.session.query(
            Credito.clasificacion_credito,
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
            Credito.clasificacion_credito
        ).all()
        # ====================================
        # ARMAR SERIES
        # ====================================
        labels = []
        vigente = []
        vencido = []
        for row in datos:
            labels.append(row.clasificacion_credito)
            vigente.append(float(row.vigente or 0))
            vencido.append(float(row.vencido or 0))
        return {
            'labels': labels,
            'vigente': vigente,
            'vencido': vencido
        }
    @staticmethod
    def get_branch_chart(anio=None, mes=None):
        # ====================================
        # ÚLTIMO PERIODO
        # ====================================
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes
        # ====================================
        # QUERY
        # ====================================
        datos = db.session.query(
            Credito.sucursal,
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
            Credito.sucursal
        ).order_by(
            Credito.sucursal.asc()
        ).all()
        # ====================================
        # SERIES
        # ====================================
        labels = []
        vigente = []
        vencido = []

        for row in datos:
            labels.append(row.sucursal)
            vigente.append(float(row.vigente or 0))
            vencido.append(float(row.vencido or 0))

        return {
            'labels': labels,
            'vigente': vigente,
            'vencido': vencido
        }
    @staticmethod
    def get_clasificacion_statuschart(sucursal='all',anio=None,mes=None):
        # ====================================
        # ÚLTIMO PERIODO
        # ====================================
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes
        # ====================================
        # QUERY
        # ====================================
        query = db.session.query(
            Credito.clasificacion_credito,
            func.count(
                Credito.numero_credito
            ).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        )

        # ====================================
        # FILTRO SUCURSAL
        # ====================================
        if sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        # ====================================
        # AGRUPACIÓN
        # ====================================

        datos = query.group_by(Credito.clasificacion_credito).all()

        # ====================================
        # SERIES
        # ====================================

        labels = []

        series = []

        for row in datos:

            labels.append(row.clasificacion_credito)

            series.append(int(row.total))

        return {

            'labels': labels,

            'series': series

        }
    @staticmethod
    def get_sucursal_count_chart(sucursal='all', anio=None, mes=None):
        # ====================================
        # ÚLTIMO PERIODO
        # ====================================
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        # ====================================
        # QUERY
        # ====================================
        query = db.session.query(
            Credito.sucursal,
            func.count(
                Credito.numero_credito
            ).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        )
        # ====================================
        # FILTRO SUCURSAL
        # ====================================
        if sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        # ====================================
        # AGRUPACIÓN
        # ====================================
        datos = query.group_by(
            Credito.sucursal
        ).order_by(
            func.count(
                Credito.numero_credito
            ).desc()
        ).all()

        # ====================================
        # SERIES
        # ====================================
        labels = []
        series = []

        for row in datos:
            labels.append(row.sucursal)
            series.append(int(row.total))

        return {
            'labels': labels,
            'series': series
        }
    @staticmethod
    def get_sucursal_vigente_chart(sucursal='all',anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Credito.sucursal,
            func.sum(Credito.capital_vigente).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes,
            func.upper(func.trim(Credito.vigente_vencido)) == 'VIGENTE'
        )

        if sucursal != 'all':
            query = query.filter(
                Credito.sucursal == sucursal
            )

        datos = query.group_by(
            Credito.sucursal
        ).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.sucursal)
            series.append(float(row.total or 0))

        return {
            'chart_labels': labels,
            'chart_series': series
        }
    @staticmethod
    def get_sucursal_vigente_anual_chart(mes=None):
        if not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            mes = ultimo_periodo.mes
        datos = db.session.query(
            Credito.anio,
            Credito.sucursal,
            func.sum(Credito.capital_vigente).label('total')
        ).filter(
            Credito.mes == mes,
            func.upper(func.trim(Credito.vigente_vencido)) == 'VIGENTE'
        ).group_by(
            Credito.anio,
            Credito.sucursal
        ).order_by(
            Credito.anio
        ).all()

        # años existentes
        anios = sorted(list({
            row.anio for row in datos
        }))

        # sucursales existentes
        sucursales = sorted(list({
            row.sucursal for row in datos
        }))

        # estructura temporal
        valores = defaultdict(dict)

        for row in datos:
            valores[row.sucursal][row.anio] = float(row.total or 0)

        series = []

        for sucursal in sucursales:

            data = []

            for anio in anios:
                data.append(
                    valores[sucursal].get(anio, 0)
                )

            series.append({
                "name": sucursal,
                "data": data
            })

        return {
            "categories": anios,
            "series": series
        }
    @staticmethod
    def get_sucursal_vencido_chart(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Credito.sucursal,
            func.sum(Credito.capital_vencido).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes,
            func.upper(func.trim(Credito.vigente_vencido)) == 'VENCIDO'
        )

        if sucursal != 'all':
            query = query.filter(
                Credito.sucursal == sucursal
            )

        datos = query.group_by(
            Credito.sucursal
        ).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.sucursal)
            series.append(float(row.total or 0))

        return {
            'chart_labels': labels,
            'chart_series': series
    }
    @staticmethod
    def get_top_productos_vigente_chart(sucursal='all',anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Credito.producto_credito,
            func.sum(Credito.capital_vigente).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        )

        if sucursal != 'all':
            query = query.filter(
                Credito.sucursal == sucursal
            )

        datos = query.group_by(
            Credito.producto_credito
        ).order_by(
            desc('total')
        ).limit(10).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.producto_credito)
            series.append(float(row.total or 0))

        return {
            'chart_labels': labels,
            'chart_series': series
        }
    @staticmethod
    def get_productos_table(anio=None,mes=None, page=1, per_page=10):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        base_query = db.session.query(
            Credito.producto_credito.label('producto'),
            func.sum(
                Credito.capital_vigente
            ).label('capital_vigente'),
            func.sum(
                Credito.capital_vencido
            ).label('capital_vencido'),
            func.count(
                Credito.numero_credito
            ).label('numero_creditos')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
            Credito.producto_credito
        )
        total=base_query.count()
        datos=base_query.order_by(
            desc('capital_vigente')
        ).offset(
            (page-1)*per_page
        ).limit(
            per_page
        ).all()
        
        resultado = []
        for row in datos:
            resultado.append({
                'producto': row.producto,
                'capital_vigente': float(row.capital_vigente or 0),
                'capital_vencido': float(row.capital_vencido or 0),
                'numero_creditos': int(row.numero_creditos or 0)
            })
        return {
            'data':resultado,
            'page':page,
            'per_page':per_page,
            'total':total,
            'total_pages':(
                total+per_page-1
            )//per_page
        }
    @staticmethod
    def get_sucursal_vigente_vencido_chart(anio=None, mes=None):

        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        datos = db.session.query(
            Credito.sucursal,
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
            Credito.sucursal
        ).order_by(
            Credito.sucursal
        ).all()

        categorias = []
        vigente = []
        vencido = []

        for row in datos:
            categorias.append(row.sucursal)

            vigente.append(float(row.vigente or 0))
            vencido.append(float(row.vencido or 0))

        return {
            "categories": categorias,
            "series": [
                {
                    "name": "Capital Vigente",
                    "data": vigente
                },
                {
                    "name": "Capital Vencido",
                    "data": vencido
                }
            ]
        }
    @staticmethod
    def get_morosidad_por_sucursal(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Credito.sucursal.label('sucursal'),
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        )

        if sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        morosidad_data = query.group_by(
            Credito.sucursal
        ).order_by(
            Credito.sucursal
        ).all()

        resultados = []

        for dato in morosidad_data:
            capital_vigente = float(dato.vigente or 0)
            capital_vencido = float(dato.vencido or 0)
            total_cartera = capital_vigente + capital_vencido

            if total_cartera > 0:
                morosidad = (capital_vencido / total_cartera) * 100
            else:
                morosidad = 0

            resultados.append({
                'sucursal': dato.sucursal,
                'capital_vigente': capital_vigente,
                'capital_vencido': capital_vencido,
                'total_cartera': total_cartera,
                'morosidad': morosidad
            })

        return {
            'anio': anio,
            'mes': mes,
            'data': resultados
        }
    @staticmethod
    def get_morosidad_por_producto(sucursal='all',anio=None, mes=None ):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Credito.producto_credito.label('producto'),
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        )

        if sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        morosidad_data = query.group_by(
            Credito.producto_credito
        ).order_by(
            Credito.producto_credito
        ).all()

        resultados = []

        for dato in morosidad_data:
            capital_vigente = float(dato.vigente or 0)
            capital_vencido = float(dato.vencido or 0)
            total_cartera = capital_vigente + capital_vencido

            if total_cartera > 0:
                morosidad = (capital_vencido / total_cartera) * 100
            else:
                morosidad = 0

            resultados.append({
                'producto': dato.producto,
                'capital_vigente': capital_vigente,
                'capital_vencido': capital_vencido,
                'total_cartera': total_cartera,
                'morosidad': round(morosidad, 2)
            })

        return {
            'anio': anio,
            'mes': mes,
            'data': resultados
        }
    @staticmethod
    def get_distribucion_dias_mora(sucursal='all', anio=None, mes=None):
        """
        Función para obtener los días de mora para la cartera de consumo.
        """
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        rango_mora = case(
            (Credito.dias_mora_cartera == 0, '0 días'),
            (Credito.dias_mora_cartera.between(1, 7), '1-7 días'),
            (Credito.dias_mora_cartera.between(8, 30), '8-30 días'),
            (Credito.dias_mora_cartera.between(31, 60), '31-60 días'),
            (Credito.dias_mora_cartera.between(61, 90), '61-90 días'),
            (Credito.dias_mora_cartera.between(91, 120), '91-120 días'),
            (Credito.dias_mora_cartera.between(121, 180), '121-180 días'),
            (Credito.dias_mora_cartera > 181, '+180 días'),
            else_='Sin clasificar'
        ).label('rango')

        query = db.session.query(
            rango_mora,
            func.sum(Credito.capital_vencido).label('capital_vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        )

        if sucursal != 'all':
            query = query.filter(
                Credito.sucursal == sucursal
            )

        distribucion_data = query.group_by(
            rango_mora
        ).all()

        orden_rangos = {
            '0 días': 1,
            '1-7 días': 2,
            '8-30 días': 3,
            '31-60 días': 4,
            '61-90 días': 5,
            '91-120 días': 6,
            '121-180 días': 7,
            '+180 días': 8
        }

        resultados = []

        for dato in distribucion_data:
            capital_vencido = float(dato.capital_vencido or 0)

            resultados.append({
                'rango': dato.rango,
                'capital_vencido': capital_vencido
            })

        resultados.sort(
            key=lambda item: orden_rangos.get(
                item['rango'],
                99
            )
        )

        return {
            'anio': anio,
            'mes': mes,
            'data': resultados
        }
    @staticmethod
    def get_cantidad_creditos_por_dias_mora(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        rango_mora = case(
            (Credito.dias_mora_cartera == 0, '0 días'),
            (Credito.dias_mora_cartera.between(1, 7), '1-7 días'),
            (Credito.dias_mora_cartera.between(8, 30), '8-30 días'),
            (Credito.dias_mora_cartera.between(31, 60), '31-60 días'),
            (Credito.dias_mora_cartera.between(61, 90), '61-90 días'),
            (Credito.dias_mora_cartera.between(91, 120), '91-120 días'),
            (Credito.dias_mora_cartera.between(121, 180), '121-180 días'),
            (Credito.dias_mora_cartera > 181, '+180 días'),
            else_='Sin clasificar'
        ).label('rango')

        query = db.session.query(
            rango_mora,
            func.count(Credito.id).label('cantidad_creditos')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        )

        if sucursal != 'all':
            query = query.filter(
                Credito.sucursal == sucursal
            )

        datos = query.group_by(
            rango_mora
        ).all()

        orden_rangos = {
            '0 días': 1,
            '1-7 días': 2,
            '8-30 días': 3,
            '31-60 días': 4,
            '61-90 días': 5,
            '91-120 días': 6,
            '121-180 días': 7,
            '+180 días': 8
        }

        resultados = [
            {
                'rango': dato.rango,
                'cantidad_creditos': int(dato.cantidad_creditos or 0)
            }
            for dato in datos
        ]

        resultados.sort(
            key=lambda item: orden_rangos.get(item['rango'], 99)
        )

        return {
            'anio': anio,
            'mes': mes,
            'data': resultados
        }
    @staticmethod
    def get_morosidad_anual(sucursal='all', anio=None):
        if not anio:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio

        mes_orden = month_case(Credito.mes)

        query = db.session.query(
            Credito.mes.label('mes'),
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        datos = query.group_by(
            Credito.mes
        ).order_by(
            mes_orden
        ).all()

        meses = []
        morosidad_mensual = []

        nombres_meses = {
            'ene': 'Ene', 'feb': 'Feb', 'mar': 'Mar',
            'abr': 'Abr', 'may': 'May', 'jun': 'Jun',
            'jul': 'Jul', 'ago': 'Ago', 'sep': 'Sep',
            'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dic'
        }

        for fila in datos:
            capital_vigente = float(fila.vigente or 0)
            capital_vencido = float(fila.vencido or 0)
            total_cartera = capital_vigente + capital_vencido

            morosidad = (
                capital_vencido / total_cartera * 100
                if total_cartera > 0 else 0
            )

            meses.append(nombres_meses.get(fila.mes, fila.mes))
            morosidad_mensual.append(round(morosidad, 2))

        return {
            'chart_labels': meses,
            'chart_series': morosidad_mensual
        }
    @staticmethod
    def get_monto_original_por_producto_mes(sucursal='all', anio=None):
        if not anio:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio

        mes_orden = month_case(Credito.mes)

        query = db.session.query(
            Credito.producto_credito,
            Credito.mes,
            func.sum(Credito.monto_original).label('total')
        ).filter(
            Credito.anio == anio
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        datos = query.group_by(
            Credito.producto_credito,
            Credito.mes
        ).order_by(
            mes_orden,
            Credito.producto_credito
        ).all()

        # Meses existentes
        orden_meses = {'ene': 1, 'feb': 2, 'mar': 3,'abr': 4, 'may': 5, 'jun': 6,'jul': 7, 'ago': 8, 'sep': 9,'oct': 10, 'nov': 11, 'dic': 12}

        meses = sorted(
            {row.mes for row in datos},
            key=lambda mes: orden_meses.get(
                str(mes).strip().lower(), 99
            )
        )

        # Productos existentes
        productos = sorted({
            row.producto_credito for row in datos
            if row.producto_credito is not None
        })

        # Estructura temporal
        valores = defaultdict(dict)

        for row in datos:
            valores[row.producto_credito][row.mes] = float(row.total or 0)

        series = []

        for producto in productos:
            data = [
                valores[producto].get(mes, 0)
                for mes in meses
            ]

            series.append({
                'name': producto,
                'data': data
            })

        nombres_meses = {
            'ene': 'Ene', 'feb': 'Feb', 'mar': 'Mar',
            'abr': 'Abr', 'may': 'May', 'jun': 'Jun',
            'jul': 'Jul', 'ago': 'Ago', 'sep': 'Sep',
            'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dic'
        }

        return {
            'categories': [
                nombres_meses.get(mes, mes) for mes in meses
            ],
            'series': series
        }
    @staticmethod
    def get_evolutionvigvenc_chart(sucursal='all', anio=None):
        if not anio:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio

        mes_orden = month_case(Credito.mes)

        query = db.session.query(
            Credito.mes,
            func.sum(Credito.capital_vigente).label('vigente'),
            func.sum(Credito.capital_vencido).label('vencido')
        ).filter(
            Credito.anio == anio
        )

        if sucursal and sucursal != 'all':
            query = query.filter(
                Credito.sucursal == sucursal
            )

        datos = query.group_by(
            Credito.mes
        ).order_by(
            mes_orden.asc()
        ).all()

        labels = []
        capital_vigente = []
        capital_vencido = []

        for row in datos:
            labels.append(row.mes.upper())
            capital_vigente.append(float(row.vigente or 0))
            capital_vencido.append(float(row.vencido or 0))

        return {
            'chart_labels': labels,
            'chart_series': [
                {
                    'name': 'Capital vigente',
                    'data': capital_vigente
                },
                {
                    'name': 'Capital vencido',
                    'data': capital_vencido
                }
            ]
        }
    @staticmethod
    def get_colocacion_mensual(sucursal='all', anio=None):
        query = db.session.query(
            func.extract('month', Credito.fecha_otorgamiento).label('mes'),
            func.sum(Credito.monto_original).label('colocacion')
        ).filter(
            Credito.fecha_otorgamiento.isnot(None)
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(
                func.extract('year', Credito.fecha_otorgamiento) == int(anio)
            )

        resultados = query.group_by(
            func.extract('month', Credito.fecha_otorgamiento)
        ).order_by(
            func.extract('month', Credito.fecha_otorgamiento)
        ).all()

        meses = FilterService.get_available_months(anio=anio)
        print("meses   ",meses)
        #meses = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN','JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']

        colocacion_mensual = {mes: 0 for mes in range(1, len(meses) + 1)}
        print("Colocacion mensual   ",colocacion_mensual)

        for mes, colocacion in resultados:
            colocacion_mensual[int(mes)] = float(colocacion or 0)

        return {
            'chart_labels': meses,
            'chart_series': [
                {
                    'name': 'Colocación',
                    'data': [colocacion_mensual[mes] for mes in range(1, len(meses) + 1)]
                }
            ]
        }
    @staticmethod
    def get_creditos_otorgados_mensual(sucursal='all', anio=None):
        query = db.session.query(
            func.extract('month', Credito.fecha_otorgamiento).label('mes'),
            func.count(Credito.numero_credito).label('total_creditos')
        ).filter(
            Credito.fecha_otorgamiento.isnot(None)
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(
                func.extract('year', Credito.fecha_otorgamiento) == int(anio)
            )

        resultados = query.group_by(
            func.extract('month', Credito.fecha_otorgamiento)
        ).order_by(
            func.extract('month', Credito.fecha_otorgamiento)
        ).all()

        meses = FilterService.get_available_months(anio=anio)
        creditos_mensuales = {mes: 0 for mes in range(1, len(meses) + 1)}

        for mes, total in resultados:
            mes = int(mes)
            if mes in creditos_mensuales:
                creditos_mensuales[mes] = int(total or 0)

        return {
            'chart_labels': meses,
            'chart_series': [
                {
                    'name': 'Créditos otorgados',
                    'data': [creditos_mensuales[mes] for mes in range(1, len(meses) + 1)]
                }
            ]
        }
    @staticmethod
    def get_montos_por_tipo_garantia(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            func.coalesce(func.sum(Credito.monto_garantia_liquida), 0).label('garantia_liquida'),
            func.coalesce(func.sum(Credito.monto_garantia_prendaria), 0).label('garantia_prendaria'),
            func.coalesce(func.sum(Credito.monto_garantia_hipotecaria), 0).label('garantia_hipotecaria')
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(Credito.anio == int(anio))

        if mes:
            query = query.filter(Credito.mes == mes)

        liquida, prendaria, hipotecaria = query.one()

        return {
            'chart_labels': [
                'Garantía líquida',
                'Garantía prendaria',
                'Garantía hipotecaria'
            ],
            'chart_series': [
                {
                    'name': 'Monto por tipo de garantía',
                    'data': [
                        float(liquida or 0),
                        float(prendaria or 0),
                        float(hipotecaria or 0)
                    ]
                }
            ]
        }
    @staticmethod
    def get_garantias_por_sucursal(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            Credito.sucursal.label('sucursal'),
            func.coalesce(func.sum(Credito.monto_garantia_liquida), 0).label('garantia_liquida'),
            func.coalesce(func.sum(Credito.monto_garantia_prendaria), 0).label('garantia_prendaria'),
            func.coalesce(func.sum(Credito.monto_garantia_hipotecaria), 0).label('garantia_hipotecaria')
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(Credito.anio == int(anio))

        if mes:
            query = query.filter(Credito.mes == mes)

        resultados = query.group_by(
            Credito.sucursal
        ).order_by(
            Credito.sucursal
        ).all()

        return {
            'chart_labels': [r.sucursal for r in resultados],
            'chart_series': [
                {
                    'name': 'Garantía líquida',
                    'data': [float(r.garantia_liquida or 0) for r in resultados]
                },
                {
                    'name': 'Garantía prendaria',
                    'data': [float(r.garantia_prendaria or 0) for r in resultados]
                },
                {
                    'name': 'Garantía hipotecaria',
                    'data': [float(r.garantia_hipotecaria or 0) for r in resultados]
                }
            ]
        }
    @staticmethod
    def get_eprc_por_sucursal(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            Credito.sucursal.label('sucursal'),
            func.coalesce(func.sum(Credito.eprc_para_parte_cubierta), 0).label('parte_cubierta'),
            func.coalesce(func.sum(Credito.eprc_para_parte_expuesta), 0).label('parte_expuesta'),
            func.coalesce(func.sum(Credito.eprc_intereses_cave), 0).label('intereses_cave')
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(Credito.anio == int(anio))

        if mes:
            query = query.filter(Credito.mes == mes)

        resultados = query.group_by(
            Credito.sucursal
        ).order_by(
            Credito.sucursal
        ).all()

        return {
            'chart_labels': [r.sucursal for r in resultados],
            'chart_series': [
                {
                    'name': 'EPRC parte cubierta',
                    'data': [float(r.parte_cubierta or 0) for r in resultados]
                },
                {
                    'name': 'EPRC parte expuesta',
                    'data': [float(r.parte_expuesta or 0) for r in resultados]
                },
                {
                    'name': 'EPRC intereses CAVE',
                    'data': [float(r.intereses_cave or 0) for r in resultados]
                }
            ]
        }
    @staticmethod
    def get_eprc_por_clasificacion(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            Credito.clasificacion_credito.label('clasificacion'),
            func.coalesce(func.sum(Credito.eprc_para_parte_cubierta), 0).label('parte_cubierta'),
            func.coalesce(func.sum(Credito.eprc_para_parte_expuesta), 0).label('parte_expuesta'),
            func.coalesce(func.sum(Credito.eprc_intereses_cave), 0).label('intereses_cave')
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(Credito.anio == int(anio))

        if mes:
            query = query.filter(Credito.mes == mes)

        resultados = query.group_by(
            Credito.clasificacion_credito
        ).order_by(
            Credito.clasificacion_credito
        ).all()

        return {
            'chart_labels': [
                r.clasificacion or 'Sin especificar'
                for r in resultados
            ],
            'chart_series': [
                {
                    'name': 'EPRC parte cubierta',
                    'data': [float(r.parte_cubierta or 0) for r in resultados]
                },
                {
                    'name': 'EPRC parte expuesta',
                    'data': [float(r.parte_expuesta or 0) for r in resultados]
                },
                {
                    'name': 'EPRC intereses CAVE',
                    'data': [float(r.intereses_cave or 0) for r in resultados]
                }
            ]
        }
    @staticmethod
    def get_top_10_acreditados_capital(sucursal='all', anio=None, mes=None):
        capital_total = (
            func.coalesce(Credito.capital_vigente, 0) +
            func.coalesce(Credito.capital_vencido, 0)
        )

        query = db.session.query(
            Credito.numero_socio_cliente.label('acreditado'),
            func.sum(capital_total).label('capital_total')
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(Credito.anio == int(anio))

        if mes:
            query = query.filter(Credito.mes == mes)

        resultados = query.group_by(
            Credito.numero_socio_cliente
        ).order_by(
            func.sum(capital_total).desc()
        ).limit(10).all()

        return {
            'chart_labels': [
                r.acreditado or 'Sin especificar'
                for r in resultados
            ],
            'chart_series': [
                {
                    'name': 'Capital total',
                    'data': [
                        float(r.capital_total or 0)
                        for r in resultados
                    ]
                }
            ]
        }
    @staticmethod
    def get_top_10_acreditados_capital_vencido(sucursal='all', anio=None, mes=None):
        capital_vencido = func.coalesce(Credito.capital_vencido, 0)

        query = db.session.query(
            Credito.numero_socio_cliente.label('acreditado'),
            func.sum(capital_vencido).label('capital_vencido')
        )

        if sucursal and sucursal.lower() != 'all':
            query = query.filter(Credito.sucursal == sucursal)

        if anio:
            query = query.filter(Credito.anio == int(anio))

        if mes:
            query = query.filter(Credito.mes == mes)

        resultados = query.group_by(
            Credito.numero_socio_cliente
        ).order_by(
            func.sum(capital_vencido).desc()
        ).limit(10).all()

        return {
            'chart_labels': [
                r.acreditado or 'Sin especificar'
                for r in resultados
            ],
            'chart_series': [
                {
                    'name': 'Capital total',
                    'data': [
                        float(r.capital_vencido or 0)
                        for r in resultados
                    ]
                }
            ]
        }
    @staticmethod
    def get_top_20_acreditados_numero_creditos(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Credito.numero_socio_cliente.label('acreditado'),
            func.count(distinct(Credito.numero_credito)).label('numero_creditos')
        ).filter(
            Credito.numero_socio_cliente.isnot(None),
            Credito.numero_credito.isnot(None)
        )

        if sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)
        if anio:
            query = query.filter(Credito.anio == int(anio))
        if mes:
            query = query.filter(Credito.mes == mes)

        resultados = query.group_by(
            Credito.numero_socio_cliente
        ).order_by(
            func.count(distinct(Credito.numero_credito)).desc(),
            Credito.numero_socio_cliente.asc()
        ).limit(10).all()

        return {
            'chart_labels': [str(r.acreditado) for r in resultados],
            'chart_series': [{
                'name': 'Número de créditos',
                'data': [int(r.numero_creditos) for r in resultados]
            }]
        }
    @staticmethod
    def get_ranking_creditos_mayor_antiguedad_pago(sucursal='all', anio=None, mes=None, limite=20):

        query = db.session.query(
            Credito.numero_credito,
            Credito.numero_socio_cliente,
            func.max(Credito.dias_mora_cartera).label('dias_mora'),
            func.max(Credito.capital_vencido).label('capital_vencido'),
            func.max(Credito.capital_vigente).label('capital_vigente')
        ).filter(
            Credito.numero_credito.isnot(None),
            Credito.dias_mora_cartera.isnot(None)
        )

        if sucursal != 'all':
            query = query.filter(Credito.sucursal == sucursal)
        if anio:
            query = query.filter(Credito.anio == int(anio))
        if mes:
            query = query.filter(Credito.mes == mes)

        resultados = query.group_by(
            Credito.numero_credito,
            Credito.numero_socio_cliente
        ).order_by(
            func.max(Credito.dias_mora_cartera).desc()
        ).limit(limite).all()

        return {
            'chart_labels': [str(r.numero_credito) for r in resultados],
            'chart_series': [{
                'name': 'Días de mora',
                'data': [int(r.dias_mora or 0) for r in resultados]
            }],
            'detalle': [{
                'numero_credito': str(r.numero_credito),
                'numero_socio_cliente': str(r.numero_socio_cliente or ''),
                'dias_mora': int(r.dias_mora or 0),
                'capital_vencido': float(r.capital_vencido or 0),
                'capital_vigente': float(r.capital_vigente or 0)
            } for r in resultados]
        }
############################## 