from __future__ import annotations

from decimal import Decimal
from typing import Any


class FinancialStoryEngine:

    @classmethod
    def build(
        cls,
        data: dict[str, Any],
    ) -> dict[str, Any]:

        monthly = data.get(
            "monthly_data",
            [],
        )

        if not monthly:
            return {
                "title": "Financial Story",
                "text": (
                    "Trend bo'yicha ma'lumot topilmadi."
                ),
                "sections": [],
            }

        sections = []

        for index, item in enumerate(monthly):

            sections.append(
                cls.describe_month(
                    item=item,
                    previous=(
                        monthly[index - 1]
                        if index > 0
                        else None
                    ),
                )
            )

        summary = cls.build_summary(
            monthly
        )

        return {
            "title": "Financial Story",
            "sections": sections,
            "summary": summary,
        }
    @classmethod
    def build_summary(
        cls,
        monthly,
    ):
        if not monthly:
            return "Trend ma'lumotlari mavjud emas."

        first = monthly[0]
        last = monthly[-1]

        income_first = Decimal(str(first.get("income", 0)))
        income_last = Decimal(str(last.get("income", 0)))

        expense_first = Decimal(str(first.get("expense", 0)))
        expense_last = Decimal(str(last.get("expense", 0)))

        profit_first = Decimal(str(first.get("profit", 0)))
        profit_last = Decimal(str(last.get("profit", 0)))

        income_change = income_last - income_first
        expense_change = expense_last - expense_first
        profit_change = profit_last - profit_first

        lines = []

        lines.append(
            f"Tahlil {len(monthly)} oylik davrni qamrab oladi."
        )

        if income_change > 0:
            lines.append(
                f"Daromad {income_change:,.2f} so'mga oshgan."
            )
        elif income_change < 0:
            lines.append(
                f"Daromad {abs(income_change):,.2f} so'mga kamaygan."
            )
        else:
            lines.append(
                "Daromad o'zgarmagan."
            )

        if expense_change > 0:
            lines.append(
                f"Xarajat {expense_change:,.2f} so'mga oshgan."
            )
        elif expense_change < 0:
            lines.append(
                f"Xarajat {abs(expense_change):,.2f} so'mga kamaygan."
            )
        else:
            lines.append(
                "Xarajat o'zgarmagan."
            )

        if profit_change > 0:
            lines.append(
                f"Sof foyda {profit_change:,.2f} so'mga yaxshilangan."
            )
        elif profit_change < 0:
            lines.append(
                f"Sof foyda {abs(profit_change):,.2f} so'mga kamaygan."
            )
        else:
            lines.append(
                "Sof foyda o'zgarmagan."
            )

        return "\n".join(lines)

    @classmethod
    def describe_month(
        cls,
        item,
        previous=None,
    ):

        income = Decimal(
            str(
                item.get(
                    "income",
                    0,
                )
            )
        )

        expense = Decimal(
            str(
                item.get(
                    "expense",
                    0,
                )
            )
        )

        profit = Decimal(
            str(
                item.get(
                    "profit",
                    0,
                )
            )
        )

        year = item["year"]
        month = item["month"]

        lines = []

        lines.append(
            f"{year}-{month:02d}"
        )

        lines.append("")

        lines.append(
            f"Daromad: {income:,.2f} so'm"
        )

        if expense == 0:

            lines.append(
                "Xarajat qayd etilmagan."
            )

        else:

            lines.append(
                f"Xarajat: {expense:,.2f} so'm"
            )

        lines.append(
            f"Sof natija: {profit:,.2f} so'm"
        )
        if previous:

            previous_income = Decimal(
                str(
                    previous.get(
                        "income",
                        0,
                    )
                )
            )

            previous_expense = Decimal(
                str(
                    previous.get(
                        "expense",
                        0,
                    )
                )
            )

            previous_profit = Decimal(
                str(
                    previous.get(
                        "profit",
                        0,
                    )
                )
            )

            income_change = (
                income
                - previous_income
            )
            income_percent = cls.percent_change(
                previous_income,
                income,
            )

            expense_percent = cls.percent_change(
                previous_expense,
                expense,
            )

            profit_percent = cls.percent_change(
                previous_profit,
                profit,
            )

            expense_change = (
                expense
                - previous_expense
            )

            profit_change = (
                profit
                - previous_profit
            )
            lines.append("")

            if income_change > 0:

                if income_percent is None:

                    lines.append(
                        f"Daromad {income_change:,.2f} so'mga oshgan."
                    )

                else:

                    lines.append(
                        f"Daromad {income_change:,.2f} so'mga "
                        f"({income_percent:.2f}%) oshgan."
                    )

            elif income_change < 0:

                lines.append(
                    f"Daromad {abs(income_change):,.2f} so'mga "
                    f"({abs(income_percent):.2f}%) kamaygan."
                )

            else:

                lines.append(
                    "Daromad o'zgarmagan."
                )
            if expense_change > 0:

                if expense_percent is None:

                    lines.append(
                        f"Xarajat {expense_change:,.2f} so'mga oshgan."
                    )

                else:

                    lines.append(
                        f"Xarajat {expense_change:,.2f} so'mga "
                        f"({expense_percent:.2f}%) oshgan."
                    )
            if profit_change > 0:

                lines.append(
                    f"Sof natija "
                    f"{profit_change:,.2f} so'mga "
                    f"({profit_percent:.2f}%) yaxshilangan."
                )

            else:

                lines.append(
                    f"Sof natija "
                    f"{abs(profit_change):,.2f} so'mga "
                    f"({abs(profit_percent):.2f}%) yomonlashgan."
                )
            if (
                    expense > income * 10
            ):
                lines.append("")

                lines.append(
                    "Xulosa:"
                )

                lines.append(
                    "Xarajat daromaddan keskin yuqori."
                )

                lines.append(
                    "Bu ATMning zarar bilan ishlashiga asosiy sabab bo'lishi mumkin."
                )
            elif (
                    profit > 0
            ):

                lines.append("")

                lines.append(
                    "ATM foyda bilan ishlamoqda."
                )
            else:

                lines.append("")

                lines.append(
                    "ATM zarar bilan ishlamoqda."
                )
            return {
                "period": (
                    f"{year}-{month:02d}"
                ),
                "text": "\n".join(
                    lines
                ),
                "income": income,
                "expense": expense,
                "profit": profit,
            }
    @classmethod
    def percent_change(
        cls,
        previous,
        current,
    ):

        previous = Decimal(str(previous))

        current = Decimal(str(current))

        if previous == 0:

            return None

        return (
            (
                current - previous
            )
            / previous
        ) * 100
