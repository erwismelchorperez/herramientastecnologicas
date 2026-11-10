from sqlalchemy import func

from app import db

from app.models.forecast_model import ForecastModel
from app.models.forecast_run import ForecastRun
from app.models.forecast_value import ForecastValue
from app.models.forecast_comparison import ForecastComparison


class ForecastDashboardService:

    @staticmethod
    def get_active_models(institucion_id):
        """
        Obtiene el total de modelos activos de una institución.
        """

        total = db.session.query(
            func.count(ForecastModel.id)
        ).filter(
            ForecastModel.institucion_id == institucion_id,
            ForecastModel.status == 'ACTIVE'
        ).scalar()

        return total or 0

    @staticmethod
    def get_last_execution(institucion_id):
        """
        Obtiene la última ejecución de pronósticos completada.
        """

        return db.session.query(
            ForecastRun
        ).filter(
            ForecastRun.institucion_id == institucion_id,
            ForecastRun.status == 'COMPLETED'
        ).order_by(
            ForecastRun.generated_at.desc()
        ).first()

    @staticmethod
    def get_generated_forecasts(institucion_id):
        """
        Obtiene el total de valores pronosticados
        correspondientes a ejecuciones completadas.
        """

        total = db.session.query(
            func.count(ForecastValue.id)
        ).join(
            ForecastRun,
            ForecastValue.forecast_run_id == ForecastRun.id
        ).filter(
            ForecastRun.institucion_id == institucion_id,
            ForecastRun.status == 'COMPLETED'
        ).scalar()

        return total or 0

    @staticmethod
    def get_pending_evaluations(institucion_id):
        """
        Obtiene los pronósticos que tienen información real
        disponible y todavía no han sido evaluados.

        Pendiente de implementar la correspondencia entre
        forecast_date y los periodos reales de cartera.
        """

        return 0

    @staticmethod
    def get_dashboard_data(institucion_id):
        """
        Recupera todos los indicadores necesarios
        para el dashboard de pronósticos financieros.
        """

        return {
            'active_models': ForecastDashboardService.get_active_models(
                institucion_id
            ),

            'last_execution': ForecastDashboardService.get_last_execution(
                institucion_id
            ),

            'generated_forecasts': ForecastDashboardService.get_generated_forecasts(
                institucion_id
            ),

            'pending_evaluations': ForecastDashboardService.get_pending_evaluations(
                institucion_id
            )
        }