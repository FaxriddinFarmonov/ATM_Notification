from decimal import Decimal
from typing import Any


class ExecutiveReportFormatter:

    # =====================================================
    # COMMON
    # =====================================================

    @staticmethod
    def _money(value: Any) -> str:
        if value is None:
            value = Decimal("0")

        value = Decimal(str(value))

        return f"{value:,.2f} so'm"

    @staticmethod
    def _percent(value: Any) -> str:
        if value is None:
            value = Decimal("0")

        value = Decimal(str(value))

        return f"{value:.2f}%"

    @staticmethod
    def _trend_icon(trend: str) -> str:
        icons = {
            "increasing": "📈",
            "decreasing": "📉",
            "stable": "➡️",
        }

        return icons.get(
            trend,
            "➡️",
        )

    # =====================================================
    # EXECUTIVE REPORT
    # =====================================================
@classmethod
def format(
    cls,
    summary: dict[str, Any],
) -> dict[str, Any]:

    if not summary:

        return {
            "type": "executive_report",
            "title": "Executive Report",
            "status": "empty",
            "text": (
                "📊 Executive hisobot uchun "
                "yetarli analitik ma'lumot mavjud emas."
            ),
            "sections": [],
        }

    headline = summary.get(
        "headline",
        "ATM analitik hisoboti",
    )

    key_findings = summary.get(
        "key_findings",
        [],
    )

    positive_factors = summary.get(
        "positive_factors",
        [],
    )

    risk_factors = summary.get(
        "risk_factors",
        [],
    )

    recommendations = summary.get(
        "recommendations",
        [],
    )

    metrics = summary.get(
        "metrics",
        {},
    )

    best_month = summary.get(
        "best_month",
    )

    worst_month = summary.get(
        "worst_month",
    )

    # =================================================
    # REAL METRICS
    # =================================================

    income = summary.get(
        "income",
        {},
    )

    expense = summary.get(
        "expense",
        {},
    )

    profit = summary.get(
        "profit",
        {},
    )

    def calculate_percent(
        first,
        last,
    ):

        first = Decimal(
            str(
                first or 0
            )
        )

        last = Decimal(
            str(
                last or 0
            )
        )

        if first == 0:

            if last > 0:
                return Decimal("100")

            if last < 0:
                return Decimal("-100")

            return Decimal("0")

        return (
            (last - first)
            / abs(first)
            * Decimal("100")
        )

    income_change_percent = calculate_percent(
        income.get(
            "first",
            0,
        ),
        income.get(
            "last",
            0,
        ),
    )

    expense_change_percent = calculate_percent(
        expense.get(
            "first",
            0,
        ),
        expense.get(
            "last",
            0,
        ),
    )

    profit_change_percent = calculate_percent(
        profit.get(
            "first",
            0,
        ),
        profit.get(
            "last",
            0,
        ),
    )

    metrics = {
        "income_change_percent":
            income_change_percent,

        "expense_change_percent":
            expense_change_percent,

        "profit_change_percent":
            profit_change_percent,
    }

    # =================================================
    # MONTH FORMATTER
    # =================================================

    month_names = {
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

    def format_month(
        month_data,
    ):

        if not month_data:

            return None

        year = month_data.get(
            "year",
            0,
        )

        month = month_data.get(
            "month",
            0,
        )

        profit_value = month_data.get(
            "profit",
            0,
        )

        return (
            f"{month_names.get(month, month)} "
            f"{year} — "
            f"{cls._money(profit_value)}"
        )

    best_month_label = format_month(
        best_month
    )

    worst_month_label = format_month(
        worst_month
    )

    # =================================================
    # TEXT
    # =================================================

    text_lines = [

        "🏢 EXECUTIVE ANALYTICS REPORT",

        "",

        "━━━━━━━━━━━━━━━━━━━━━━━━━━",

        "",

        f"🎯 {headline}",

        "",

        "━━━━━━━━━━━━━━━━━━━━━━━━━━",

        "",
    ]

    # =================================================
    # FINDINGS
    # =================================================

    if key_findings:

        text_lines.extend(
            [
                "📌 ASOSIY ANIQLANGAN HOLATLAR",
                "",
            ]
        )

        for index, finding in enumerate(
            key_findings,
            start=1,
        ):

            text_lines.append(
                f"{index}. {finding}"
            )

        text_lines.append("")

    # =================================================
    # METRICS
    # =================================================

    income_icon = cls._trend_icon(
        "increasing"
        if income_change_percent > 0
        else "decreasing"
        if income_change_percent < 0
        else "stable"
    )

    expense_icon = cls._trend_icon(
        "increasing"
        if expense_change_percent > 0
        else "decreasing"
        if expense_change_percent < 0
        else "stable"
    )

    profit_icon = cls._trend_icon(
        "increasing"
        if profit_change_percent > 0
        else "decreasing"
        if profit_change_percent < 0
        else "stable"
    )

    text_lines.extend(
        [
            "📊 ASOSIY KO'RSATKICHLAR",
            "",

            (
                f"💰 Daromad dinamikasi: "
                f"{cls._percent(income_change_percent)} "
                f"{income_icon}"
            ),

            (
                f"💸 Xarajat dinamikasi: "
                f"{cls._percent(expense_change_percent)} "
                f"{expense_icon}"
            ),

            (
                f"📈 Sof natija dinamikasi: "
                f"{cls._percent(profit_change_percent)} "
                f"{profit_icon}"
            ),

            "",
        ]
    )

    # =================================================
    # POSITIVE FACTORS
    # =================================================

    if positive_factors:

        text_lines.extend(
            [
                "✅ IJOBIY OMILLAR",
                "",
            ]
        )

        for factor in positive_factors:

            text_lines.append(
                f"• {factor}"
            )

        text_lines.append("")

    # =================================================
    # RISKS
    # =================================================

    if risk_factors:

        text_lines.extend(
            [
                "⚠️ ASOSIY RISK VA MUAMMOLAR",
                "",
            ]
        )

        for risk in risk_factors:

            text_lines.append(
                f"• {risk}"
            )

        text_lines.append("")

    # =================================================
    # BEST MONTH
    # =================================================

    if best_month_label:

        text_lines.extend(
            [
                "🏆 ENG YAXSHI DAVR",
                "",
                f"📅 {best_month_label}",
                "",
            ]
        )

    # =================================================
    # WORST MONTH
    # =================================================

    if worst_month_label:

        text_lines.extend(
            [
                "🔻 ENG ZAIF DAVR",
                "",
                f"📅 {worst_month_label}",
                "",
            ]
        )

    # =================================================
    # RECOMMENDATIONS
    # =================================================

    if recommendations:

        text_lines.extend(
            [
                "🎯 RAHBARIYAT UCHUN TAVSIYALAR",
                "",
            ]
        )

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            text_lines.append(
                f"{index}. {recommendation}"
            )

        text_lines.append("")

    # =================================================
    # FINAL DECISION
    # =================================================

    if risk_factors:

        decision = (
            "⚠️ Ushbu ATM bo'yicha aniqlangan "
            "risklarni kamaytirish uchun "
            "qo'shimcha nazorat va operatsion "
            "tahlil tavsiya etiladi."
        )

    elif recommendations:

        decision = (
            "✅ Umumiy ko'rsatkichlar asosida "
            "joriy holatni monitoring qilish va "
            "aniqlangan tavsiyalarni amalga oshirish "
            "tavsiya etiladi."
        )

    else:

        decision = (
            "ℹ️ Qo'shimcha qaror qabul qilishdan "
            "oldin kengaytirilgan analitik ma'lumot "
            "talab qilinadi."
        )

    text_lines.extend(
        [
            "🧠 RAHBARIYAT UCHUN YAKUNIY XULOSA",
            "",
            decision,
        ]
    )

    return {
        "type": "executive_report",

        "title": "Executive Analytics Report",

        "status": "success",

        "text": "\n".join(
            text_lines
        ),

        "sections": [

            {
                "type": "headline",
                "title": "Asosiy xulosa",
                "content": headline,
            },

            {
                "type": "findings",
                "title": "Asosiy aniqlangan holatlar",
                "items": key_findings,
            },

            {
                "type": "metrics",
                "title": "Asosiy ko'rsatkichlar",
                "data": metrics,
            },

            {
                "type": "positive_factors",
                "title": "Ijobiy omillar",
                "items": positive_factors,
            },

            {
                "type": "risks",
                "title": "Risklar",
                "items": risk_factors,
            },

            {
                "type": "recommendations",
                "title": "Tavsiyalar",
                "items": recommendations,
            },

        ],

        "summary": summary,
    }