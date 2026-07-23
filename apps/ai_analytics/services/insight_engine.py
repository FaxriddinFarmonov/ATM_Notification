from decimal import Decimal


class InsightEngine:

    @classmethod
    def make_insight(
        cls,
        severity: str,
        insight_type: str,
        title: str,
        description: str,
        impact: str,
    ) -> dict:

        return {
            "severity": severity,
            "type": insight_type,
            "title": title,
            "description": description,
            "impact": impact,
        }

    @classmethod
    def analyze_trend(
        cls,
        data: dict,
    ) -> list[dict]:

        insights = []
        expense = data.get(
            "expense",
            {},
        )

        expense_first = Decimal(
            str(
                expense.get(
                    "first",
                    0,
                )
            )
        )

        expense_last = Decimal(
            str(
                expense.get(
                    "last",
                    0,
                )
            )
        )

        if expense_last > expense_first:
            insights.append(
                cls.make_insight(
                    severity="high",
                    insight_type="expense_growth",
                    title="Xarajatlar oshmoqda",
                    description=(
                        "ATM xarajatlari oldingi davrga "
                        "nisbatan oshgan."
                    ),
                    impact=(
                        "Profit kamayishiga sabab "
                        "bo'lishi mumkin."
                    ),
                )
            )
        profit = data.get(
            "profit",
            {},
        )

        profit_last = Decimal(
            str(
                profit.get(
                    "last",
                    0,
                )
            )
        )

        if profit_last < 0:
            insights.append(
                cls.make_insight(
                    severity="critical",
                    insight_type="negative_profit",
                    title="ATM zarar bilan ishlamoqda",
                    description=(
                        "Yakuniy sof moliyaviy natija "
                        "manfiy qiymatga tushgan."
                    ),
                    impact=(
                        "Operatsion samaradorlik "
                        "pasaymoqda."
                    ),
                )
            )
        income = data.get(
            "income",
            {},
        )

        income_first = Decimal(
            str(
                income.get(
                    "first",
                    0,
                )
            )
        )

        income_last = Decimal(
            str(
                income.get(
                    "last",
                    0,
                )
            )
        )

        if income_last > income_first:
            insights.append(
                cls.make_insight(
                    severity="low",
                    insight_type="income_growth",
                    title="Daromad oshmoqda",
                    description=(
                        "ATM daromadi ijobiy "
                        "dinamikani ko'rsatmoqda."
                    ),
                    impact=(
                        "Kelgusida profitni "
                        "yaxshilashi mumkin."
                    ),
                )
            )
        

        return insights