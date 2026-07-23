from decimal import Decimal


class ExecutiveReportFormatter:

    @classmethod
    def format_money(
        cls,
        value,
    ):
        value = Decimal(
            str(value or 0)
        )

        return (
            f"{value:,.2f}"
            " so'm"
        )

    @classmethod
    def format_percent(
        cls,
        value,
    ):
        if value is None:
            return "N/A"

        value = Decimal(
            str(value or 0)
        )

        sign = ""

        if value > 0:
            sign = "+"

        return (
            f"{sign}{value:,.2f}%"
        )

    @classmethod
    def month_label(
        cls,
        month_data,
    ):
        if not month_data:
            return "Noma'lum davr"

        year = month_data.get(
            "year",
            0,
        )

        month = month_data.get(
            "month",
            0,
        )

        months = {
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

        return (
            f"{months.get(month, 'Noma’lum')} "
            f"{year}"
        )

    @classmethod
    def build(
        cls,
        summary: dict,
        data: dict,
    ) -> dict:

        metrics = summary.get(
            "metrics",
            {},
        )

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

        best_month = summary.get(
            "best_month"
        )

        worst_month = summary.get(
            "worst_month"
        )

        headline = summary.get(
            "headline",
            "Moliyaviy tahlil yakunlandi.",
        )

        findings = summary.get(
            "key_findings",
            [],
        )

        positive_factors = summary.get(
            "positive_factors",
            [],
        )

        risks = summary.get(
            "risk_factors",
            [],
        )

        recommendations = summary.get(
            "recommendations",
            [],
        )

        text_lines = []

        text_lines.append(
            "🏢 EXECUTIVE ANALYTICS REPORT"
        )

        text_lines.append("")

        text_lines.append(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

        text_lines.append("")

        text_lines.append(
            f"🎯 {headline}"
        )

        text_lines.append("")

        text_lines.append(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

        text_lines.append("")

        text_lines.append(
            "📌 ASOSIY ANIQLANGAN HOLATLAR"
        )

        text_lines.append("")

        for index, item in enumerate(
            findings,
            start=1,
        ):

            text_lines.append(
                f"{index}. {item}"
            )

        text_lines.append("")

        text_lines.append(
            "📊 ASOSIY KO'RSATKICHLAR"
        )

        text_lines.append("")

        text_lines.append(
            "💰 Daromad"
        )

        text_lines.append(
            f"   Boshlang'ich: "
            f"{cls.format_money(income.get('first'))}"
        )

        text_lines.append(
            f"   Yakuniy: "
            f"{cls.format_money(income.get('last'))}"
        )

        text_lines.append(
            f"   O'zgarish: "
            f"{cls.format_percent(metrics.get('income_change_percent'))}"
        )

        text_lines.append("")

        text_lines.append(
            "💸 Xarajat"
        )

        text_lines.append(
            f"   Boshlang'ich: "
            f"{cls.format_money(expense.get('first'))}"
        )

        text_lines.append(
            f"   Yakuniy: "
            f"{cls.format_money(expense.get('last'))}"
        )

        text_lines.append(
            f"   O'zgarish: "
            f"{cls.format_percent(metrics.get('expense_change_percent'))}"
        )

        text_lines.append("")

        text_lines.append(
            "📈 Sof natija"
        )

        text_lines.append(
            f"   Boshlang'ich: "
            f"{cls.format_money(profit.get('first'))}"
        )

        text_lines.append(
            f"   Yakuniy: "
            f"{cls.format_money(profit.get('last'))}"
        )

        text_lines.append(
            f"   O'zgarish: "
            f"{cls.format_percent(metrics.get('profit_change_percent'))}"
        )

        text_lines.append("")

        text_lines.append(
            "✅ IJOBIY OMILLAR"
        )

        text_lines.append("")

        if positive_factors:

            for item in positive_factors:

                text_lines.append(
                    f"• {item}"
                )

        else:

            text_lines.append(
                "• Aniq ijobiy omillar aniqlanmadi."
            )

        text_lines.append("")

        text_lines.append(
            "⚠️ ASOSIY RISK VA MUAMMOLAR"
        )

        text_lines.append("")

        if risks:

            for item in risks:

                text_lines.append(
                    f"• {item}"
                )

        else:

            text_lines.append(
                "• Kritik risklar aniqlanmadi."
            )

        text_lines.append("")

        text_lines.append(
            "🏆 ENG YAXSHI DAVR"
        )

        text_lines.append("")

        if best_month:

            text_lines.append(
                f"📅 {cls.month_label(best_month)}"
            )

            text_lines.append(
                f"💰 Daromad: "
                f"{cls.format_money(best_month.get('income'))}"
            )

            text_lines.append(
                f"💸 Xarajat: "
                f"{cls.format_money(best_month.get('expense'))}"
            )

            text_lines.append(
                f"📊 Sof natija: "
                f"{cls.format_money(best_month.get('profit'))}"
            )

        else:

            text_lines.append(
                "Ma'lumot mavjud emas."
            )

        text_lines.append("")

        text_lines.append(
            "🔻 ENG ZAIF DAVR"
        )

        text_lines.append("")

        if worst_month:

            text_lines.append(
                f"📅 {cls.month_label(worst_month)}"
            )

            text_lines.append(
                f"💰 Daromad: "
                f"{cls.format_money(worst_month.get('income'))}"
            )

            text_lines.append(
                f"💸 Xarajat: "
                f"{cls.format_money(worst_month.get('expense'))}"
            )

            text_lines.append(
                f"📊 Sof natija: "
                f"{cls.format_money(worst_month.get('profit'))}"
            )

        else:

            text_lines.append(
                "Ma'lumot mavjud emas."
            )

        text_lines.append("")

        text_lines.append(
            "🎯 RAHBARIYAT UCHUN TAVSIYALAR"
        )

        text_lines.append("")

        for index, item in enumerate(
            recommendations,
            start=1,
        ):

            text_lines.append(
                f"{index}. {item}"
            )

        text_lines.append("")

        text_lines.append(
            "🧠 RAHBARIYAT UCHUN YAKUNIY XULOSA"
        )

        text_lines.append("")

        if risks:

            text_lines.append(
                "⚠️ Aniqlangan risklarni kamaytirish "
                "uchun qo'shimcha nazorat va "
                "operatsion tahlil tavsiya etiladi."
            )

        else:

            text_lines.append(
                "✅ ATM bo'yicha jiddiy moliyaviy "
                "risklar aniqlanmadi."
            )

        return {
            "type": "executive_report",

            "title": (
                "Executive Analytics Report"
            ),

            "status": "success",

            "text": "\n".join(
                text_lines
            ),

            "summary": summary,

            "data": data,
        }