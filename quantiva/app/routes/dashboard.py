from flask import Blueprint,render_template
from flask_login import login_required,current_user
from app.utils.months import month_case
from sqlalchemy import func
from app import db
from app.models.creditos import Credito
from app.models.captacion import Captacion
from app.services.dashboard_service import DashboardService

dashboard = Blueprint('dashboard',__name__)

@dashboard.route('/')
@login_required
def index():
    data = (DashboardService.get_dashboard_data())
    return render_template(
        'dashboard/index.html',
        user=current_user,**data
    )
