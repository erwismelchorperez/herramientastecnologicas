import json
import re
from app.ml.explanation_engine import ExplanationEngine

class PatternClassifier:

    def __init__(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            self.patterns = json.load(f)

    def split_pattern(self, pattern):
        return re.findall(r"\[(.*?)\]", pattern)

    def evaluate_condition(self, condition, sample):

        m = re.match(
            r"^\s*(\w+)\s*(<=|>=|<|>|==|=|!=)\s*(.*?)\s*$",
            condition
        )

        if m is None:
            return False

        feature = m.group(1)
        operator = m.group(2)
        value = m.group(3).strip()

        if feature not in sample:
            return False

        x = sample[feature]

        try:
            x_num = float(x)
            value_num = float(value)
            numeric = True
        except (ValueError, TypeError):
            numeric = False

        if numeric:
            if operator == "<":
                return x_num < value_num

            if operator == "<=":
                return x_num <= value_num

            if operator == ">":
                return x_num > value_num

            if operator == ">=":
                return x_num >= value_num

            if operator in ("==","="):
                return x_num == value_num

            if operator == "!=":
                return x_num != value_num

        else:
            x_text = str(x).strip().upper()
            value_text = value.strip().strip("'\"").upper()

            if operator in ("==","="):
                return x_text == value_text

            if operator == "!=":
                return x_text != value_text

        return False
    def pattern_matches(self, pattern, sample):

        conditions = self.split_pattern(pattern)

        print("\nPATTERN:", pattern)

        for condition in conditions:

            result = self.evaluate_condition(
                condition,
                sample
            )

            print(
                f"  {condition} -> {result}"
            )

            if not result:
                return False

        return True
    """
    def pattern_matches(self, pattern, sample):

        conditions = self.split_pattern(pattern)

        if not conditions:
            return False

        for condition in conditions:
            if not self.evaluate_condition(
                condition,
                sample
            ):
                return False

        return True
    """

    def confidence(self, pattern):

        neg = pattern["negative Count"]
        pos = pattern["positive Count"]

        total = neg + pos

        if total == 0:
            return 0

        return max(neg, pos) / total

    def predict(self, sample):

        candidates = []

        for pattern in self.patterns:

            if not self.pattern_matches(
                pattern["Pattern"],
                sample
            ):
                continue

            length = len(
                self.split_pattern(
                    pattern["Pattern"]
                )
            )

            support = (
                pattern["negative Count"] +
                pattern["positive Count"]
            )

            confidence = self.confidence(pattern)

            score = (
                length *
                confidence *
                support
            )

            candidates.append({
                "pattern": pattern,
                "score": score,
                "length": length,
                "confidence": confidence,
                "support": support,
                "explanations": ExplanationEngine.explain_pattern(
                    pattern["Pattern"]
                )
            })

        if not candidates:
            return {
                "prediction": None,
                "probability": 0,
                "matched_pattern": None,
                "matched_rules": []
            }

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        best = candidates[0]

        neg = best["pattern"]["negative Count"]
        pos = best["pattern"]["positive Count"]

        total = neg + pos

        if neg >= pos:
            prediction = "negative"
            probability = neg / total
        else:
            prediction = "positive"
            probability = pos / total

        return {
            "prediction": prediction,
            "probability": probability,
            "matched_pattern": best,
            "matched_rules": candidates
        }

"""
class PatternClassifier:

    def __init__(self, json_path):

        with open(json_path, "r", encoding="utf-8") as f:
            self.patterns = json.load(f)


    ####################################################################
    # Convierte
    #
    # [share > 0.001] ∧ [age <= 35]
    #
    # en
    #
    # ["share > 0.001",
    #  "age <= 35"]
    #
    ####################################################################
    def split_pattern(self, pattern):

        return re.findall(r"\[(.*?)\]", pattern)


    ####################################################################
    # Evalúa una condición
    ####################################################################
    def evaluate_condition(self, condition, sample):

        m = re.match(
            r"(\w+)\s*(<=|>=|<|>|==|!=)\s*(.*)",
            condition
        )

        if m is None:
            return False

        feature = m.group(1)

        operator = m.group(2)

        value = float(m.group(3))

        if feature not in sample:
            return False

        x = float(sample[feature])

        if operator == "<":
            return x < value

        if operator == "<=":
            return x <= value

        if operator == ">":
            return x > value

        if operator == ">=":
            return x >= value

        if operator == "==":
            return x == value

        if operator == "!=":
            return x != value

        return False


    ####################################################################
    # Evalúa si un patrón completo se cumple
    ####################################################################
    def pattern_matches(self, pattern, sample):

        conditions = self.split_pattern(pattern)

        for cond in conditions:

            if not self.evaluate_condition(cond, sample):
                return False

        return True


    ####################################################################
    # Confidence
    ####################################################################
    def confidence(self, p):

        neg = p["negative Count"]

        pos = p["positive Count"]

        total = neg + pos

        if total == 0:
            return 0

        return max(neg, pos) / total


    ####################################################################
    # Predicción
    ####################################################################
    def predict(self, sample):

        candidates = []

        for p in self.patterns:

            if self.pattern_matches(
                p["Pattern"],
                sample
            ):

                length = len(
                    self.split_pattern(
                        p["Pattern"]
                    )
                )

                support = (
                    p["negative Count"] +
                    p["positive Count"]
                )

                confidence = self.confidence(p)

                score = (
                    length *
                    confidence *
                    support
                )

                candidates.append(

                    {
                        "pattern": p,

                        "score": score,

                        "length": length,

                        "confidence": confidence,

                        "support": support,
                        "explanations": ExplanationEngine.explain_pattern(p["Pattern"])

                    }

                )

        if len(candidates) == 0:

            return {

                "prediction": None,

                "probability": 0,

                "matched_pattern": None

            }

        #######################################################

        candidates.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        best = candidates[0]#["pattern"]
        neg = best["pattern"]["negative Count"]
        pos = best["pattern"]["positive Count"]

        total = neg + pos

        if neg >= pos:

            prediction = "negative"

            probability = neg / total

        else:

            prediction = "positive"

            probability = pos / total

        return {

            "prediction": prediction,

            "probability": probability,

            "matched_pattern": best,

            "matched_rules": candidates

        }
"""