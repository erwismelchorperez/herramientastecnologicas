from app import db
from app.models.credit_risk import CreditRiskPrediction, CreditRiskPredictionExplanation
from app.ml.pattern_classifier import PatternClassifier

from app import db
from app.models.credit_risk import (
    CreditRiskPrediction,
    CreditRiskPredictionExplanation
)
from app.ml.pattern_classifier import PatternClassifier


class CreditRiskService:

    @staticmethod
    def save_prediction(form, user):
        sample = {
            "edad": int(form["edad"]),
            "codigo_postal": form["codigo_postal"],
            "tipovivienda": form["tipovivienda"],
            "dependientes": int(form["dependientes"]),
            "estadocivil": form["estadocivil"],
            "genero": form["genero"],
            "claveactividad": form["claveactividad"],
            "nivelacademico": form["nivelacademico"],
            "telefono": form["telefono"],
            "ingreso": float(form["ingreso"]),
            "egreso": float(form["egreso"]),
            "tipoprestamo": form["tipoprestamo"],
            "tasainteres": float(form["tasainteres"]),
            "tasamoratoria": float(form["tasamoratoria"]),
            "monto": float(form["monto"]),
            "num_avales": int(form["num_avales"]),
            "creditostrabajados": int(form["creditostrabajados"]),
            "bien": form["bien"],
            "montogarantia": float(form["montogarantia"]),
            "finalidad": form["finalidad"],
            "remesas": form["remesas"],
            "plazo": int(form["plazo"])
        }

        classifier = PatternClassifier("patterns/cips_strong_data-eiz-categorica.json")
        resultado = classifier.predict(sample)

        print("Resultado predicción:", resultado)

        prediction = CreditRiskPrediction(
            edad=int(form["edad"]),
            codigo_postal=form["codigo_postal"],
            tipovivienda=form["tipovivienda"],
            dependientes=int(form["dependientes"]),
            estadocivil=form["estadocivil"],
            genero=form["genero"],
            claveactividad=form["claveactividad"],
            nivelacademico=form["nivelacademico"],
            telefono=form["telefono"],
            ingreso=float(form["ingreso"]),
            egreso=float(form["egreso"]),
            tipoprestamo=form["tipoprestamo"],
            tasainteres=float(form["tasainteres"]),
            tasamoratoria=float(form["tasamoratoria"]),
            monto=float(form["monto"]),
            num_avales=int(form["num_avales"]),
            creditostrabajados=int(form["creditostrabajados"]),
            bien=form["bien"],
            montogarantia=float(form["montogarantia"]),
            finalidad=form["finalidad"],
            remesas=form["remesas"],
            plazo=int(form["plazo"]),

            prediction=resultado["prediction"],
            probability=resultado["probability"],

            created_by=user
        )

        db.session.add(prediction)
        db.session.commit()

        matched_rules = resultado.get("matched_rules", [])

        for rule in matched_rules:
            pattern = rule["pattern"]["Pattern"]
            confidence = rule["confidence"]
            support = rule["support"]
            score = rule["score"]

            for text in rule["explanations"]:
                explanation = CreditRiskPredictionExplanation(
                    prediction_id=prediction.id,
                    pattern=pattern,
                    explanation=text,
                    confidence=confidence,
                    support=support,
                    score=score
                )

                db.session.add(explanation)

        db.session.commit()

        return prediction

    @staticmethod
    def get_predictions():
        rows = (
            CreditRiskPrediction.query
            .order_by(CreditRiskPrediction.created_at.desc())
            .all()
        )

        result = []

        for r in rows:
            result.append({
                "id": r.id,
                "created_at": r.created_at.strftime("%d/%m/%Y %H:%M"),
                "prediction": r.prediction,
                "probability": round(r.probability * 100, 2),
                "created_by": r.created_by
            })

        return result

    @staticmethod
    def get_prediction(id):
        p = CreditRiskPrediction.query.get_or_404(id)

        explanations = (
            CreditRiskPredictionExplanation.query
            .filter_by(prediction_id=id)
            .all()
        )

        patterns = []

        for e in explanations:
            patterns.append({
                "pattern": e.pattern,
                "confidence": float(e.confidence),
                "support": e.support,
                "score": float(e.score),
                "prediction": e.prediction_id,
                "explanations": e.explanation
            })

        return {
            "id": p.id,
            "prediction": p.prediction,
            "probability": float(p.probability),
            "created_at": p.created_at.strftime("%d/%m/%Y %H:%M"),
            "created_by": p.created_by,
            "variables": {
                "Edad": p.edad,
                "Código Postal": p.codigo_postal,
                "Tipo de Vivienda": p.tipovivienda,
                "Dependientes": p.dependientes,
                "Estado Civil": p.estadocivil,
                "Género": p.genero,
                "Clave de Actividad": p.claveactividad,
                "Nivel Académico": p.nivelacademico,
                "Teléfono": p.telefono,
                "Ingreso": float(p.ingreso),
                "Egreso": float(p.egreso),
                "Tipo de Préstamo": p.tipoprestamo,
                "Tasa de Interés": float(p.tasainteres),
                "Tasa Moratoria": float(p.tasamoratoria),
                "Monto": float(p.monto),
                "Número de Avales": p.num_avales,
                "Créditos Trabajados": p.creditostrabajados,
                "Bien": p.bien,
                "Monto de Garantía": float(p.montogarantia),
                "Finalidad": p.finalidad,
                "Remesas": p.remesas,
                "Plazo": p.plazo
            },
            "patterns": patterns
        }

"""
class CreditRiskService:

    @staticmethod
    def save_prediction(form,user):
        sample = {
            "reports": int(form["reports"]),
            "age": float(form["age"]),
            "income": float(form["income"]),
            "share": float(form["share"]),
            "expenditure": float(form["expenditure"]),
            "owner": 1 if form["owner"] == "1" else 0,
            "selfemp": 1 if form["selfemp"] == "1" else 0,
            "dependents": int(form["dependents"]),
            "months": int(form["months"]),
            "majorcards": int(form["majorcards"]),
            "active": int(form["active"])
        }

        classifier = PatternClassifier("patterns/cips_strong_aer.json")
        resultado = classifier.predict(sample)

        print("Resultado predicción             ",resultado)

        prediction = CreditRiskPrediction(
            reports=int(form["reports"]),
            age=float(form["age"]),
            income=float(form["income"]),
            share=float(form["share"]),
            expenditure=float(form["expenditure"]),
            owner=form["owner"] == "1",
            selfemp=form["selfemp"] == "1",
            dependents=int(form["dependents"]),
            months=int(form["months"]),
            majorcards=int(form["majorcards"]),
            active=int(form["active"]),

            prediction=resultado["prediction"],
            probability=resultado["probability"],

            created_by=user
        )

        db.session.add(prediction)
        db.session.commit()
        ####################################################
        # Guarda TODAS las reglas que cubrieron la instancia
        ####################################################
        for rule in resultado["matched_rules"]:
            pattern = rule["pattern"]["Pattern"]
            confidence = rule["confidence"]
            support = rule["support"]
            score = rule["score"]
            ################################################
            # Una fila por explicación
            ################################################
            for text in rule["explanations"]:
                explanation = CreditRiskPredictionExplanation(
                    prediction_id=prediction.id,
                    pattern=pattern,
                    explanation=text,
                    confidence=confidence,
                    support=support,
                    score=score
                )

                db.session.add(explanation)

        db.session.commit()
        return prediction
    @staticmethod
    def get_predictions():
        rows = CreditRiskPrediction.query.order_by(CreditRiskPrediction.created_at.desc()).all()
        result = []
        for r in rows:
            result.append({
                "id": r.id,
                "created_at": r.created_at.strftime("%d/%m/%Y %H:%M"),
                "prediction": r.prediction,
                "probability": round(r.probability * 100,2),
                "created_by": r.created_by
            })

        return result
    @staticmethod
    def get_prediction(id):

        p = CreditRiskPrediction.query.get_or_404(id)
        explanations = (
            CreditRiskPredictionExplanation.query
            .filter_by(prediction_id=id)
            .all()
        )
        print(p)
        patterns = []
        for e in explanations:
            print(e.pattern)
            print(e.explanation)
            patterns.append({
                "pattern": e.pattern,
                "confidence": float(e.confidence),
                "support": e.support,
                "score": float(e.score),
                "prediction": e.prediction_id,
                "explanations": e.explanation
            })

        return {
            "id": p.id,
            "prediction": p.prediction,
            "probability": float(p.probability),
            "created_at": p.created_at.strftime("%d/%m/%Y %H:%M"),
            "created_by": p.created_by,
            "variables": {
                "Reports": p.reports,
                "Age": float(p.age),
                "Income": float(p.income),
                "Share": float(p.share),
                "Expenditure": float(p.expenditure),
                "Owner": p.owner,
                "Self Employment": p.selfemp,
                "Dependents": p.dependents,
                "Months": p.months,
                "Major Cards": p.majorcards,
                "Active Accounts": p.active
            },
            "patterns": patterns
        }
"""