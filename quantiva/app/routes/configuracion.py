from flask import Blueprint,render_template,request, jsonify
from flask_login import login_required

from app.services.filter_service import FilterService
from app.services.configuracion_service import ConfiguracionService

configuracion = Blueprint('configuracion',__name__,url_prefix='/configuracion')
@configuracion.route('/confcartera')
@login_required
def confcartera():
    
    ultimo_periodo = ConfiguracionService.get_latest_period()
    selected_anio = request.args.get('anio',default=ultimo_periodo.anio,type=int)
    selected_mes = request.args.get('mes',default=ultimo_periodo.mes)
    
    anios = (FilterService.get_available_years())
    meses = (FilterService.get_available_months(selected_anio))
    return render_template('configuracion/confcartera.html', anios=anios, meses=meses)
@configuracion.route("/api/importar", methods=["POST"])
@login_required
def importar_cartera():
    try:
        archivo = request.files.get("archivo")
        fecha_cierre = request.form.get("fecha_cierre")

        if not archivo:
            return jsonify({"message": "No se recibió ningún archivo."}), 400

        if not fecha_cierre:
            return jsonify({"message": "Debe indicar la fecha de cierre."}), 400

        resultado = ConfiguracionService.importar(archivo,fecha_cierre,'admin')

        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except Exception as e:

        print("ERROR:", e)

        return jsonify({"message": "Error al importar la cartera."}), 500