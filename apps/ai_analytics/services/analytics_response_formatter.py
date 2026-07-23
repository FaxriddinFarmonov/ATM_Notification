from __future__ import annotations
from .executive_summary import (
    ExecutiveSummaryService
)
from .executive_report import (
    ExecutiveReportFormatter,
)

from decimal import Decimal, InvalidOperation
from typing import Any


class AnalyticsResponseFormatter:

    MONTH_NAMES = {
        1: "Yanvar",
        2: "Fevral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "Iyun",
        7: "Iyul",
        8: "Avgust",
        9: "Sentabr",
        10: "Oktabr",
        11: "Noyabr",
        12: "Dekabr",
    }
    @classmethod
    def format_percent(cls, value):
        if value is None:
            return "0.00%"

        return f"{Decimal(str(value)):,.2f}%"

    @classmethod
    def calculate_change_percent(cls, first, last):
        first = Decimal(str(first or 0))
        last = Decimal(str(last or 0))

        if first == 0:
            if last == 0:
                return Decimal("0")

            return Decimal("100")

        return ((last - first) / abs(first)) * 100

    @classmethod
    def trend_icon(cls, trend):
        return {
            "increasing": "📈",
            "decreasing": "📉",
            "stable": "➡️",
        }.get(trend, "➡️")

    # =====================================================
    # MAIN DISPATCHER
    # =====================================================

    @classmethod
    def format(
            cls,
            result: dict[str, Any] | None,
            intent: str | None = None,
            question: str | None = None,
    ) -> dict[str, Any]:

        if not result:
            return {
                "type": "empty",
                "text": (
                    "🔍 Savol bo'yicha ma'lumot topilmadi.\n\n"
                    "Boshqa parametrlar bilan qayta urinib ko'ring."
                ),
                "data": {},
            }

        if intent == "count_by_region":
            return cls.format_count_by_region(
                result
            )

        elif intent == "revenue_by_region":
            return cls.format_revenue_by_region(
                result
            )

        elif intent == "performance_by_atm":
            return cls.format_performance_by_atm(
                result
            )

        elif intent == "monthly_trend":
            return cls.format_monthly_trend(
                result
            )

        elif intent == "trend_analysis":
            return cls.format_trend_analysis(
                result
            )

        return cls.format_generic(
            result
        )
    # =====================================================
    # COMMON
    # =====================================================

    @classmethod
    def to_decimal(
        cls,
        value: Any,
    ) -> Decimal:

        if value is None:

            return Decimal("0")

        if isinstance(
            value,
            Decimal,
        ):

            return value

        try:

            return Decimal(
                str(value)
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError,
        ):

            return Decimal("0")

    @classmethod
    def format_currency(
        cls,
        value: Any,
    ) -> str:

        value = cls.to_decimal(
            value
        )

        return f"{value:,.2f} so'm"

    @classmethod
    def format_integer(
        cls,
        value: Any,
    ) -> str:

        if value is None:

            return "0"

        try:

            return f"{int(value):,}"

        except (
            ValueError,
            TypeError,
        ):

            return "0"

    @classmethod
    def month_label(
        cls,
        year: int,
        month: int,
    ) -> str:

        return (
            f"{cls.MONTH_NAMES.get(month, month)} "
            f"{year}"
        )

    @classmethod
    def trend_icon(
        cls,
        trend: str | None,
    ) -> str:

        icons = {
            "increasing": "📈",
            "decreasing": "📉",
            "stable": "➡️",
        }

        return icons.get(
            trend,
            "📊",
        )


    @classmethod
    def format_count_by_region(
        cls,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        region = result.get(
            "region",
            "Noma'lum",
        )

        total_atms = result.get(
            "total_atms",
            0,
        )

        text = (
            "🏧 ATM HISOBOTI\n\n"
            f"📍 Region: {region}\n"
            f"🔢 Jami bankomatlar: "
            f"{cls.format_integer(total_atms)} ta\n\n"
            "📊 XULOSA\n\n"
            f"{region} regionida jami "
            f"{cls.format_integer(total_atms)} ta "
            "bankomat mavjud."
        )

        return {
            "type": "summary",
            "text": text,
            "data": result,
        }

    # =====================================================
    # REVENUE BY REGION
    # =====================================================

    @classmethod
    def format_revenue_by_region(
        cls,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        region = result.get(
            "region",
            "Noma'lum",
        )

        income = cls.to_decimal(
            result.get(
                "income",
                0,
            )
        )

        expense = cls.to_decimal(
            result.get(
                "expense",
                0,
            )
        )

        profit = cls.to_decimal(
            result.get(
                "profit",
                0,
            )
        )

        if profit > 0:

            profit_status = "📈 FOYDA"

            conclusion = (
                "Ushbu region ijobiy moliyaviy "
                "natija ko'rsatmoqda."
            )

        elif profit < 0:

            profit_status = "📉 ZARAR"

            conclusion = (
                "Ushbu regionda xarajatlar "
                "daromaddan yuqori."
            )

        else:

            profit_status = "➡️ NOL"

            conclusion = (
                "Daromad va xarajatlar o'rtasida "
                "farq mavjud emas."
            )

        text = (
            "💰 MOLIYAVIY TAHLIL\n\n"
            f"📍 Region: {region}\n\n"

            "━━━━━━━━━━━━━━━━━━\n"

            "💵 DAROMAD\n"
            f"{cls.format_currency(income)}\n\n"

            "💸 XARAJAT\n"
            f"{cls.format_currency(expense)}\n\n"

            f"{profit_status}\n"
            f"{cls.format_currency(profit)}\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "🧠 XULOSA\n\n"

            f"{conclusion}"
        )

        return {
            "type": "financial_report",
            "text": text,
            "data": result,
        }

    # =====================================================
    # PERFORMANCE BY ATM
    # =====================================================

    @classmethod
    def format_performance_by_atm(
        cls,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        if not result.get(
            "found"
        ):

            return {
                "type": "not_found",
                "text": (
                    "🔍 ATM topilmadi.\n\n"
                    "Berilgan identifikator bo'yicha "
                    "bazada ma'lumot mavjud emas."
                ),
                "data": result,
            }

        atm = result.get(
            "atm",
            {},
        )

        finance = result.get(
            "finance",
            {},
        )

        maintenance = result.get(
            "maintenance",
            {},
        )

        profit = cls.to_decimal(
            finance.get(
                "profit",
                0,
            )
        )

        if profit > 0:

            financial_status = (
                "📈 ATM moliyaviy jihatdan foydali."
            )

        elif profit < 0:

            financial_status = (
                "📉 ATM xarajatlari daromadidan yuqori."
            )

        else:

            financial_status = (
                "➡️ ATM bo'yicha moliyaviy natija nol."
            )

        text = (
            "🏧 ATM TO'LIQ TAHLILI\n\n"

            f"🆔 ID: {atm.get('id', 'Nomaʼlum')}\n"
            f"📍 Nomi: {atm.get('name', 'Nomaʼlum')}\n"
            f"🌍 Region: {atm.get('region', 'Nomaʼlum')}\n"
            f"⚙️ Model: {atm.get('model', 'Nomaʼlum')}\n"
            f"💳 Card type: {atm.get('card_type', 'Nomaʼlum')}\n"
            f"🔧 Status: {atm.get('status', 'Nomaʼlum')}\n\n"

            "━━━━━━━━━━━━━━━━━━\n"

            "💰 MOLIYAVIY KO'RSATKICHLAR\n\n"

            f"💵 Daromad: "
            f"{cls.format_currency(finance.get('income', 0))}\n"

            f"💸 Xarajat: "
            f"{cls.format_currency(finance.get('expense', 0))}\n"

            f"📊 Sof natija: "
            f"{cls.format_currency(finance.get('profit', 0))}\n\n"

            "━━━━━━━━━━━━━━━━━━\n"

            "🛠 TEXNIK XIZMAT\n\n"

            f"🔧 Remontlar soni: "
            f"{cls.format_integer(maintenance.get('repair_count', 0))} ta\n"

            f"💰 Remont xarajati: "
            f"{cls.format_currency(maintenance.get('repair_cost', 0))}\n\n"

            "🧠 ANALITIK XULOSA\n\n"

            f"{financial_status}"
        )

        return {
            "type": "atm_performance",
            "text": text,
            "data": result,
        }

    # =====================================================
    # MONTHLY TREND
    # =====================================================

    @classmethod
    def format_monthly_trend(
        cls,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        months = result.get(
            "months",
            [],
        )

        chart_data = []

        text_lines = [
            "📊 OYLIK MOLIYAVIY TAHLIL",
            "",
        ]

        for item in months:

            year = item.get(
                "year",
                0,
            )

            month = item.get(
                "month",
                0,
            )

            label = cls.month_label(
                year,
                month,
            )

            income = item.get(
                "income",
                0,
            )

            expense = item.get(
                "expense",
                0,
            )

            profit = item.get(
                "profit",
                0,
            )

            chart_data.append(
                {
                    "label": label,
                    "income": float(
                        cls.to_decimal(
                            income
                        )
                    ),
                    "expense": float(
                        cls.to_decimal(
                            expense
                        )
                    ),
                    "profit": float(
                        cls.to_decimal(
                            profit
                        )
                    ),
                }
            )

            text_lines.extend(
                [
                    f"📅 {label}",

                    f"   💰 Daromad: "
                    f"{cls.format_currency(income)}",

                    f"   💸 Xarajat: "
                    f"{cls.format_currency(expense)}",

                    f"   📊 Sof natija: "
                    f"{cls.format_currency(profit)}",

                    "",
                ]
            )

        return {
            "type": "monthly_trend",
            "text": "\n".join(
                text_lines
            ),
            "data": result,
            "chart": {
                "type": "line",
                "x_key": "label",
                "series": [
                    {
                        "key": "income",
                        "label": "Daromad",
                    },
                    {
                        "key": "expense",
                        "label": "Xarajat",
                    },
                    {
                        "key": "profit",
                        "label": "Sof natija",
                    },
                ],
                "data": chart_data,
            },
        }

    # =====================================================
    # TREND ANALYSIS
    # =====================================================


    @classmethod
    def format_generic(
        cls,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        lines = [
            "📊 ANALITIK HISOBOT",
            "",
        ]

        for key, value in result.items():

            label = (
                key
                .replace(
                    "_",
                    " ",
                )
                .title()
            )

            lines.append(
                f"🔹 {label}: {value}"
            )

        return {
            "type": "generic",
            "text": "\n".join(
                lines
            ),
            "data": result,
        }

    @classmethod
    def format_trend_analysis(
            cls,
            result: dict[str, Any],
    ) -> dict[str, Any]:

        income = result.get(
            "income",
            {},
        )

        expense = result.get(
            "expense",
            {},
        )

        profit = result.get(
            "profit",
            {},
        )

        period = result.get(
            "period",
            {},
        )

        period_from = period.get(
            "from",
            {},
        )

        period_to = period.get(
            "to",
            {},
        )

        from_label = cls.month_label(
            period_from.get(
                "year",
                0,
            ),
            period_from.get(
                "month",
                0,
            ),
        )

        to_label = cls.month_label(
            period_to.get(
                "year",
                0,
            ),
            period_to.get(
                "month",
                0,
            ),
        )

        income_trend = income.get(
            "trend",
            "stable",
        )

        expense_trend = expense.get(
            "trend",
            "stable",
        )

        profit_trend = profit.get(
            "trend",
            "stable",
        )

        income_change = income.get(
            "change",
            Decimal("0"),
        )

        expense_change = expense.get(
            "change",
            Decimal("0"),
        )

        profit_change = profit.get(
            "change",
            Decimal("0"),
        )

        first_income = income.get(
            "first",
            Decimal("0"),
        )

        last_income = income.get(
            "last",
            Decimal("0"),
        )

        first_expense = expense.get(
            "first",
            Decimal("0"),
        )

        last_expense = expense.get(
            "last",
            Decimal("0"),
        )

        first_profit = profit.get(
            "first",
            Decimal("0"),
        )

        last_profit = profit.get(
            "last",
            Decimal("0"),
        )

        monthly_data = result.get(
            "monthly_data",
            [],
        )

        table_rows = []

        chart_data = []

        for item in monthly_data:
            year = item.get(
                "year",
                0,
            )

            month = item.get(
                "month",
                0,
            )

            income_value = item.get(
                "income",
                Decimal("0"),
            )

            expense_value = item.get(
                "expense",
                Decimal("0"),
            )

            profit_value = item.get(
                "profit",
                Decimal("0"),
            )

            label = cls.month_label(
                year,
                month,
            )

            table_rows.append(
                {
                    "period": label,
                    "income": cls.format_currency(
                        income_value,
                    ),
                    "expense": cls.format_currency(
                        expense_value,
                    ),
                    "profit": cls.format_currency(
                        profit_value,
                    ),
                }
            )

            chart_data.append(
                {
                    "label": label,
                    "income": float(
                        income_value,
                    ),
                    "expense": float(
                        expense_value,
                    ),
                    "profit": float(
                        profit_value,
                    ),
                }
            )

        text = (
            "📈 MOLIYAVIY TREND TAHLILI\n\n"

            f"📅 Davr: "
            f"{from_label} — {to_label}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "💰 DAROMAD\n"
            f"Boshlang'ich: "
            f"{cls.format_currency(first_income)}\n"
            f"Yakuniy: "
            f"{cls.format_currency(last_income)}\n"
            f"O'zgarish: "
            f"{cls.format_currency(income_change)}\n\n"

            "💸 XARAJAT\n"
            f"Boshlang'ich: "
            f"{cls.format_currency(first_expense)}\n"
            f"Yakuniy: "
            f"{cls.format_currency(last_expense)}\n"
            f"O'zgarish: "
            f"{cls.format_currency(expense_change)}\n\n"

            "📊 SOF NATIJA\n"
            f"Boshlang'ich: "
            f"{cls.format_currency(first_profit)}\n"
            f"Yakuniy: "
            f"{cls.format_currency(last_profit)}\n"
            f"O'zgarish: "
            f"{cls.format_currency(profit_change)}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "🧠 ANALITIK XULOSA\n\n"
        )

        insights = []

        if (
                income_trend == "increasing"
                and profit_trend == "increasing"
        ):

            insights.append(
                "📈 Daromad va sof moliyaviy natija "
                "ijobiy dinamikani ko'rsatmoqda."
            )

        elif (
                expense_trend == "increasing"
                and income_trend != "increasing"
        ):

            insights.append(
                "⚠️ Xarajatlar oshgan, ammo daromad "
                "xarajatlar o'sishini qoplamayapti."
            )

        elif profit_trend == "decreasing":

            insights.append(
                "📉 Sof moliyaviy natija pasaygan. "
                "Xarajatlar va daromad o'rtasidagi "
                "nisbatni qo'shimcha tahlil qilish kerak."
            )

        else:

            insights.append(
                "📊 Moliyaviy ko'rsatkichlarda "
                "aralash dinamika kuzatilmoqda."
            )

        text += "\n".join(
            insights
        )

        summary = cls.build_trend_summary(
            result
        )
        executive_report = (
            ExecutiveReportFormatter
            .build(
                summary=summary,
                data=result,
            )
        )

        return {
            "type": "trend_analysis",

            "text": text,

            "table": {
                "title": "Oylik moliyaviy ko'rsatkichlar",

                "columns": [
                    {
                        "key": "period",
                        "label": "Davr",
                    },
                    {
                        "key": "income",
                        "label": "Daromad",
                    },
                    {
                        "key": "expense",
                        "label": "Xarajat",
                    },
                    {
                        "key": "profit",
                        "label": "Sof natija",
                    },
                ],

                "rows": table_rows,
            },

            "chart": {
                "type": "line",

                "title": "ATM moliyaviy dinamikasi",

                "x_key": "label",

                "series": [
                    {
                        "key": "income",
                        "label": "Daromad",
                    },
                    {
                        "key": "expense",
                        "label": "Xarajat",
                    },
                    {
                        "key": "profit",
                        "label": "Sof natija",
                    },
                ],

                "data": chart_data,
            },

            "insights": insights,

            "summary": summary,

            "executive_report": executive_report,

            "data": result,
        }
    @classmethod
    def build_trend_table(
            cls,
            result: dict,
    ) -> dict:

        monthly_data = result.get(
            "monthly_data",
            []
        )

        rows = []

        for item in monthly_data:
            year = item.get(
                "year"
            )

            month = item.get(
                "month"
            )

            income = item.get(
                "income",
                Decimal("0")
            )

            expense = item.get(
                "expense",
                Decimal("0")
            )

            profit = item.get(
                "profit",
                Decimal("0")
            )

            rows.append({

                "period": cls.month_label(
                    year,
                    month,
                ),

                "income": cls.format_currency(
                    income
                ),

                "expense": cls.format_currency(
                    expense
                ),

                "profit": cls.format_currency(
                    profit
                ),

            })

        return {

            "columns": [

                {
                    "key": "period",
                    "label": "Davr",
                },

                {
                    "key": "income",
                    "label": "Daromad",
                },

                {
                    "key": "expense",
                    "label": "Xarajat",
                },

                {
                    "key": "profit",
                    "label": "Sof natija",
                },

            ],

            "rows": rows,

        }

    @classmethod
    def build_trend_chart(
            cls,
            result: dict,
    ) -> dict:

        monthly_data = result.get(
            "monthly_data",
            []
        )

        data = []

        for item in monthly_data:
            data.append({

                "label": cls.month_label(
                    item["year"],
                    item["month"],
                ),

                "income": float(
                    item.get(
                        "income",
                        0,
                    )
                ),

                "expense": float(
                    item.get(
                        "expense",
                        0,
                    )
                ),

                "profit": float(
                    item.get(
                        "profit",
                        0,
                    )
                ),

            })

        return {

            "type": "line",

            "x_key": "label",

            "series": [

                {
                    "key": "income",
                    "label": "Daromad",
                },

                {
                    "key": "expense",
                    "label": "Xarajat",
                },

                {
                    "key": "profit",
                    "label": "Sof natija",
                },

            ],

            "data": data,

        }

    @classmethod
    def build_trend_text(
            cls,
            *,
            summary: dict,
    ) -> str:

        period = summary.get("period", {})

        period_from = period.get("from", {})
        period_to = period.get("to", {})

        from_label = cls.month_label(
            period_from.get("year", 0),
            period_from.get("month", 0),
        )

        to_label = cls.month_label(
            period_to.get("year", 0),
            period_to.get("month", 0),
        )

        income = summary.get("income", {})

        expense = summary.get("expense", {})

        profit = summary.get("profit", {})

        income_first = income.get(
            "first",
            Decimal("0"),
        )

        income_last = income.get(
            "last",
            Decimal("0"),
        )

        income_change = income.get(
            "change",
            Decimal("0"),
        )

        expense_first = expense.get(
            "first",
            Decimal("0"),
        )

        expense_last = expense.get(
            "last",
            Decimal("0"),
        )

        expense_change = expense.get(
            "change",
            Decimal("0"),
        )

        profit_first = profit.get(
            "first",
            Decimal("0"),
        )

        profit_last = profit.get(
            "last",
            Decimal("0"),
        )

        profit_change = profit.get(
            "change",
            Decimal("0"),
        )

        income_trend = income.get(
            "trend",
            "unknown",
        )

        expense_trend = expense.get(
            "trend",
            "unknown",
        )

        profit_trend = profit.get(
            "trend",
            "unknown",
        )

        text = (
            "📈 MOLIYAVIY TREND TAHLILI\n\n"

            f"📅 Davr: {from_label} — {to_label}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "💰 DAROMAD\n"
            f"Boshlang'ich: "
            f"{cls.format_currency(income_first)}\n"
            f"Yakuniy: "
            f"{cls.format_currency(income_last)}\n"
            f"O'zgarish: "
            f"{cls.format_currency(income_change)}\n"
            f"Trend: {income_trend}\n\n"

            "💸 XARAJAT\n"
            f"Boshlang'ich: "
            f"{cls.format_currency(expense_first)}\n"
            f"Yakuniy: "
            f"{cls.format_currency(expense_last)}\n"
            f"O'zgarish: "
            f"{cls.format_currency(expense_change)}\n"
            f"Trend: {expense_trend}\n\n"

            "📊 SOF NATIJA\n"
            f"Boshlang'ich: "
            f"{cls.format_currency(profit_first)}\n"
            f"Yakuniy: "
            f"{cls.format_currency(profit_last)}\n"
            f"O'zgarish: "
            f"{cls.format_currency(profit_change)}\n"
            f"Trend: {profit_trend}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "🧠 ANALITIK XULOSA\n\n"
        )

        if profit_last < 0:

            text += (
                "📉 Yakuniy davrda ATM zarar bilan ishlagan.\n"
                "Xarajatlar daromaddan yuqori bo'lgan."
            )

        elif profit_last > 0:

            text += (
                "📈 Yakuniy davrda ATM ijobiy moliyaviy "
                "natija ko'rsatgan."
            )

        else:

            text += (
                "⚪ Yakuniy moliyaviy natija nolga teng."
            )

        return text
    @classmethod
    def build_trend_summary(
        cls,
        result: dict[str, Any],
    ) -> dict[str, Any]:

        income = result.get(
            "income",
            {},
        )

        expense = result.get(
            "expense",
            {},
        )

        profit = result.get(
            "profit",
            {},
        )

        monthly_data = result.get(
            "monthly_data",
            [],
        )

        income_trend = income.get(
            "trend",
            "stable",
        )

        expense_trend = expense.get(
            "trend",
            "stable",
        )

        profit_trend = profit.get(
            "trend",
            "stable",
        )

        last_profit = profit.get(
            "last",
            Decimal("0"),
        )

        first_profit = profit.get(
            "first",
            Decimal("0"),
        )

        best_month = None
        worst_month = None

        if monthly_data:

            best_month = max(
                monthly_data,
                key=lambda item: item.get(
                    "profit",
                    Decimal("0"),
                ),
            )

            worst_month = min(
                monthly_data,
                key=lambda item: item.get(
                    "profit",
                    Decimal("0"),
                ),
            )

        key_findings = []

        if income_trend == "increasing":

            key_findings.append(
                "Daromad davr oxiriga kelib oshgan."
            )

        elif income_trend == "decreasing":

            key_findings.append(
                "Daromad davr oxiriga kelib kamaygan."
            )

        if expense_trend == "increasing":

            key_findings.append(
                "Xarajatlar o'sish trendini ko'rsatmoqda."
            )

        elif expense_trend == "decreasing":

            key_findings.append(
                "Xarajatlar kamayish trendini ko'rsatmoqda."
            )

        if profit_trend == "decreasing":

            key_findings.append(
                "Sof moliyaviy natija pasaygan."
            )

        elif profit_trend == "increasing":

            key_findings.append(
                "Sof moliyaviy natija yaxshilangan."
            )

        positive_factors = []

        if income_trend == "increasing":

            positive_factors.append(
                "Daromadning o'sish dinamikasi mavjud."
            )

        if last_profit > 0:

            positive_factors.append(
                "So'nggi davr ijobiy moliyaviy natija bilan yakunlangan."
            )

        if not positive_factors:

            positive_factors.append(
                "Aniq ijobiy moliyaviy omil aniqlanmadi."
            )

        risk_factors = []

        if expense_trend == "increasing":

            risk_factors.append(
                "Xarajatlar oshmoqda."
            )

        if last_profit < 0:

            risk_factors.append(
                "So'nggi davrda ATM manfiy moliyaviy natija ko'rsatgan."
            )

        if not risk_factors:

            risk_factors.append(
                "Kritik moliyaviy risk aniqlanmadi."
            )

        recommendations = []

        if last_profit < 0:

            recommendations.append(
                "Xarajatlar tarkibini chuqur tahlil qilish."
            )

            recommendations.append(
                "Daromadni oshirish imkoniyatlarini ko'rib chiqish."
            )

        elif profit_trend == "increasing":

            recommendations.append(
                "Ijobiy moliyaviy trendni saqlab qolish."
            )

        else:

            recommendations.append(
                "ATM moliyaviy ko'rsatkichlarini muntazam monitoring qilish."
            )

        if last_profit > first_profit:

            headline = (
                "ATM moliyaviy natijasi ijobiy tomonga o'zgargan."
            )

        elif last_profit < first_profit:

            headline = (
                "ATM moliyaviy natijasi yomonlashgan va qo'shimcha tahlil talab qiladi."
            )

        else:

            headline = (
                "ATM moliyaviy natijasida sezilarli o'zgarish kuzatilmagan."
            )

        return {
            "headline": headline,

            "key_findings": key_findings,

            "positive_factors": positive_factors,

            "risk_factors": risk_factors,

            "recommendations": recommendations,

            "best_month": best_month,

            "worst_month": worst_month,
        }