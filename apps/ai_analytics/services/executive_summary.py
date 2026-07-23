from decimal import Decimal


class ExecutiveSummaryService:

    @classmethod
    def percentage_change(
        cls,
        first,
        last,
    ):

        first = Decimal(
            str(first or 0)
        )

        last = Decimal(
            str(last or 0)
        )

        if first == 0:

            if last == 0:
                return Decimal("0")

            return None

        return (
            (last - first)
            / abs(first)
        ) * 100

    @classmethod
    def money_status(
        cls,
        value,
    ):

        value = Decimal(
            str(value or 0)
        )

        if value > 0:
            return "positive"

        if value < 0:
            return "negative"

        return "zero"

    @classmethod
    def generate_trend_summary(
        cls,
        data: dict,
    ) -> dict:

        income = data.get(
            "income",
            {},
        )

        expense = data.get(
            "expense",
            {},
        )

        profit = data.get(
            "profit",
            {},
        )

        income_first = income.get(
            "first",
            0,
        )

        income_last = income.get(
            "last",
            0,
        )

        expense_first = expense.get(
            "first",
            0,
        )

        expense_last = expense.get(
            "last",
            0,
        )

        profit_first = profit.get(
            "first",
            0,
        )

        profit_last = profit.get(
            "last",
            0,
        )

        income_change_percent = (
            cls.percentage_change(
                income_first,
                income_last,
            )
        )

        expense_change_percent = (
            cls.percentage_change(
                expense_first,
                expense_last,
            )
        )

        profit_change_percent = (
            cls.percentage_change(
                profit_first,
                profit_last,
            )
        )

        findings = []

        risks = []

        recommendations = []

        if (
            Decimal(str(profit_last))
            < 0
        ):

            headline = (
                "ATM moliyaviy jihatdan "
                "zararli holatga o'tgan."
            )

            risks.append(
                "Yakuniy davrda sof moliyaviy "
                "natija manfiy."
            )

        elif (
            Decimal(str(profit_last))
            > 0
        ):

            headline = (
                "ATM ijobiy moliyaviy "
                "natija ko'rsatmoqda."
            )

        else:

            headline = (
                "ATM moliyaviy jihatdan "
                "nol natijaga yaqin."
            )

        if (
            Decimal(str(income_last))
            > Decimal(str(income_first))
        ):

            findings.append(
                "Daromad o'sgan."
            )

        elif (
            Decimal(str(income_last))
            < Decimal(str(income_first))
        ):

            findings.append(
                "Daromad kamaygan."
            )

        if (
            Decimal(str(expense_last))
            > Decimal(str(expense_first))
        ):

            findings.append(
                "Xarajatlar oshgan."
            )

            risks.append(
                "Xarajatlar daromadga "
                "nisbatan tezroq o'sgan bo'lishi mumkin."
            )

            recommendations.append(
                "Xarajatlarning o'sish sabablarini "
                "oyma-oy tekshirish."
            )

        if (
            Decimal(str(profit_last))
            < Decimal(str(profit_first))
        ):

            findings.append(
                "Sof moliyaviy natija pasaygan."
            )

        if not recommendations:

            recommendations.append(
                "Joriy moliyaviy trendni "
                "kuzatishda davom etish."
            )

        return {
            "headline": headline,

            "key_findings": findings,

            "positive_factors": [],

            "risk_factors": risks,

            "recommendations": recommendations,

            "income": {
                "first": income_first,

                "last": income_last,

                "change": (
                        income_last
                        - income_first
                ),

                "change_percent": (
                    income_change_percent
                ),

                "trend": (
                    "increasing"
                    if income_last > income_first
                    else "decreasing"
                    if income_last < income_first
                    else "stable"
                ),
            },

            "expense": {
                "first": expense_first,

                "last": expense_last,

                "change": (
                        expense_last
                        - expense_first
                ),

                "change_percent": (
                    expense_change_percent
                ),

                "trend": (
                    "increasing"
                    if expense_last > expense_first
                    else "decreasing"
                    if expense_last < expense_first
                    else "stable"
                ),
            },

            "profit": {
                "first": profit_first,

                "last": profit_last,

                "change": (
                        profit_last
                        - profit_first
                ),

                "change_percent": (
                    profit_change_percent
                ),

                "trend": (
                    "increasing"
                    if profit_last > profit_first
                    else "decreasing"
                    if profit_last < profit_first
                    else "stable"
                ),
            },

            "metrics": {
                "income_change_percent": (
                    income_change_percent
                ),

                "expense_change_percent": (
                    expense_change_percent
                ),

                "profit_change_percent": (
                    profit_change_percent
                ),
            },

            "status": cls.money_status(
                profit_last
            ),
        }