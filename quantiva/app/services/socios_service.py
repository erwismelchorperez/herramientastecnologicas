from sqlalchemy import func, extract, desc, or_, case
from app import db
from app.models.socios import Socios
from app.utils.months import month_case
from app.utils.months import month_number
from app.utils.formatters import format_currency_short, format_number_short
from datetime import datetime
import calendar
class SociosService:
    @staticmethod
    def get_latest_period():
        mes_orden = month_case(Socios.mes)
        return db.session.query(Socios.anio,Socios.mes).order_by(Socios.anio.desc(),mes_orden.desc()).first()
    @staticmethod
    def get_general_kpis(anio=None, mes=None):
        if not anio or not mes:
            ultimo=SociosService.get_latest_period()
            anio=ultimo.anio
            mes=ultimo.mes

        fecha_inicio=datetime.strptime(f'{anio}-{month_number(mes)}-01','%Y-%m-%d')
        ultimo_dia=calendar.monthrange(anio,fecha_inicio.month)[1]

        fecha_fin=datetime(anio,fecha_inicio.month,ultimo_dia)

        capital_social=db.session.query(
            func.sum(
                Socios.capital_social
            )
        ).filter(
            Socios.fecha_baja.is_(None)
        ).scalar()

        socios_activos=db.session.query(
            func.count(
                Socios.numero_socio
            )
        ).filter(
            Socios.fecha_baja.is_(None)
        ).scalar()

        altas_mes=db.session.query(
            func.count(
                Socios.numero_socio
            )
        ).filter(
                Socios.fecha_ingreso.between(
                fecha_inicio,
                fecha_fin
            )
        ).scalar()

        bajas_mes=db.session.query(
            func.count(
                Socios.numero_socio
            )
        ).filter(
            Socios.fecha_baja.isnot(None),
            Socios.fecha_baja.between(
                fecha_inicio,
                fecha_fin
            )
        ).scalar()

        capital_social=float(capital_social or 0)

        socios_activos=int(socios_activos or 0)

        altas_mes=int(altas_mes or 0)

        bajas_mes=int(bajas_mes or 0)

        return {
            'capital_social':format_currency_short(capital_social),
            'capital_social_title':capital_social,
            'socios_activos':format_number_short(socios_activos),
            'socios_activos_title':socios_activos,
            'altas_mes':format_number_short(altas_mes),
            'altas_mes_title':altas_mes,
            'bajas_mes':format_number_short(bajas_mes),
            'bajas_mes_title':bajas_mes,
            'ultimo_anio':anio,
            'ultimo_mes':mes
        }
    @staticmethod
    def get_sucursal_chart(anio=None,mes=None):

        if not anio or not mes:
            ultimo=SociosService.get_latest_period()
            anio=ultimo.anio
            mes=ultimo.mes

        datos=db.session.query(
            Socios.sucursal,
            func.count(
                Socios.numero_socio
            ).label('total')
        ).filter(
            Socios.anio==anio,
            Socios.mes==mes,
            Socios.fecha_baja.is_(None)
        ).group_by(
            Socios.sucursal
        ).order_by(
            desc('total')
        ).all()

        return{
            'chart_labels':[ x.sucursal for x in datos],
            'chart_series':[ int(x.total) for x in datos]
        }
    @staticmethod
    def get_sexo_chart(anio=None,mes=None):

        if not anio or not mes:
            ultimo=SociosService.get_latest_period()
            anio=ultimo.anio
            mes=ultimo.mes

        datos=db.session.query(
            Socios.sexo,
            func.count(
                Socios.numero_socio
            ).label('total')
        ).filter(
            Socios.anio==anio,
            Socios.mes==mes,
            Socios.fecha_baja.is_(None)
        ).group_by(
            Socios.sexo
        ).all()

        return{
            'chart_labels':[(x.sexo if x.sexo else 'SIN DATO') for x in datos ],
            'chart_series':[int(x.total) for x in datos ] 
            }
    @staticmethod
    def get_edad_chart(anio=None,mes=None):

        if not anio or not mes:
            ultimo=SociosService.get_latest_period()
            anio=ultimo.anio
            mes=ultimo.mes

        fecha_corte=datetime(
            anio,
            month_number(mes),
            calendar.monthrange(
                anio,
                month_number(mes)
            )[1]
        )

        edad=func.extract(
            'year',
            func.age(
                fecha_corte,
                Socios.fecha_nacimiento
            )
        )

        rango=case(
            (edad<18,'0–17'),
            (edad<=25,'18–25'),
            (edad<=35,'26–35'),
            (edad<=45,'36–45'),
            (edad<=60,'46–60'),
            else_='60+'
        )

        orden=case(
            (edad<18,1),
            (edad<=25,2),
            (edad<=35,3),
            (edad<=45,4),
            (edad<=60,5),
            else_=6
        )

        datos=db.session.query(
            rango.label('rango'),
            orden.label('orden'),
            func.count(
                Socios.numero_socio
            )
        ).filter(
            Socios.fecha_baja.is_(None),
            Socios.anio==anio,
            Socios.mes==mes,
            Socios.fecha_nacimiento.isnot(None)
        ).group_by(
            rango,
            orden
        ).order_by(
            orden
        ).all()

        return{
            'chart_labels':[x[0] for x in datos],
            'chart_series':[int(x[2]) for x in datos]
        }

    @staticmethod
    def get_antiguedad_chart(anio=None,mes=None):

        if not anio or not mes:
            ultimo=SociosService.get_latest_period()
            anio=ultimo.anio
            mes=ultimo.mes

        fecha_corte=datetime(
            anio,
            month_number(mes),
            calendar.monthrange(
                anio,
                month_number(mes)
            )[1]
        )

        antiguedad=func.extract(
            'year',
            func.age(
                fecha_corte,
                Socios.fecha_ingreso
            )
        )

        rango=case(
            (antiguedad<1,'<1'),
            (antiguedad<=3,'1–3'),
            (antiguedad<=5,'3–5'),
            (antiguedad<=10,'5–10'),
            else_='10+'
        )

        orden=case(
            (antiguedad<1,1),
            (antiguedad<=3,2),
            (antiguedad<=5,3),
            (antiguedad<=10,4),
            else_=5
        )

        datos=db.session.query(
            rango.label('rango'),
            orden.label('orden'),
            func.count(
                Socios.numero_socio
            )
        ).filter(
            Socios.fecha_baja.is_(None),
            Socios.anio==anio,
            Socios.mes==mes,
            Socios.fecha_ingreso.isnot(None)
        ).group_by(
            rango,
            orden
        ).order_by(
            orden
        ).all()

        return{
            'chart_labels':[x[0] for x in datos],
            'chart_series':[int(x[2]) for x in datos]
        }