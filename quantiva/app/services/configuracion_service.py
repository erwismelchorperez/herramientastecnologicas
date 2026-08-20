from sqlalchemy import func, extract, desc, or_
from app import db
from app.models.creditos import Credito
from app.utils.months import month_case
from app.utils.months import month_number
from app.utils.formatters import format_currency_short
import pandas as pd
from datetime import datetime

MESES = {1: "ene",2: "feb",3: "mar",4: "abr",5: "may",6: "jun",7: "jul",8: "ago",9: "sep",10: "oct",11: "nov",12: "dic"}
class ConfiguracionService:
    @staticmethod
    def get_latest_period():
        mes_orden = month_case(Credito.mes)
        return db.session.query(Credito.anio,Credito.mes).order_by(Credito.anio.desc(),mes_orden.desc()).first()
    @staticmethod
    def importar(archivo,fecha_cierre,usuario):
        fecha = datetime.strptime(fecha_cierre,"%Y-%m-%d")
        anio = fecha.year
        mes = MESES[fecha.month]
        # ------------------------------------------------
        # Leer archivo
        # ------------------------------------------------
        filename = archivo.filename.lower()
        if filename.endswith(".xlsx"):
            dataframe = pd.read_excel(archivo,header=None)
        elif filename.endswith(".csv"):
            dataframe = pd.read_csv(archivo,header=None)
        else:
            raise ValueError("El archivo debe ser CSV o Excel.")
        # ------------------------------------------------
        # Procesar
        # ------------------------------------------------
        registros = []
        # Aquí posteriormente colocaremos
        # el parser específico de tu archivo.
        #
        # Por ahora:
        dataframe = (ConfiguracionService.limpiar_dataframe(dataframe))
        for _, row in dataframe.iterrows():
            credito = Credito(
                nombre_acreditado=row["nombre_acreditado"],
                numero_socio_cliente=row["numero_socio_cliente"],
                numero_credito=row["numero_credito"],
                sucursal=row["sucursal"],
                clasificacion_credito=row["clasificacion_credito"],
                producto_credito=row["producto_credito"],
                tipo_cuota=row["tipo_cuota"],
                fecha_otorgamiento=row["fecha_otorgamiento"],
                monto_original=row["monto_original"],
                fecha_vencimiento=row["fecha_vencimiento"],
                tasa_ord_nom_anual=row["tasa_ord_nom_anual"],
                tasa_moratoria_nom_anual=row["tasa_moratoria_nom_anual"],
                plazo_credito=row["plazo_credito"],
                frecuencia_pago_capital=row["frecuencia_pago_capital"],
                frecuencia_pago_intereses=row["frecuencia_pago_intereses"],
                dias_mora_cartera=row["dias_mora_cartera"],
                capital_vigente=row["capital_vigente"],
                capital_vencido=row["capital_vencido"], vigente_vencido=row["vigente_vencido"],anio=anio,mes=mes)
            registros.append(credito)
        # ------------------------------------------------
        # INSERT
        # ------------------------------------------------
        db.session.bulk_save_objects(registros)
        db.session.commit()

        return {"success": True,"insertados": len(registros),"anio": anio,"mes": mes,"usuario": usuario}
    