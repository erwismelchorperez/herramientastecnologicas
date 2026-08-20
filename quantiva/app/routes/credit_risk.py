from flask import Blueprint,render_template,request, jsonify
from flask_login import login_required, current_user

from app.services.filter_service import FilterService
from app.services.socios_service import SociosService
from app.services.cartera_service import CarteraService
from app.services.credit_risk_service import CreditRiskService


credit_risk = Blueprint('credit_risk',__name__,url_prefix='/credit_risk')
@credit_risk.route('/dashboard')
@login_required
def dashboard():
    return render_template('forecasting/dashboard.html')
@credit_risk.route('/evaluation')
@login_required
def evaluation():
    """
    if request.method == "POST":
        CreditRiskService.save_prediction(request.form,current_user.username)
    """
    return render_template('forecasting/evaluation.html')
@credit_risk.route("/predict", methods=["POST"])
@login_required
def predict():
    prediction = CreditRiskService.save_prediction(request.form,current_user.username)
    return jsonify({
        "success": True,
        "prediction_id": prediction.id,
        "prediction": prediction.prediction,
        "probability": prediction.probability
    })

@credit_risk.route("/api/history")
@login_required
def history():
    data = CreditRiskService.get_predictions()
    return jsonify(data)
@credit_risk.route("/api/evaluation/<int:id>")
@login_required
def get_prediction(id):
    data = CreditRiskService.get_prediction(id)
    return jsonify(data)