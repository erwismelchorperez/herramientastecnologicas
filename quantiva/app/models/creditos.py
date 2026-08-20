"""from app import db

class Credito(db.Model):

    __tablename__ = 'creditos'
    id = db.Column(db.BigInteger,primary_key=True)
    anio = db.Column(db.Integer,nullable=False)
    mes = db.Column(db.String(10),nullable=False)
    capital_vigente = db.Column(db.Numeric(14,2),nullable=True)
    capital_vencido = db.Column(db.Numeric(14,2),nullable=True)
    producto_credito = db.Column(db.String(100),nullable=False)
    clasificacion_credito = db.Column(db.String(100),nullable=False)
    sucursal = db.Column(db.String(100),nullable=False)
    numero_credito = db.Column(db.String(100),nullable=False)
    vigente_vencido = db.Column(db.String(20),nullable=False)
    renovado_reestructurado_normal = db.Column(db.String(20),nullable=False)
    monto_original = db.Column(db.Numeric(14,2),nullable=True)
"""
from app import db


class Credito(db.Model):

    __tablename__ = 'creditos'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    nombre_acreditado = db.Column(db.String(255), nullable=False)
    numero_socio_cliente = db.Column(db.String(100), nullable=True)
    numero_credito = db.Column(db.String(100), nullable=True)
    sucursal = db.Column(db.String(100), nullable=True)

    clasificacion_credito = db.Column(db.String(50), nullable=True)
    producto_credito = db.Column(db.String(100), nullable=True)
    tipo_cuota = db.Column(db.String(100), nullable=True)

    fecha_otorgamiento = db.Column(db.Date, nullable=False)
    monto_original = db.Column(db.Numeric(18, 2), nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)

    tasa_ord_nom_anual = db.Column(db.Numeric(10, 4), nullable=False)
    tasa_moratoria_nom_anual = db.Column(
        db.Numeric(10, 4),
        nullable=False,
        default=0
    )

    plazo_credito = db.Column(db.String(50), nullable=False)
    frecuencia_pago_capital = db.Column(db.String(50), nullable=True)
    frecuencia_pago_intereses = db.Column(db.String(50), nullable=True)

    dias_mora_cartera = db.Column(db.Integer, nullable=False, default=0)

    capital_vigente = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    capital_vencido = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    intereses_moratorios_devengados_no_cobrados = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    intereses_ordinarios_devengados_no_cobrados_vigente = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    intereses_devengados_no_cobrados_vencido = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    intereses_devengados_no_cobrados_cuentas_orden = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    fecha_ultimo_pago_capital = db.Column(db.Date, nullable=True)

    monto_ultimo_pago_capital = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    fecha_ultimo_pago_interes = db.Column(db.Date, nullable=True)

    monto_ultimo_pago_interes = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    renovado_reestructurado_normal = db.Column(
        db.String(50),
        nullable=True
    )

    emproblemado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    vigente_vencido = db.Column(
        db.String(20),
        nullable=True
    )

    cargo_parte_relacionada = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    monto_garantia_liquida = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    cuentas_garantia_liquida = db.Column(
        db.String(50),
        nullable=True
    )

    monto_garantia_prendaria = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    monto_garantia_hipotecaria = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    eprc_para_parte_cubierta = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    eprc_para_parte_expuesta = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    eprc_intereses_cave = db.Column(
        db.Numeric(18, 2),
        nullable=False,
        default=0
    )

    anio = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.String(3), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False
    )