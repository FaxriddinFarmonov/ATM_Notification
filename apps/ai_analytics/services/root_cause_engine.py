from decimal import Decimal


class RootCauseEngine:

    @classmethod
    def analyze(
        cls,
        metrics: dict,
    ) -> dict:
        income = metrics["income"]

        expense = metrics["expense"]

        profit = metrics["profit"]
        income_score = abs(
            income["difference"]
        )

        expense_score = abs(
            expense["difference"]
        )

        profit_score = abs(
            profit["difference"]
        )
        total = (
                income_score
                +
                expense_score
        )
        income_percent = (
                                 income_score
                                 / total
                         ) * 100

        expense_percent = (
                                  expense_score
                                  / total
                          ) * 100
        causes = []
        causes.append({

            "factor": "expense",

            "impact_percent": round(
                float(expense_percent),
                2,
            ),

            "impact_value": expense_score,

            "priority": 1,
        })
        causes.append({

            "factor": "income",

            "impact_percent": round(
                float(income_percent),
                2,
            ),

            "impact_value": income_score,

            "priority": 2,
        })
        causes = sorted(

            causes,

            key=lambda x:
            x["impact_percent"],

            reverse=True,
        )
        return {

            "main_reason": causes[0],

            "causes": causes,

            "profit_status": profit["status"],

            "profit_change": profit["difference"],
        }