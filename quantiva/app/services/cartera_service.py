from sqlalchemy import func, desc
from app import db
from app.models.creditos import Credito
from app.utils.months import month_case
from app.utils.formatters import format_currency_short
class CarteraService:

    @staticmethod
    def get_latest_period():
        mes_orden = month_case(Credito.mes)
        return db.session.query(Credito.anio,Credito.mes).order_by(Credito.anio.desc(),mes_orden.desc()).first()
    
    @staticmethod
    def get_general_kpis(anio=None, mes=None):

        if not anio or not mes:

            ultimo_periodo = CarteraService.get_latest_period()

            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes


        cartera_total = db.session.query(func.sum(Credito.capital_vigente)).filter(Credito.anio == anio,Credito.mes == mes).scalar()
        cartera_total = float(cartera_total or 0)

        morosidad_data = db.session.query(
            func.sum(
                Credito.capital_vigente
            ).label('vigente'),
            func.sum(
                Credito.capital_vencido
            ).label('vencido')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).first()

        capital_vigente = float(morosidad_data.vigente or 0)

        capital_vencido = float(morosidad_data.vencido or 0)

        total_cartera = (capital_vigente + capital_vencido)
        if total_cartera > 0:
            morosidad = ( capital_vencido / total_cartera) * 100
        else:
            morosidad = 0

        # ==========================
        # CRÉDITOS VIGENTES/VENCIDOS
        # ==========================
        creditos_vigentes = db.session.query(func.count(Credito.vigente_vencido)).filter(
            Credito.anio == anio,
            Credito.mes == mes,
            Credito.vigente_vencido == 'VIGENTE'
        ).scalar()

        creditos_vigentes = int(creditos_vigentes or 0)

        creditos_vencidos = db.session.query(func.count(Credito.vigente_vencido)).filter(
            Credito.anio == anio,
            Credito.mes == mes,
            Credito.vigente_vencido == 'VENCIDO'
        ).scalar()

        creditos_vencidos = int(creditos_vencidos or 0)

        creditos_reestructurados = db.session.query(
            func.count(Credito.renovado_reestructurado_normal)
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes,
            Credito.renovado_reestructurado_normal == 'RE-ESTRUCTURADO X CONTINGENCIA'
        ).scalar()

        creditos_reestructurados = int(creditos_reestructurados or 0)

        credito_promedio = db.session.query(
            func.avg(Credito.monto_original)
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).scalar()

        credito_promedio = float(credito_promedio or 0)

        return {
            'cartera_total': format_currency_short(total_cartera),
            'cartera_total_title': total_cartera,
            'capital_vigente': format_currency_short(capital_vigente),
            'capital_vigente_title': capital_vigente,
            'capital_vencido': format_currency_short(capital_vencido),
            'capital_vencido_title': capital_vencido,
            'morosidad': morosidad,
            'creditos_vigentes': creditos_vigentes,
            'creditos_vencidos': creditos_vencidos,
            'creditos_reestructurados': creditos_reestructurados,
            'credito_promedio': format_currency_short(credito_promedio),
            'credito_promedio_title': credito_promedio,
            'ultimo_anio': anio,
            'ultimo_mes': mes
        }
    @staticmethod
    def get_evolution_chart(anio= None):
        if not anio:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio

        mes_orden = month_case(Credito.mes)
        datos = db.session.query(
            Credito.mes,
            func.sum(
                Credito.capital_vigente
            ).label('total')
        ).filter(
            Credito.anio == anio
        ).group_by(
            Credito.mes
        ).order_by(
            mes_orden.asc()
        ).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.mes.upper())
            series.append(float(row.total))
        return {
            'chart_labels': labels,
            'chart_series': series
        }
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
    def get_clasificacion_statuschart(anio=None, mes=None):
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
            func.count(
                Credito.numero_credito
            ).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
            Credito.clasificacion_credito
        ).all()
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
    def get_sucursal_count_chart(anio=None, mes=None):
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
            func.count(Credito.numero_credito).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
            Credito.sucursal
        ).order_by(
            func.count(Credito.numero_credito).desc()
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
    def get_sucursal_vigente_chart(anio=None,mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        datos = db.session.query(
            Credito.sucursal,
            func.sum(Credito.capital_vigente).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes,
            Credito.vigente_vencido == 'VIGENTE'
        ).group_by(
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
    def get_sucursal_vencido_chart(anio=None,mes=None):

        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        datos = db.session.query(
            Credito.sucursal,
            func.sum(Credito.capital_vencido).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes,
            Credito.vigente_vencido == 'VENCIDO'
        ).group_by(
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
    def get_top_productos_vigente_chart(anio=None,mes=None):
        if not anio or not mes:
            ultimo_periodo = CarteraService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        datos = db.session.query(
            Credito.producto_credito,
            func.sum(Credito.capital_vigente).label('total')
        ).filter(
            Credito.anio == anio,
            Credito.mes == mes
        ).group_by(
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