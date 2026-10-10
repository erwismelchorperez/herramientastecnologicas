from sqlalchemy import func, extract, desc, or_
from app import db
from app.models.captacion import Captacion
from app.utils.months import month_case
from app.utils.months import month_number
from app.utils.formatters import format_currency_short
class CaptacionService:
    @staticmethod
    def get_latest_period():
        mes_orden = month_case(Captacion.mes)
        return db.session.query(Captacion.anio,Captacion.mes).order_by(Captacion.anio.desc(),mes_orden.desc()).first()
    @staticmethod
    def get_general_kpis(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        filtros = [
            Captacion.anio == anio,
            Captacion.mes == mes
        ]

        if sucursal and sucursal != 'all':
            filtros.append(Captacion.sucursal == sucursal)

        captacion_total = db.session.query(
            func.sum(Captacion.saldo_total_cierre_mes)
        ).filter(*filtros).scalar()
        captacion_total = float(captacion_total or 0)

        filtros_captado = [
            extract('year', Captacion.fecha_apertura_contratacion) == anio,
            extract('month', Captacion.fecha_apertura_contratacion) == month_number(mes)
        ]
        if sucursal and sucursal != 'all':
            filtros_captado.append(Captacion.sucursal == sucursal)

        capital_captado = db.session.query(
            func.sum(Captacion.saldo_total_cierre_mes)
        ).filter(*filtros_captado).scalar()
        capital_captado = float(capital_captado or 0)

        filtros_retiros = [
            extract('year', Captacion.fecha_retiro_ultimo) == anio,
            extract('month', Captacion.fecha_retiro_ultimo) == month_number(mes)
        ]
        if sucursal and sucursal != 'all':
            filtros_retiros.append(Captacion.sucursal == sucursal)

        retiros_mes = db.session.query(
            func.count(Captacion.numero_socio)
        ).filter(*filtros_retiros).scalar()
        retiros_mes = int(retiros_mes or 0)

        filtros_depositos = [
            extract('year', Captacion.fecha_deposito_ultimo) == anio,
            extract('month', Captacion.fecha_deposito_ultimo) == month_number(mes)
        ]
        if sucursal and sucursal != 'all':
            filtros_depositos.append(Captacion.sucursal == sucursal)

        depositos_mes = db.session.query(
            func.count(Captacion.numero_socio)
        ).filter(*filtros_depositos).scalar()
        depositos_mes = int(depositos_mes or 0)

        return {
            'captacion_total': format_currency_short(captacion_total),
            'captacion_total_title': captacion_total,
            'captacion_captado': format_currency_short(capital_captado),
            'captacion_captado_title': capital_captado,
            'captacion_retiro': format_currency_short(retiros_mes),
            'captacion_retiro_title': retiros_mes,
            'captacion_deposito': format_currency_short(depositos_mes),
            'captacion_deposito_title': depositos_mes,
            'ultimo_anio': anio,
            'ultimo_mes': mes
        }
    @staticmethod
    def get_evolution_chart(sucursal='all', anio=None):
        if not anio:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio

        mes_orden = month_case(Captacion.mes)
        query = db.session.query(
            Captacion.mes,
            func.sum(
                Captacion.saldo_total_cierre_mes
            ).label('total')
        ).filter(
            Captacion.anio == anio
        )
        if sucursal and sucursal != 'all':
            query = query.filter(
                Captacion.sucursal == sucursal
            )

        datos = query.group_by(
            Captacion.mes
        ).order_by(
            mes_orden.asc()
        ).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.mes.upper())
            series.append(float(row.total or 0))

        return {
            'chart_labels': labels,
            'chart_series': series
        }
    @staticmethod
    def get_producto_chart(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Captacion.tipo_deposito_cuenta_producto,
            func.sum(
                Captacion.saldo_total_cierre_mes
            ).label('total')
        ).filter(
            Captacion.anio == anio,
            Captacion.mes == mes
        )

        if sucursal and sucursal != 'all':
            query = query.filter(
                Captacion.sucursal == sucursal
            )

        datos = query.group_by(
            Captacion.tipo_deposito_cuenta_producto
        ).order_by(
            desc('total')
        ).limit(10).all()

        labels = []
        series = []

        for row in datos:
            labels.append(row.tipo_deposito_cuenta_producto)
            series.append(float(row.total or 0))

        return {
            'chart_labels': labels,
            'chart_series': series
        }
    @staticmethod
    def get_sucursal_chart(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Captacion.sucursal,
            func.sum(
                Captacion.saldo_total_cierre_mes
            ).label('total')
        ).filter(
            Captacion.anio == anio,
            Captacion.mes == mes
        )

        if sucursal and sucursal != 'all':
            query = query.filter(
                Captacion.sucursal == sucursal
            )

        datos = query.group_by(
            Captacion.sucursal
        ).order_by(
            desc('total')
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
    def get_tipo_socio_chart(sucursal='all',anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        filtros = [
            Captacion.anio == anio,
            Captacion.mes == mes
        ]

        if sucursal and sucursal != 'all':
            filtros.append(Captacion.sucursal == sucursal)

        menor_total = db.session.query(
            func.sum(
                Captacion.saldo_total_cierre_mes
            )
        ).filter(
            *filtros,
            Captacion.no_socio_padre_tutor.isnot(None),
            Captacion.no_socio_padre_tutor != ''
        ).scalar()

        mayor_total = db.session.query(
            func.sum(
                Captacion.saldo_total_cierre_mes
            )
        ).filter(
            *filtros,
            or_(
                Captacion.no_socio_padre_tutor.is_(None),
                Captacion.no_socio_padre_tutor == ''
            )
        ).scalar()

        menor_total = float(menor_total or 0)
        mayor_total = float(mayor_total or 0)

        return {
            'chart_labels': [
                'Socio Mayor',
                'Socio Menor'
            ],
            'chart_series': [
                mayor_total,
                menor_total
            ]
        }
    @staticmethod
    def get_top_ahorradores(sucursal='all',anio=None,mes=None):
        if not anio or not mes:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        tipos_excluidos = [
            'PARTE SOCIAL ADICIONAL 1',
            'AHORRO INFANTIL CACHI',
            'PARTE SOCIAL OBLIGATORIA'
        ]

        query = db.session.query(
            Captacion.numero_socio,
            func.sum(
                Captacion.saldo_total_cierre_mes
            ).label('total')
        ).filter(
            Captacion.anio == anio,
            Captacion.mes == mes,
            ~Captacion.tipo_deposito_cuenta_producto.in_(tipos_excluidos)
        )

        if sucursal != 'all':
            query = query.filter(
                Captacion.sucursal == sucursal
            )

        datos = query.group_by(
            Captacion.numero_socio
        ).order_by(
            desc('total')
        ).limit(10).all()

        labels = []
        series = []

        for row in datos:
            labels.append(
                row.numero_socio
            )
            series.append(
                float(row.total or 0)
            )

        return {
            'chart_labels': labels,
            'chart_series': series
        }