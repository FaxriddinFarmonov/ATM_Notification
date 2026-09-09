from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.db.models import Sum

from ...services.atm_detail_queryset import ATMDetailQuerySet
from ...services.ollama_service import OllamaService
from ...services.prompt_builder import PromptBuilder


# --- Swagger Serializerlar ---
class ATMLineChartSerializer(serializers.Serializer):
    labels = serializers.ListField(
        child=serializers.CharField(),
        help_text="Oxirgi 6 oy ketma-ketligi (masalan: ['2025-10', '2025-11', ...])"
    )
    income = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Har bir oy bo'yicha bankning komissiya daromadi (so'mda)"
    )
    expense = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Har bir oy bo'yicha haqiqiy operatsion xarajatlar: servis + svet/ijara + ta'mir (so'mda)"
    )
    profit = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Har bir oy bo'yicha sof foyda: daromad - xarajatlar (so'mda)"
    )
    cash_withdrawn = serializers.ListField(
        child=serializers.FloatField(),
        required=False,
        help_text="Har bir oy bo'yicha mijozlar yechgan naqd pul aylanmasi (so'mda)"
    )


class ATMMonthlyRecordSerializer(serializers.Serializer):
    period = serializers.CharField()
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    cash_withdrawn = serializers.FloatField(help_text="Yechilgan naqd pul (aylanma)")
    income = serializers.FloatField(help_text="Yalpi komissiya daromadi")
    service_cost = serializers.FloatField(help_text="BTech + Glob xizmati")
    utility_cost = serializers.FloatField(help_text="Elektr, Ijara, Inkassatsiya")
    repair_cost = serializers.FloatField(help_text="Ta'mirlash va ehtiyot qismlar")
    total_expense = serializers.FloatField(help_text="Jami haqiqiy xarajatlar")
    net_profit = serializers.FloatField(help_text="Sof foyda")


class ATMMetricsSerializer(serializers.Serializer):
    total_income = serializers.FloatField(help_text="6 oylik jami komissiya daromadi (so'mda)")
    total_cash_withdrawn = serializers.FloatField(help_text="6 oylik jami yechilgan naqd pul aylanmasi (so'mda)")
    total_expense = serializers.FloatField(help_text="6 oylik jami haqiqiy xarajatlar (so'mda)")
    net_profit = serializers.FloatField(help_text="6 oylik sof foyda (so'mda)")
    average_income = serializers.FloatField(help_text="O'rtacha oylik daromad (so'mda)")
    average_cash_withdrawn = serializers.FloatField(help_text="O'rtacha oylik naqd pul aylanmasi (so'mda)")
    average_expense = serializers.FloatField(help_text="O'rtacha oylik haqiqiy xarajat (so'mda)")
    profitability_rate = serializers.FloatField(help_text="Rentabellik darajasi (%)")
    total_service_fee = serializers.FloatField(help_text="6 oylik jami servis to'lovi (so'mda)")
    total_utility_cost = serializers.FloatField(help_text="6 oylik jami elektr va ijara to'lovi (so'mda)")
    total_repair_cost = serializers.FloatField(help_text="6 oylik jami ta'mirlash xarajati (so'mda)")
    health_score = serializers.IntegerField(help_text="Sog'lomlik reytingi (0-100)")
    risk_level = serializers.CharField(help_text="Xavf darajasi (LOW, MEDIUM, HIGH)")
    status = serializers.CharField(help_text="Bankomat texnik holati")
    repair_cost = serializers.FloatField(help_text="Ta'mirlash xarajatlari (so'mda)")
    btech_fee = serializers.FloatField(help_text="BTech oylik to'lovi (so'mda)")
    glob_fee = serializers.FloatField(help_text="Glob oylik to'lovi (so'mda)")


class ATMInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="ATM ID")
    terminal_id = serializers.CharField(help_text="Terminal ID")
    name = serializers.CharField(help_text="Bankomat nomi")
    region = serializers.CharField(help_text="Viloyat")
    model = serializers.CharField(help_text="Model")
    address = serializers.CharField(help_text="Manzil")
    status = serializers.CharField(help_text="Texnik holati")
    serial_number = serializers.CharField(help_text="Seriya raqami")


class ATMAIAnalysisResponseSerializer(serializers.Serializer):
    analysis = serializers.CharField(help_text="Ollama AI o'zbek tilidagi batafsil tahlili")
    atm = ATMInfoSerializer(help_text="Bankomat pasport ma'lumotlari")
    metrics = ATMMetricsSerializer(help_text="Aniq hisoblangan moliyaviy va texnik raqamlar")
    line_chart = ATMLineChartSerializer(help_text="Line graph chizish uchun oxirgi 6 oylik aniq miqdorlar")
    monthly_records = serializers.ListField(
        child=ATMMonthlyRecordSerializer(),
        help_text="Oylar kesimidagi aniq jadval ko'rsatkichlari"
    )


@extend_schema(
    tags=["ATM AI"],
    summary="Bitta bankomat bo'yicha 6 oylik Ollama AI tahlili va Line Graph ko'rsatkichlari",
    description="Oxirgi 6 oylik aniq moliyaviy hisob-kitoblar (daromad, haqiqiy xarajatlar, naqd pul aylanmasi) va Ollama AI xulosasi.",
    request=None,
    responses={200: ATMAIAnalysisResponseSerializer},
)
class ATMAIAnalysisAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, pk):
        # 1. Bankomat ob'ektini olish
        atm = ATMDetailQuerySet.get(pk)

        # 2. Aynan OXIRGI 6 OYLIK statistikani olish (xronologik o'sish tartibida)
        recent_6_stats = list(
            atm.monthly_statistics.order_by("-year", "-month")[:6]
        )[::-1]

        # 3. Shartnoma va servis to'lovlarini tayyorlash (* 1000 so'm)
        contract = getattr(atm, "service_contract", None)
        btech_fee_monthly = round(float(contract.btech_monthly_fee or 0) * 1000, 2) if contract else 0
        glob_fee_monthly = round(float(contract.glob_monthly_fee or 0) * 1000, 2) if contract else 0
        payments = list(contract.payments.all()) if contract else []

        # 4. Texnik holat va ta'mirlash xarajatlari (maintenance bazada allaqachon aniq so'mda saqlangan)
        tech = getattr(atm, "technical", None)
        status_str = (tech.status if tech and tech.status else "SOZ")
        serial_str = (tech.serial_number if tech and tech.serial_number else "")
        m_items = list(tech.maintenance_items.all()) if tech else []

        chart_labels = []
        chart_income = []
        chart_expense = []
        chart_profit = []
        chart_withdrawn = []
        monthly_records = []

        # 5. Har bir oy bo'yicha haqiqiy ko'rsatkichlarni hisoblash
        for m in recent_6_stats:
            period_str = f"{m.year}-{int(m.month):02d}"

            # a) Yechilgan naqd pul aylanmasi (expense bazada 1000 ga bo'lingan, shuning uchun * 1000)
            cash_withdrawn = round(float(m.expense or 0) * 1000, 2)

            # b) Bankning yalpi komissiya daromadi (income bazada 1000 ga bo'lingan, shuning uchun * 1000)
            income = round(float(m.income or 0) * 1000, 2)

            # c) Haqiqiy operatsion xarajatlar:
            # 1. Servis xizmati
            service_cost = round(btech_fee_monthly + glob_fee_monthly, 2)

            # 2. Kommunal va ijara to'lovlari (svet, rent, incas)
            elec = sum(float(p.amount) * 1000 for p in payments if p.year == m.year and p.month == m.month and p.payment_type == "ELECTRICITY")
            rent = sum(float(p.amount) * 1000 for p in payments if p.year == m.year and p.month == m.month and p.payment_type == "RENT")
            incas = sum(float(p.amount) * 1000 for p in payments if p.year == m.year and p.month == m.month and p.payment_type == "INCASSATION")
            utility_cost = round(elec + rent + incas, 2)

            # 3. Ta'mirlash (maintenance) shu oyga to'g'ri kelsa
            repair_cost = 0.0
            for it in m_items:
                p_date = getattr(it, "protocol_date", None)
                if p_date and p_date.year == m.year and p_date.month == m.month:
                    repair_cost += float(it.total_with_vat or 0)
            repair_cost = round(repair_cost, 2)

            # Jami haqiqiy xarajat
            real_expense = round(service_cost + utility_cost + repair_cost, 2)

            # Sof foyda = Komissiya daromadi - Jami haqiqiy xarajatlar
            net_profit = round(income - real_expense, 2)

            chart_labels.append(period_str)
            chart_income.append(income)
            chart_expense.append(real_expense)
            chart_profit.append(net_profit)
            chart_withdrawn.append(cash_withdrawn)

            monthly_records.append({
                "period": period_str,
                "year": m.year,
                "month": m.month,
                "cash_withdrawn": cash_withdrawn,
                "income": income,
                "service_cost": service_cost,
                "utility_cost": utility_cost,
                "repair_cost": repair_cost,
                "total_expense": real_expense,
                "net_profit": net_profit,
            })

        # 6. 6 oylik umumiy va o'rtacha aniq sonlar
        total_inc = round(sum(chart_income), 2)
        total_withdrawn = round(sum(chart_withdrawn), 2)
        total_exp = round(sum(chart_expense), 2)
        total_prof = round(total_inc - total_exp, 2)
        total_service = round(sum(r["service_cost"] for r in monthly_records), 2)
        total_utility = round(sum(r["utility_cost"] for r in monthly_records), 2)
        total_repair = round(sum(r["repair_cost"] for r in monthly_records), 2)

        months_count = len(chart_income) if chart_income else 1
        avg_inc = round(total_inc / months_count, 2)
        avg_withdrawn = round(total_withdrawn / months_count, 2)
        avg_exp = round(total_exp / months_count, 2)
        profitability_pct = round((total_prof / total_inc) * 100, 2) if total_inc > 0 else 0

        atm_info_dict = {
            "id": atm.id,
            "terminal_id": atm.terminal_id,
            "name": atm.name,
            "region": atm.region or "",
            "model": atm.model or "",
            "address": getattr(atm, "address", "") or "",
            "status": status_str,
            "serial_number": serial_str,
        }

        metrics_dict = {
            "total_income": total_inc,
            "total_cash_withdrawn": total_withdrawn,
            "total_expense": total_exp,
            "net_profit": total_prof,
            "average_income": avg_inc,
            "average_cash_withdrawn": avg_withdrawn,
            "average_expense": avg_exp,
            "profitability_rate": profitability_pct,
            "total_service_fee": total_service,
            "total_utility_cost": total_utility,
            "total_repair_cost": total_repair,
            "health_score": 95 if status_str == "SOZ" and total_prof >= 0 else (75 if status_str == "SOZ" else 35),
            "risk_level": "LOW" if total_prof >= 0 else ("MEDIUM" if total_inc > 0 else "HIGH"),
            "status": status_str,
            "repair_cost": total_repair,
            "btech_fee": btech_fee_monthly,
            "glob_fee": glob_fee_monthly,
        }

        service_dict = {
            "btech_fee": btech_fee_monthly,
            "glob_fee": glob_fee_monthly,
            "total_service_fee": total_service,
            "total_utility_cost": total_utility,
            "total_repair_cost": total_repair,
        }

        # 7. Ollama AI uchun lo'nda, professional o'zbekcha hisobot tayyorlash
        prompt_data = {
            "atm": atm_info_dict,
            "metrics": metrics_dict,
            "service": service_dict,
            "monthly_records": monthly_records,
        }
        prompt = PromptBuilder.build(prompt_data)
        analysis_text = OllamaService.generate(prompt)

        # 8. Response qaytarish
        return Response({
            "analysis": analysis_text,
            "atm": atm_info_dict,
            "metrics": metrics_dict,
            "line_chart": {
                "labels": chart_labels,
                "income": chart_income,
                "expense": chart_expense,
                "profit": chart_profit,
                "cash_withdrawn": chart_withdrawn,
            },
            "monthly_records": monthly_records,
        })
