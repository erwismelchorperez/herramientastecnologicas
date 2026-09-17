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
    def limpiar_dataframe(dataframe):

        print("======================================")
        print("DATAFRAME ORIGINAL")
        print("======================================")

        print(dataframe.head(10).to_string())

        print("======================================")
        print("COLUMNAS")
        print("======================================")

        print(dataframe.columns)

        return dataframe
    @staticmethod
    def clean_boolean(value):
        if pd.isna(value):
            return False

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return bool(value)

        value = str(value).strip().lower()

        if value in ["si", "sí", "yes", "true", "1", "verdadero"]:
            return True

        if value in ["no", "false", "0", "falso"]:
            return False

        return False
    @staticmethod
    def importar(archivo, fecha_cierre, usuario):

        try:

            fecha = datetime.strptime(fecha_cierre, "%Y-%m-%d")
            anio = fecha.year
            mes = MESES[fecha.month]
            # ------------------------------------------------
            # Leer archivo
            # ------------------------------------------------
            filename = archivo.filename.lower()
            if filename.endswith(".xlsx"):
                dataframe = pd.read_excel(archivo,header=5)

            elif filename.endswith(".csv"):
                dataframe = pd.read_csv(archivo,header=None)

            else:
                raise ValueError("El archivo debe ser CSV o Excel.")

            # ------------------------------------------------
            # Procesar
            # ------------------------------------------------

            dataframe = ConfiguracionService.limpiar_dataframe(dataframe)
            dataframe = dataframe[~dataframe["Nombre del Acreditado"].str.contains("SubTotal|Naturaleza:|Nombre del|Producto:|Sucursal:|CREDITOS|Total Cartera|Tipo de Crédito:", case=False, na=False)]

            #dataframe["Emproblemado"] = dataframe["Emproblemado"].apply(clean_boolean)
            #dataframe["CARGO DEL ACREDITADO PARTE RELACIONADA art. 26 LRASCAP"] = (dataframe["CARGO DEL ACREDITADO PARTE RELACIONADA art. 26 LRASCAP"].apply(clean_boolean))
            #dataframe = dataframe.replace({np.nan: None})

            registros = []

            for _, row in dataframe.iterrows():
                credito = Credito(
                    nombre_acreditado=row["Nombre del Acreditado"],
                    numero_socio_cliente=row["Número de Socio y/o Cliente"],
                    numero_credito=row["Número de Crédito"],
                    sucursal=row["Sucursal"],
                    clasificacion_credito=row["Clasificacion de Crédito"],
                    producto_credito=row["Producto de Crédito"],
                    tipo_cuota=row["Tipo de Cuota"],
                    fecha_otorgamiento=row["Fecha de Otorgamiento"],
                    monto_original=row["Monto Original"],
                    fecha_vencimiento=row["Fecha de Vencimiento"],
                    tasa_ord_nom_anual=row["Tasa Ord. Nom. Anual"],
                    tasa_moratoria_nom_anual=row["Tasa Moratoria Nominal Anual %"],
                    plazo_credito=row["Plazo del Credito "],
                    frecuencia_pago_capital=row["Frecuencia de Pago Capital "],
                    frecuencia_pago_intereses=row["Frecuencia de Pago Intereses "],
                    dias_mora_cartera=row["Dias de Mora Cartera"],
                    capital_vigente=row["Capital Vigente"],
                    capital_vencido=row["Capital Vencido"],
                    intereses_moratorios_devengados_no_cobrados=row["Intereses Moratorios Devengados No Cobrados"],
                    intereses_ordinarios_devengados_no_cobrados_vigente = row["Intereses Ordinarios Devengados No Cobrados Vigente"],
                    intereses_devengados_no_cobrados_vencido = row["Intereses Devengados No Cobrados Vencido"],
                    intereses_devengados_no_cobrados_cuentas_orden = row["Intereses Devengados No Cobrados Cuentas de Orden"],
                    fecha_ultimo_pago_capital = row["Fecha de Ultimo Pago de Capital"],
                    monto_ultimo_pago_capital = row["Monto Ultimo Pago de Capital"],
                    fecha_ultimo_pago_interes = row["Fecha de Ultimo Pago de Interes"],
                    monto_ultimo_pago_interes = row["Monto Ultimo Pago de Interes"],
                    renovado_reestructurado_normal = row["Renovado, reestructurado ó normal"],
                    emproblemado = ConfiguracionService.clean_boolean(row["Emproblemado"]),
                    vigente_vencido=row["Vigente ó vencido"],
                    cargo_parte_relacionada = ConfiguracionService.clean_boolean(row["CARGO DEL ACREDITADO PARTE RELACIONADA art. 26 LRASCAP"]),
                    monto_garantia_liquida = row["Monto Garantia Liquida"],
                    cuentas_garantia_liquida = row["CUENTA(S) SOBRE LA(S) QUE SE CONSITUYO GARANTIA LIQUIDA"],
                    monto_garantia_prendaria = row["MONTO GARANTIA PRENDARIA"],
                    monto_garantia_hipotecaria = row["MONTO GARANTIA HIPOTECARIA"],
                    eprc_para_parte_cubierta = row["EPRC PARA PARTE CUBIERTA"],
                    eprc_para_parte_expuesta = row["EPRC PARA PARTE EXPUESTA"],
                    eprc_intereses_cave = row["EPRC X INTERESES DE CaVe"],
                    anio=anio,
                    mes=mes
                )

                registros.append(credito)

            # ------------------------------------------------
            # INSERT
            # ------------------------------------------------

            db.session.bulk_save_objects(registros)

            db.session.commit()

            return {
                "success": True,
                "insertados": len(registros),
                "anio": anio,
                "mes": mes,
                "usuario": usuario
            }

        except Exception:

            db.session.rollback()

            raise