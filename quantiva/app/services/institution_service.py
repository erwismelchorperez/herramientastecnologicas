from sqlalchemy import func, desc, case
from app import db
from app.models.institucion import Institucion
from app.utils.months import month_case
from app.utils.formatters import format_currency_short
from collections import defaultdict
class InstitucionService:

    @staticmethod
    def get_tipo_institucion():
        institucion = db.session.query(
            Institucion.tipo
        ).first()

        return institucion.tipo if institucion else None