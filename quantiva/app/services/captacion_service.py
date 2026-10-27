from sqlalchemy import func, extract, desc, or_
from app import db
from app.models.captacion import Captacion
from app.services.filter_service import FilterService
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

        filtros = [Captacion.anio == anio,Captacion.mes == mes]
        periodo = [Captacion.anio == anio, Captacion.mes == mes]

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

        # 5. Socios con captación
        socios_captacion = db.session.query(
            func.count(func.distinct(Captacion.numero_socio))
        ).filter(
            *periodo,
            Captacion.numero_socio.isnot(None),
            Captacion.saldo_total_cierre_mes > 0
        ).scalar() or 0

        # 6. Capital de depósitos a plazo
        capital_plazo = db.session.query(
            func.coalesce(func.sum(Captacion.saldo_total_cierre_mes), 0)
        ).filter(
            *periodo,
            Captacion.tipo_deposito_cuenta_producto.ilike('%PLAZO%')
        ).scalar() or 0
        capital_plazo = float(capital_plazo)

        # 7. Número de cuentas o contratos
        numero_cuentas = db.session.query(
            func.count(func.distinct(Captacion.num_contrato_cuenta))
        ).filter(
            *periodo,
            Captacion.num_contrato_cuenta.isnot(None)
        ).scalar() or 0

        # 8. Intereses generados durante el mes
        # Reemplaza intereses_generados_mes por el nombre real de tu columna.
        intereses_mes = db.session.query(
            func.coalesce(func.sum(Captacion.intereses_generados_mes), 0)
        ).filter(*periodo).scalar() or 0
        intereses_mes = float(intereses_mes)

        return {
            'captacion_total': format_currency_short(captacion_total),
            'captacion_total_title': captacion_total,
            'captacion_captado': format_currency_short(capital_captado),
            'captacion_captado_title': capital_captado,
            'captacion_retiro': format_currency_short(retiros_mes),
            'captacion_retiro_title': int(retiros_mes),
            'captacion_deposito': format_currency_short(depositos_mes),
            'captacion_deposito_title': int(depositos_mes),
            'socios_captacion': f'{socios_captacion:,}',
            'socios_captacion_title': int(socios_captacion),
            'capital_plazo': format_currency_short(capital_plazo),
            'capital_plazo_title': capital_plazo,
            'numero_cuentas': f'{numero_cuentas:,}',
            'numero_cuentas_title': int(numero_cuentas),
            'intereses_mes': format_currency_short(intereses_mes),
            'intereses_mes_title': intereses_mes,
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
    def get_ahorradores_por_sucursal_chart(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            Captacion.sucursal,
            func.count(
                func.distinct(Captacion.numero_socio)
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

        return {
            'chart_labels': [row.sucursal for row in datos],
            'chart_series': [int(row.total or 0) for row in datos]
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
    @staticmethod
    def get_composicion_captacion_producto(sucursal='all', anio=None, mes=None):
        if not anio or not mes:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = ultimo_periodo.anio
            mes = ultimo_periodo.mes

        query = db.session.query(
            func.coalesce(
                func.nullif(func.trim(Captacion.tipo_deposito_cuenta_producto), ''),
                'Sin especificar'
            ).label('producto'),
            func.sum(Captacion.saldo_total_cierre_mes).label('saldo')
        ).filter(
            Captacion.saldo_total_cierre_mes.isnot(None)
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Captacion.sucursal == sucursal)
        if anio:
            query = query.filter(Captacion.anio == int(anio))
        if mes:
            query = query.filter(Captacion.mes == mes)

        resultados = query.group_by('producto').order_by(
            func.sum(Captacion.saldo_total_cierre_mes).desc()
        ).all()

        labels = [r.producto for r in resultados]
        valores = [round(float(r.saldo or 0), 2) for r in resultados]
        total = sum(valores)

        return {
            'chart_labels': labels,
            'chart_values': valores,
            'chart_percentages': [
                round(v / total * 100, 2) if total else 0
                for v in valores
            ],
            'captacion_total': round(total, 2)
        }
    @staticmethod
    def get_variacion_mensual_captacion(sucursal='all', anio=None):
        if not anio:
            ultimo_periodo = CaptacionService.get_latest_period()
            anio = int(ultimo_periodo.anio)
        else:
            anio = int(anio)

        orden_meses = {
            'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4,
            'may': 5, 'jun': 6, 'jul': 7, 'ago': 8,
            'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
        }

        query = db.session.query(
            Captacion.anio,
            Captacion.mes,
            func.sum(Captacion.saldo_total_cierre_mes).label('saldo')
        ).filter(
            Captacion.anio.in_([anio - 1, anio])
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Captacion.sucursal == sucursal)

        resultados = query.group_by(
            Captacion.anio,
            Captacion.mes
        ).all()

        periodos = []

        for r in resultados:
            mes = str(r.mes).strip().lower()[:3]
            numero_mes = orden_meses.get(mes)

            if numero_mes is None:
                continue

            periodos.append({
                'anio': int(r.anio),
                'mes': mes,
                'numero_mes': numero_mes,
                'saldo': float(r.saldo or 0)
            })

        periodos.sort(key=lambda x: (x['anio'], x['numero_mes']))

        variaciones = []

        for i in range(1, len(periodos)):
            actual = periodos[i]
            anterior = periodos[i - 1]

            periodo_actual = actual['anio'] * 12 + actual['numero_mes']
            periodo_anterior = anterior['anio'] * 12 + anterior['numero_mes']

            if periodo_actual - periodo_anterior != 1:
                continue

            if actual['anio'] != anio:
                continue

            variacion = actual['saldo'] - anterior['saldo']

            variaciones.append({
                'periodo': f"{actual['mes'].capitalize()} {actual['anio']}",
                'variacion': round(variacion, 2),
                'saldo_actual': round(actual['saldo'], 2),
                'saldo_anterior': round(anterior['saldo'], 2)
            })

        return {
            'chart_labels': [v['periodo'] for v in variaciones],
            'chart_values': [v['variacion'] for v in variaciones],
            'variaciones': variaciones
        }
    @staticmethod
    def get_evolucion_socios_ahorradores(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            Captacion.tipo_deposito_cuenta_producto.label('producto'),
            func.count(func.distinct(Captacion.numero_socio)).label('cantidad')
        ).filter(
            Captacion.numero_socio.isnot(None),
            Captacion.tipo_deposito_cuenta_producto.isnot(None)
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Captacion.sucursal == sucursal)

        if anio:
            query = query.filter(Captacion.anio == int(anio))

        if mes and mes.lower() not in ('all', 'todos', ''):
            query = query.filter(func.lower(Captacion.mes) == mes.strip().lower())

        resultados = query.group_by(
            Captacion.tipo_deposito_cuenta_producto
        ).order_by(
            Captacion.tipo_deposito_cuenta_producto
        ).all()

        return {
            'chart_labels': [r.producto for r in resultados],
            'chart_values': [int(r.cantidad or 0) for r in resultados]
        }
    @staticmethod
    def get_evolucion_numero_cuentas(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            Captacion.tipo_deposito_cuenta_producto.label('producto'),
            func.count(
                func.distinct(Captacion.num_contrato_cuenta)
            ).label('cantidad')
        ).filter(
            Captacion.num_contrato_cuenta.isnot(None),
            Captacion.tipo_deposito_cuenta_producto.isnot(None)
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Captacion.sucursal == sucursal)

        if anio:
            query = query.filter(Captacion.anio == int(anio))

        if mes and mes.lower() not in ('all', 'todos', ''):
            query = query.filter(func.lower(Captacion.mes) == mes.strip().lower())

        resultados = query.group_by(
            Captacion.tipo_deposito_cuenta_producto
        ).order_by(
            Captacion.tipo_deposito_cuenta_producto
        ).all()

        return {
            'chart_labels': [r.producto for r in resultados],
            'chart_values': [int(r.cantidad or 0) for r in resultados]
        }
    @staticmethod
    def get_numero_cuentas_por_sucursal(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            Captacion.sucursal,
            func.count(
                func.distinct(Captacion.num_contrato_cuenta)
            ).label('cantidad')
        ).filter(
            Captacion.sucursal.isnot(None),
            Captacion.num_contrato_cuenta.isnot(None)
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Captacion.sucursal == sucursal)

        if anio:
            query = query.filter(Captacion.anio == int(anio))

        if mes and mes.lower() not in ('all', 'todos', ''):
            query = query.filter(
                func.lower(Captacion.mes) == mes.strip().lower()
            )

        resultados = query.group_by(
            Captacion.sucursal
        ).order_by(
            Captacion.sucursal
        ).all()

        return {
            'chart_labels': [r.sucursal for r in resultados],
            'chart_values': [int(r.cantidad or 0) for r in resultados]
        }
    @staticmethod
    def get_top_socios_por_numero_cuentas(sucursal='all', anio=None, mes=None):
        query = db.session.query(
            Captacion.numero_socio,
            func.max(Captacion.nombre_socio).label('nombre_socio'),
            func.count(
                func.distinct(Captacion.num_contrato_cuenta)
            ).label('numero_cuentas')
        ).filter(
            Captacion.numero_socio.isnot(None),
            Captacion.num_contrato_cuenta.isnot(None)
        )

        if sucursal and sucursal != 'all':
            query = query.filter(Captacion.sucursal == sucursal)

        if anio:
            query = query.filter(Captacion.anio == int(anio))

        if mes and mes.strip().lower() not in ('all', 'todos', ''):
            query = query.filter(
                func.lower(Captacion.mes) == mes.strip().lower()
            )

        resultados = query.group_by(
            Captacion.numero_socio
        ).order_by(
            func.count(func.distinct(Captacion.num_contrato_cuenta)).desc(),
            Captacion.numero_socio
        ).limit(10).all()

        return {
            'chart_labels': [
                f"{r.numero_socio} - {r.nombre_socio or 'Sin nombre'}"
                for r in resultados
            ],
            'chart_values': [
                int(r.numero_cuentas or 0)
                for r in resultados
            ],
            'socios': [
                {
                    'numero_socio': str(r.numero_socio),
                    'nombre_socio': r.nombre_socio or 'Sin nombre',
                    'numero_cuentas': int(r.numero_cuentas or 0)
                }
                for r in resultados
            ]
        }