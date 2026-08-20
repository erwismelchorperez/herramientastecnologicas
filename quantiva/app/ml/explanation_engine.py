import re

from app.ml.variable_dictionary import VARIABLES
class ExplanationEngine:

    @staticmethod
    def explain_condition(condition):

        m = re.match(
            r"(\w+)\s*(<=|>=|<|>|==|!=)\s*(.*)",
            condition
        )

        if m is None:
            return condition

        variable = m.group(1)
        operator = m.group(2)
        value = m.group(3)

        info = VARIABLES.get(variable)

        if info is None:
            return condition

        text = info["description"]

        if operator == ">":

            return (
                f"{text.capitalize()} "
                f"es mayor que {value}."
            )

        if operator == ">=":

            return (
                f"{text.capitalize()} "
                f"es mayor o igual que {value}."
            )

        if operator == "<":

            return (
                f"{text.capitalize()} "
                f"es menor que {value}."
            )

        if operator == "<=":

            return (
                f"{text.capitalize()} "
                f"es menor o igual que {value}."
            )

        if operator == "==":

            return (
                f"{text.capitalize()} "
                f"es igual a {value}."
            )

        if operator == "!=":

            return (
                f"{text.capitalize()} "
                f"es diferente de {value}."
            )

        return condition


    @staticmethod
    def explain_pattern(pattern):

        conditions = re.findall(
            r"\[(.*?)\]",
            pattern
        )

        explanation = []

        for cond in conditions:

            explanation.append(

                ExplanationEngine.explain_condition(cond)

            )

        return explanation