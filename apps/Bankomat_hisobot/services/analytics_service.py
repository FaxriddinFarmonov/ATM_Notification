from decimal import Decimal
from collections import defaultdict
from django.db.models import Sum, Count, Q
from django.utils import timezone

from apps.Bankomat_hisobot.models import (
    ATMTURON,
    ATMTechnical,
    ATMMonthlyStatistic,
    ATMYearStatistic,
    ATMServiceContract,
    ATMServicePayment,
)
from apps.maintenance.models import MaintenanceItem


class BaseAnalyticsHelper:
    MONEY_MULTIPLIER = 1000

    @classmethod
    def money(cls, value):
        if value is None:
            return 0.0
        return float(Decimal(str(value)) * cls.MONEY_MULTIPLIER)

    @classmethod
    def round_val(cls, value, digits=2):
        if value is None:
            return 0.0
        return round(float(value), digits)

    @classmethod
    def get_latest_period(cls):
        """
        Bazadagi eng oxirgi to'liq statistik oy va yilni qaytaradi.
        """
        latest = (
            ATMMonthlyStatistic.objects.order_by("-year", "-month")
            .values("year", "month")
            .first()
        )
        if latest:
            return latest["year"], latest["month"]
        return 2026, 6

    @classmethod
    def get_serial_to_atm_mapping(cls):
        """
        MaintenanceItem dagi texnikasi null bo'lgan yozuvlarni
        serial_number orqali ATM ga bog'lash lug'ati.
        """
        return {
            t["serial_number"]: t["atm_id"]
            for t in ATMTechnical.objects.filter(serial_number__gt="").values("serial_number", "atm_id")
            if t["atm_id"]
        }

    @classmethod
    def get_atm_filial_mapping(cls):
        """
        MaintenanceItem lardan filial nomlarini yig'ish.
        """
        filial_map = {}
        for row in MaintenanceItem.objects.filter(technical__atm_id__isnull=False).exclude(filial_name="").values("technical__atm_id", "filial_name"):
            filial_map[row["technical__atm_id"]] = row["filial_name"]
        return filial_map

    @classmethod
    def collect_atm_expenses(cls, year=None, month=None, region=None):
        """
        Har bir bankomat uchun haqiqiy xarajatlarni to'plash:
        1. MaintenanceItem (Zapchast va ta'mirlash, to'liq so'mda)
        2. ATMServicePayment (RENT, ELECTRICITY, INCASSATION - ming so'mda, *1000 qilinadi)
        3. ATMServiceContract (BTech va Glob oylik shartnoma to'lovlari)
        """
        serial_to_atm = cls.get_serial_to_atm_mapping()
        filial_map = cls.get_atm_filial_mapping()

        # Natijaviy lug'at: atm_id -> xarajatlar
        expense_map = defaultdict(lambda: {
            "maintenance_cost": 0.0,
            "repairs_count": 0,
            "rent_cost": 0.0,
            "electricity_cost": 0.0,
            "incassation_cost": 0.0,
            "service_fee": 0.0,
            "total_real_expense": 0.0,
            "filial_name": "",
        })

        # 1. MaintenanceItem xarajatlari
        m_qs = MaintenanceItem.objects.all()
        if year:
            m_qs = m_qs.filter(protocol_date__year=year)
        if month:
            m_qs = m_qs.filter(protocol_date__month=month)

        for m in m_qs.select_related("technical"):
            aid = m.technical.atm_id if (m.technical and m.technical.atm_id) else serial_to_atm.get(m.serial_number)
            if aid:
                cost = float(m.total_with_vat or 0)
                expense_map[aid]["maintenance_cost"] += cost
                expense_map[aid]["repairs_count"] += 1
                if m.filial_name and not expense_map[aid]["filial_name"]:
                    expense_map[aid]["filial_name"] = m.filial_name

        # 2. ATMServicePayment (Ijara, Tok, Inkassatsiya)
        p_qs = ATMServicePayment.objects.select_related("contract")
        if year:
            p_qs = p_qs.filter(year=year)
        if month:
            p_qs = p_qs.filter(month=month)

        for p in p_qs:
            aid = p.contract.atm_id if p.contract else None
            if aid:
                amt = cls.money(p.amount)
                pt = p.payment_type
                if pt == "RENT":
                    expense_map[aid]["rent_cost"] += amt
                elif pt == "ELECTRICITY":
                    expense_map[aid]["electricity_cost"] += amt
                elif pt == "INCASSATION":
                    expense_map[aid]["incassation_cost"] += amt

        # 3. ATMServiceContract (BTech va Glob oylik qat'iy to'lovlari)
        if month:
            months_multiplier = 1
        elif year == 2026:
            months_multiplier = 6
        elif year == 2025:
            months_multiplier = 12
        elif year:
            months_multiplier = ATMMonthlyStatistic.objects.filter(year=year).values("month").distinct().count() or 1
        else:
            months_multiplier = ATMMonthlyStatistic.objects.values("year", "month").distinct().count() or 18

        for c in ATMServiceContract.objects.all():
            aid = c.atm_id
            fee = cls.money(c.btech_monthly_fee + c.glob_monthly_fee) * months_multiplier
            expense_map[aid]["service_fee"] += fee

        # Jami haqiqiy xarajatlarni yakunlash
        for aid, exp in expense_map.items():
            exp["total_real_expense"] = (
                exp["maintenance_cost"]
                + exp["rent_cost"]
                + exp["electricity_cost"]
                + exp["incassation_cost"]
                + exp["service_fee"]
            )
            if not exp["filial_name"] and aid in filial_map:
                exp["filial_name"] = filial_map[aid]

        return expense_map


class TopIncomeATMsService(BaseAnalyticsHelper):
    """
    1. Eng ko'p daromad keltirgan bankomatlar (Top Revenue ATMs).
    - Daromad tayyor (ATMMonthlyStatistic.income * 1000).
    - ATMMonthlyStatistic.expense esa bankomatdan yechilgan naqd pul aylanmasi (cash_withdrawal).
    - Haqiqiy xarajatlar esa MaintenanceItem va Service to'lovlaridan yig'iladi.
    - Sof foyda: income - total_real_expense.
    """

    @classmethod
    def get(cls, period="all", year=None, month=None, region=None, card_type=None, limit=10):
        # Default davr: agar yil/oy berilmasa, eng oxirgi to'liq oy
        if not year and not month and period == "all":
            pass  # barcha davr uchun jamlanadi
        elif not year and not month and period == "monthly":
            year, month = cls.get_latest_period()

        # 1. Daromad va aylanma statistikasi
        stats_qs = ATMMonthlyStatistic.objects.select_related("atm", "atm__technical")
        if region:
            stats_qs = stats_qs.filter(atm__region__iexact=region)
        if card_type:
            stats_qs = stats_qs.filter(atm__card_type__iexact=card_type)
        if year:
            stats_qs = stats_qs.filter(year=year)
        if month:
            stats_qs = stats_qs.filter(month=month)

        grouped = (
            stats_qs.values(
                "atm_id",
                "atm__terminal_id",
                "atm__name",
                "atm__region",
                "atm__address",
                "atm__model",
                "atm__card_type",
                "atm__is_active",
                "atm__technical__status",
                "atm__technical__serial_number",
            )
            .annotate(
                sum_income=Sum("income"),
                sum_cash_withdrawal=Sum("expense"),  # YECHILGAN PUL!
            )
            .order_by("-sum_income")
        )

        # 2. Xarajatlarni to'plash
        expenses = cls.collect_atm_expenses(year=year, month=month, region=region)

        results = []
        for idx, row in enumerate(grouped[:limit], start=1):
            aid = row["atm_id"]
            income = cls.money(row["sum_income"])
            cash_withdrawn = cls.money(row["sum_cash_withdrawal"])
            exp = expenses.get(aid, {})

            maint_cost = exp.get("maintenance_cost", 0.0)
            service_cost = (
                exp.get("rent_cost", 0.0)
                + exp.get("electricity_cost", 0.0)
                + exp.get("incassation_cost", 0.0)
                + exp.get("service_fee", 0.0)
            )
            total_real_exp = maint_cost + service_cost
            net_profit = income - total_real_exp
            margin = cls.round_val((net_profit / income * 100) if income > 0 else 0.0)

            results.append({
                "rank": idx,
                "atm_id": aid,
                "terminal_id": row["atm__terminal_id"] or "",
                "serial_number": row["atm__technical__serial_number"] or "",
                "name": row["atm__name"] or "",
                "filial_name": exp.get("filial_name") or row["atm__name"] or "",
                "region": row["atm__region"] or "",
                "address": row["atm__address"] or "",
                "model": row["atm__model"] or "",
                "card_type": row["atm__card_type"] or "",
                "status": row["atm__technical__status"] or "SOZ",
                "is_active": row["atm__is_active"],
                "income": income,
                "cash_withdrawal": cash_withdrawn,
                "maintenance_cost": maint_cost,
                "service_cost": service_cost,
                "total_real_expense": total_real_exp,
                "net_profit": net_profit,
                "profit_margin": margin,
            })

        return results


class TopExpenseATMsService(BaseAnalyticsHelper):
    """
    2. Eng ko'p haqiqiy rasxod qilgan bankomatlar reytingi.
    - Xarajatlar taqsimoti: zapchast/ta'mirlash, ijara, tok, inkassatsiya, servis.
    - Bankomat keltirgan daromad va aylanma bilan qiyoslash.
    - Qaysi region va qaysi BXM/BXO da joylashganligi.
    """

    @classmethod
    def get(cls, expense_type="all", year=None, month=None, region=None, limit=10):
        # 1. Barcha xarajatlarni to'plash
        expenses = cls.collect_atm_expenses(year=year, month=month, region=region)

        # 2. Bankomatlar ma'lumotlari va daromadlari
        stats_qs = ATMMonthlyStatistic.objects.select_related("atm", "atm__technical")
        if region:
            stats_qs = stats_qs.filter(atm__region__iexact=region)
        if year:
            stats_qs = stats_qs.filter(year=year)
        if month:
            stats_qs = stats_qs.filter(month=month)

        atm_fin = (
            stats_qs.values(
                "atm_id",
                "atm__terminal_id",
                "atm__name",
                "atm__region",
                "atm__address",
                "atm__model",
                "atm__card_type",
                "atm__technical__status",
                "atm__technical__serial_number",
            )
            .annotate(
                sum_income=Sum("income"),
                sum_cash_withdrawal=Sum("expense"),
            )
        )
        fin_map = {row["atm_id"]: row for row in atm_fin}

        # Barcha bankomatlar bazasini qamrab olish
        all_atm_ids = set(fin_map.keys()) | set(expenses.keys())
        if region:
            region_atm_ids = set(ATMTURON.objects.filter(region__iexact=region).values_list("id", flat=True))
            all_atm_ids = all_atm_ids & region_atm_ids

        missing_meta = ATMTURON.objects.filter(id__in=all_atm_ids - set(fin_map.keys())).values(
            "id", "terminal_id", "name", "region", "address", "model", "card_type", "technical__status", "technical__serial_number"
        )
        for m in missing_meta:
            fin_map[m["id"]] = {
                "atm_id": m["id"],
                "atm__terminal_id": m["terminal_id"],
                "atm__name": m["name"],
                "atm__region": m["region"],
                "atm__address": m["address"],
                "atm__model": m["model"],
                "atm__card_type": m["card_type"],
                "atm__technical__status": m.get("technical__status") or "SOZ",
                "atm__technical__serial_number": m.get("technical__serial_number") or "",
                "sum_income": 0,
                "sum_cash_withdrawal": 0,
            }

        items = []
        for aid in all_atm_ids:
            meta = fin_map.get(aid, {})
            exp = expenses.get(aid, {})

            income = cls.money(meta.get("sum_income", 0))
            cash_withdrawn = cls.money(meta.get("sum_cash_withdrawal", 0))
            maint = exp.get("maintenance_cost", 0.0)
            rent = exp.get("rent_cost", 0.0)
            elec = exp.get("electricity_cost", 0.0)
            incass = exp.get("incassation_cost", 0.0)
            srv = exp.get("service_fee", 0.0)
            tot_exp = maint + rent + elec + incass + srv
            net_profit = income - tot_exp
            ratio = cls.round_val((tot_exp / income * 100) if income > 0 else 999.9)

            items.append({
                "atm_id": aid,
                "terminal_id": meta.get("atm__terminal_id") or "",
                "serial_number": meta.get("atm__technical__serial_number") or "",
                "name": meta.get("atm__name") or "",
                "filial_name": exp.get("filial_name") or meta.get("atm__name") or "",
                "region": meta.get("atm__region") or "",
                "address": meta.get("atm__address") or "",
                "model": meta.get("atm__model") or "",
                "card_type": meta.get("atm__card_type") or "",
                "status": meta.get("atm__technical__status") or "SOZ",
                "income": income,
                "cash_withdrawal": cash_withdrawn,
                "maintenance_cost": maint,
                "rent_cost": rent,
                "electricity_cost": elec,
                "incassation_cost": incass,
                "service_fees": srv,
                "total_real_expense": tot_exp,
                "net_profit": net_profit,
                "expense_to_income_ratio": ratio,
                "repairs_count": exp.get("repairs_count", 0),
            })

        # Filtr bo'yicha saralash
        if expense_type == "maintenance":
            items.sort(key=lambda x: x["maintenance_cost"], reverse=True)
        elif expense_type == "rent":
            items.sort(key=lambda x: x["rent_cost"], reverse=True)
        elif expense_type == "electricity":
            items.sort(key=lambda x: x["electricity_cost"], reverse=True)
        elif expense_type == "incassation":
            items.sort(key=lambda x: x["incassation_cost"], reverse=True)
        else:
            items.sort(key=lambda x: x["total_real_expense"], reverse=True)

        ranked = []
        for idx, it in enumerate(items[:limit], start=1):
            it["rank"] = idx
            ranked.append(it)

        return ranked


class TopRegionsAnalyticsService(BaseAnalyticsHelper):
    """
    3. Viloyatlar kesimida to'liq moliyaviy tahlil va reyting:
    - Jami daromad, yechilgan naqd pul aylanmasi
    - Jami haqiqiy xarajatlar (zapchastlar + tok + ijara + inkassatsiya + servis)
    - Sof foyda va rentabellik marjasi
    - O'rtacha bitta bankomat hissasiga to'g'ri keluvchi daromad va rasxod
    - Viloyatning yetakchi (top) bankomati
    """

    @classmethod
    def get(cls, year=None, month=None, sort_by="income", limit=20):
        # 1. Viloyatlar bo'yicha bankomatlar taqsimoti
        atms_qs = ATMTURON.objects.exclude(region="").values("region").annotate(
            total_atms=Count("id", distinct=True),
            active_atms=Count("id", filter=Q(is_active=True), distinct=True),
            soz_atms=Count("id", filter=Q(technical__status="SOZ"), distinct=True),
            nosoz_atms=Count("id", filter=Q(technical__status="NOSOZ"), distinct=True),
            uzcard_atms=Count("id", filter=Q(card_type="UZCARD"), distinct=True),
            humo_atms=Count("id", filter=Q(card_type="HUMO"), distinct=True),
        )
        region_meta = {row["region"]: row for row in atms_qs}

        # 2. Daromad va yechilgan pul agregatsiyasi
        stats_qs = ATMMonthlyStatistic.objects.exclude(atm__region="")
        if year:
            stats_qs = stats_qs.filter(year=year)
        if month:
            stats_qs = stats_qs.filter(month=month)

        fin_data = stats_qs.values("atm__region").annotate(
            sum_income=Sum("income"),
            sum_cash_withdrawal=Sum("expense"),
        )
        fin_map = {row["atm__region"]: row for row in fin_data}

        # 3. Viloyatdagi eng yaxshi bankomatlar
        top_atms_per_region = {}
        top_atm_rows = (
            stats_qs.values("atm__region", "atm__terminal_id", "atm__name")
            .annotate(tot_inc=Sum("income"))
            .order_by("atm__region", "-tot_inc")
        )
        for r in top_atm_rows:
            reg = r["atm__region"]
            if reg not in top_atms_per_region:
                top_atms_per_region[reg] = {
                    "terminal_id": r["atm__terminal_id"],
                    "name": r["atm__name"],
                    "income": cls.money(r["tot_inc"]),
                }

        # 4. Haqiqiy xarajatlarni to'plash
        expenses = cls.collect_atm_expenses(year=year, month=month)

        # Xarajatlarni viloyatlar bo'yicha jamlash
        region_expenses = defaultdict(lambda: {
            "maintenance_cost": 0.0,
            "operational_cost": 0.0,
            "total_real_expense": 0.0,
        })
        atm_region_lookup = dict(ATMTURON.objects.values_list("id", "region"))
        for aid, exp in expenses.items():
            reg = atm_region_lookup.get(aid)
            if reg:
                maint = exp["maintenance_cost"]
                oper = exp["rent_cost"] + exp["electricity_cost"] + exp["incassation_cost"] + exp["service_fee"]
                region_expenses[reg]["maintenance_cost"] += maint
                region_expenses[reg]["operational_cost"] += oper
                region_expenses[reg]["total_real_expense"] += (maint + oper)

        results = []
        for region_name, meta in region_meta.items():
            fin = fin_map.get(region_name, {})
            exp = region_expenses.get(region_name, {})

            income = cls.money(fin.get("sum_income", 0))
            cash_withdrawn = cls.money(fin.get("sum_cash_withdrawal", 0))
            maint_cost = exp.get("maintenance_cost", 0.0)
            oper_cost = exp.get("operational_cost", 0.0)
            total_real_exp = maint_cost + oper_cost

            net_profit = income - total_real_exp
            profit_margin = cls.round_val((net_profit / income * 100) if income > 0 else 0.0)

            tot_atms = meta["total_atms"]
            avg_income = cls.round_val(income / tot_atms) if tot_atms > 0 else 0.0
            avg_expense = cls.round_val(total_real_exp / tot_atms) if tot_atms > 0 else 0.0

            results.append({
                "region": region_name,
                "total_atms": tot_atms,
                "active_atms": meta["active_atms"],
                "inactive_atms": tot_atms - meta["active_atms"],
                "soz_atms": meta["soz_atms"],
                "nosoz_atms": meta["nosoz_atms"],
                "uzcard_atms": meta["uzcard_atms"],
                "humo_atms": meta["humo_atms"],
                "total_income": income,
                "total_cash_withdrawal": cash_withdrawn,
                "total_real_expense": total_real_exp,
                "maintenance_cost": maint_cost,
                "operational_cost": oper_cost,
                "net_profit": net_profit,
                "profit_margin": profit_margin,
                "avg_income_per_atm": avg_income,
                "avg_expense_per_atm": avg_expense,
                "top_atm": top_atms_per_region.get(region_name, {
                    "terminal_id": "",
                    "name": "",
                    "income": 0.0,
                }),
            })

        # Saralash
        sort_keys = {
            "income": lambda x: x["total_income"],
            "expense": lambda x: x["total_real_expense"],
            "profit": lambda x: x["net_profit"],
            "profit_margin": lambda x: x["profit_margin"],
            "atms_count": lambda x: x["total_atms"],
            "cash_withdrawal": lambda x: x["total_cash_withdrawal"],
        }
        key_func = sort_keys.get(sort_by, sort_keys["income"])
        results.sort(key=key_func, reverse=True)

        ranked = []
        for idx, it in enumerate(results[:limit], start=1):
            it["rank"] = idx
            ranked.append(it)

        return ranked


class LossMakingRelocationService(BaseAnalyticsHelper):
    """
    4. Rasxodi daromadidan oshib ketgan muammoli bankomatlar
       va Joyini almashtirish (Relokatsiya) bo'yicha qat'iy tavsiyalar.
    - 100% real bazadagi raqamlar asosida.
    - OLLAMA ISHLATILMAYDI.
    - Aniq qoidali biznes algoritmi: past aylanmali nuqtalarni ko'chirish,
      yuqori ta'mirlashli nuqtalarni audit qilish, ijara stavkalarini qayta ko'rib chiqish.
    """

    @classmethod
    def get(cls, year=None, month=None, region=None, min_loss=0, limit=20):
        # Barcha bankomatlar xarajatlari va daromadlarini olish
        all_atms = TopExpenseATMsService.get(
            expense_type="all",
            year=year,
            month=month,
            region=region,
            limit=500,
        )

        loss_making_list = []
        for atm in all_atms:
            income = atm["income"]
            total_exp = atm["total_real_expense"]
            net_profit = atm["net_profit"]
            cash_withdrawn = atm["cash_withdrawal"]
            maint_cost = atm["maintenance_cost"]
            rent_cost = atm["rent_cost"]
            oper_cost = atm["electricity_cost"] + atm["incassation_cost"] + atm["service_fees"]

            # Zarar sharti: xarajat daromaddan ko'p bo'lsa yoki daromad 0 bo'lib xarajat mavjud bo'lsa
            if total_exp > income or (income == 0 and total_exp > 0):
                loss_amount = total_exp - income
                if loss_amount < min_loss:
                    continue

                # ==============================================================
                # ALGORITMIK TAVSIYALAR DVIJOKI (NO OLLAMA, 100% PURE LOGIC)
                # ==============================================================
                if cash_withdrawn < 100_000_000 and income < 1_000_000:
                    primary_cause = "PAST_AYLANMA_VA_KAM_DAROMAD"
                    action_required = "JOYINI_ALMASHTIRISH"
                    urgency_level = "YUQORI"
                    recommendation = (
                        f"Bankomatda oylik naqd pul aylanmasi juda past ({cash_withdrawn:,.0f} so'm) va "
                        f"daromad ({income:,.0f} so'm) xarajatlarni ({total_exp:,.0f} so'm) mutlaqo qoplamayapti. "
                        f"Ushbu {atm['name']} bankomatini aholi oqimi yuqori bo'lgan savdo markazi, bozor yoki "
                        f"vokzal hududiga JOYINI ALMASHTIRISH (RELOKATSIYA) tavsiya etiladi."
                    )
                elif rent_cost > income and rent_cost > 0:
                    primary_cause = "IJARA_XARAJATI_DAROMADDAN_YUQORI"
                    action_required = "IJARA_MUZOKARASI_YOKI_KOCHIRISH"
                    urgency_level = "YUQORI"
                    recommendation = (
                        f"Bankomatning ijara to'lovi ({rent_cost:,.0f} so'm) keltirayotgan daromadidan ({income:,.0f} so'm) "
                        f"yuqori. Ijara to'lovini pasaytirish bo'yicha muzokara o'tkazish yoki bankning o'z binosiga "
                        f"ko'chirish tavsiya etiladi."
                    )
                elif maint_cost > income or maint_cost > 2_000_000:
                    primary_cause = "ORTIQCHA_TAMIRLASH_VA_ZAPCHAST_XARAJATI"
                    action_required = "TEXNIK_AUDIT_YOKI_YANGILASH"
                    urgency_level = "YUQORI" if maint_cost > 5_000_000 else "O'RTA"
                    recommendation = (
                        f"Ehtiyot qismlar va ta'mirlash xarajatlari ({maint_cost:,.0f} so'm, {atm['repairs_count']} ta ta'mirlash) "
                        f"daromadga nisbatan o'ta yuqori. Bankomat modeli ({atm['model']}) eskirgan yoki surunkali nosozliklar mavjud. "
                        f"Bankomatni to'liq texnik auditdan o'tkazish yoki yangi zamonaviy modelga almashtirish lozim."
                    )
                elif oper_cost > income:
                    primary_cause = "LOGISTIKA_VA_OPERATSION_XARAJATLAR_YUQORI"
                    action_required = "INKASSATSIYA_GRAFIGINI_OPTIMALLASHTIRISH"
                    urgency_level = "O'RTA"
                    recommendation = (
                        f"Inkassatsiya va elektr operatsion xarajatlari ({oper_cost:,.0f} so'm) daromaddan oshmoqda. "
                        f"Inkassatsiya rejasini qayta ko'rib chiqish va xizmat shartnomalarini optimallashtirish tavsiya etiladi."
                    )
                else:
                    primary_cause = "RENTABELLIK_MANFIY"
                    action_required = "KOMPLEKS_MONITORING"
                    urgency_level = "O'RTA"
                    recommendation = (
                        f"Bankomat oylik {loss_amount:,.0f} so'm zarar bilan ishlamoqda. "
                        f"Filial mutaxassislari ishtirokida joylashuv samaradorligini qayta baholash zarur."
                    )

                loss_making_list.append({
                    "atm_id": atm["atm_id"],
                    "terminal_id": atm["terminal_id"],
                    "serial_number": atm["serial_number"],
                    "name": atm["name"],
                    "filial_name": atm["filial_name"],
                    "region": atm["region"],
                    "address": atm["address"],
                    "model": atm["model"],
                    "card_type": atm["card_type"],
                    "status": atm["status"],
                    "income": income,
                    "cash_withdrawal": cash_withdrawn,
                    "total_real_expense": total_exp,
                    "loss_amount": loss_amount,
                    "maintenance_cost": maint_cost,
                    "rent_cost": rent_cost,
                    "operational_cost": oper_cost,
                    "primary_cause": primary_cause,
                    "action_required": action_required,
                    "urgency_level": urgency_level,
                    "recommendation": recommendation,
                })

        loss_making_list.sort(key=lambda x: x["loss_amount"], reverse=True)

        ranked = []
        for idx, item in enumerate(loss_making_list[:limit], start=1):
            item["rank"] = idx
            ranked.append(item)

        return ranked


class ManagementOverviewService(BaseAnalyticsHelper):
    """
    5. Boshqaruv uchun o'tgan oy (va davriy) tezkor KPI xulosasi.
    Dashboard kartalari va monitoring uchun yagona to'liq ko'rsatkichlar to'plami.
    """

    @classmethod
    def get(cls, year=None, month=None):
        # Default: agar yil va oy berilmasa, eng oxirgi to'liq ma'lumot mavjud oy
        is_default_last_month = False
        if not year and not month:
            year, month = cls.get_latest_period()
            is_default_last_month = True

        month_names = {
            1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel", 5: "May", 6: "Iyun",
            7: "Iyul", 8: "Avgust", 9: "Sentabr", 10: "Oktabr", 11: "Noyabr", 12: "Dekabr"
        }
        period_str = f"{year}-yil {month_names.get(month, month)} (O'tgan oy)" if is_default_last_month else (
            f"{year}-yil {month_names.get(month, '')}" if month else f"{year}-yil"
        )

        # 1. Daromad va aylanma
        stats_qs = ATMMonthlyStatistic.objects.filter(year=year)
        if month:
            stats_qs = stats_qs.filter(month=month)

        totals = stats_qs.aggregate(
            inc=Sum("income"),
            cw=Sum("expense"),
        )
        total_income = cls.money(totals["inc"])
        total_cash_withdrawal = cls.money(totals["cw"])

        # 2. Haqiqiy xarajatlarni hisoblash
        expenses = cls.collect_atm_expenses(year=year, month=month)
        total_maint = sum(e["maintenance_cost"] for e in expenses.values())
        total_rent = sum(e["rent_cost"] for e in expenses.values())
        total_elec = sum(e["electricity_cost"] for e in expenses.values())
        total_incass = sum(e["incassation_cost"] for e in expenses.values())
        total_srv = sum(e["service_fee"] for e in expenses.values())
        total_real_expense = total_maint + total_rent + total_elec + total_incass + total_srv

        total_net_profit = total_income - total_real_expense
        overall_margin = cls.round_val((total_net_profit / total_income * 100) if total_income > 0 else 0.0)

        # 3. Bankomatlar soni
        total_atms = ATMTURON.objects.count()
        active_atms = ATMTURON.objects.filter(is_active=True).count()

        # 4. Top daromadli va top xarajatli bankomat
        top_income_list = TopIncomeATMsService.get(year=year, month=month, limit=1)
        top_revenue_atm = top_income_list[0] if top_income_list else None

        top_expense_list = TopExpenseATMsService.get(year=year, month=month, limit=1)
        top_expense_atm = top_expense_list[0] if top_expense_list else None

        # 5. Viloyatlar reytingi
        regions = TopRegionsAnalyticsService.get(year=year, month=month, sort_by="profit", limit=20)
        top_profit_region = regions[0] if regions else None
        most_problematic_region = regions[-1] if regions else None

        # 6. Zarardagi bankomatlar statistikasi
        loss_atms = LossMakingRelocationService.get(year=year, month=month, limit=500)
        relocation_count = sum(1 for a in loss_atms if a.get("action_required") == "JOYINI_ALMASHTIRISH")

        return {
            "period_label": period_str,
            "year": year,
            "month": month,
            "kpi_overview": {
                "total_income": total_income,
                "total_cash_withdrawal": total_cash_withdrawal,
                "total_real_expense": total_real_expense,
                "total_maintenance_cost": total_maint,
                "total_rent_cost": total_rent,
                "total_operational_cost": total_elec + total_incass + total_srv,
                "total_net_profit": total_net_profit,
                "overall_profit_margin": overall_margin,
                "total_atms": total_atms,
                "active_atms": active_atms,
                "loss_making_atms_count": len(loss_atms),
                "relocation_recommended_count": relocation_count,
            },
            "top_revenue_atm": {
                "terminal_id": top_revenue_atm["terminal_id"] if top_revenue_atm else "",
                "name": top_revenue_atm["name"] if top_revenue_atm else "",
                "region": top_revenue_atm["region"] if top_revenue_atm else "",
                "income": top_revenue_atm["income"] if top_revenue_atm else 0.0,
                "cash_withdrawal": top_revenue_atm["cash_withdrawal"] if top_revenue_atm else 0.0,
                "net_profit": top_revenue_atm["net_profit"] if top_revenue_atm else 0.0,
            } if top_revenue_atm else None,
            "top_expense_atm": {
                "terminal_id": top_expense_atm["terminal_id"] if top_expense_atm else "",
                "name": top_expense_atm["name"] if top_expense_atm else "",
                "region": top_expense_atm["region"] if top_expense_atm else "",
                "total_real_expense": top_expense_atm["total_real_expense"] if top_expense_atm else 0.0,
                "maintenance_cost": top_expense_atm["maintenance_cost"] if top_expense_atm else 0.0,
                "income": top_expense_atm["income"] if top_expense_atm else 0.0,
            } if top_expense_atm else None,
            "top_profit_region": {
                "region": top_profit_region["region"] if top_profit_region else "",
                "total_income": top_profit_region["total_income"] if top_profit_region else 0.0,
                "net_profit": top_profit_region["net_profit"] if top_profit_region else 0.0,
                "total_atms": top_profit_region["total_atms"] if top_profit_region else 0,
            } if top_profit_region else None,
            "most_problematic_region": {
                "region": most_problematic_region["region"] if most_problematic_region else "",
                "total_real_expense": most_problematic_region["total_real_expense"] if most_problematic_region else 0.0,
                "net_profit": most_problematic_region["net_profit"] if most_problematic_region else 0.0,
                "total_atms": most_problematic_region["total_atms"] if most_problematic_region else 0,
            } if most_problematic_region else None,
        }


class ModelAnalyticsService(BaseAnalyticsHelper):
    """
    6. Bankomat va terminal modellari bo'yicha real tahlil va reyting.
    - 100% real bazadagi BTechATMSnapshot hamda ATMTechnical ma'lumotlaridan olinadi.
    """

    @classmethod
    def get(cls):
        from apps.atms.models import BTechATMSnapshot
        snapshots = BTechATMSnapshot.objects.all()

        model_map = defaultdict(lambda: {
            "model": "",
            "vendor": "",
            "total": 0,
            "online": 0,
            "offline": 0,
            "total_cash": 0,
        })

        if snapshots.exists():
            for s in snapshots:
                model_name = s.model_name or "Noma'lum"
                vendor_name = s.vendor_name or ""

                entry = model_map[model_name]
                entry["model"] = model_name
                if vendor_name and not entry["vendor"]:
                    entry["vendor"] = vendor_name
                entry["total"] += 1
                if s.service_status.lower() in ["inservice", "soz"] and s.agent_status.lower() in ["online", "soz"]:
                    entry["online"] += 1
                else:
                    entry["offline"] += 1
                entry["total_cash"] += s.total_cash_uzs
        else:
            techs = ATMTechnical.objects.select_related("atm").all()
            for t in techs:
                model_name = t.model_name or "Noma'lum"
                entry = model_map[model_name]
                entry["model"] = model_name
                entry["total"] += 1
                if t.status == "SOZ":
                    entry["online"] += 1
                else:
                    entry["offline"] += 1

        models_list = []
        for model_name, stats in model_map.items():
            tot = stats["total"]
            online = stats["online"]
            offline = stats["offline"]
            uptime = cls.round_val((online / tot * 100) if tot > 0 else 0.0)
            avg_cash = int(stats["total_cash"] / tot) if tot > 0 else 0

            status_label = "Yaxshi" if uptime >= 80 else ("O'rtacha" if uptime >= 50 else "Nosoz")

            models_list.append({
                "model": model_name,
                "vendor": stats["vendor"] or "Generik",
                "total": tot,
                "online": online,
                "offline": offline,
                "uptime": uptime,
                "total_cash": stats["total_cash"],
                "avg_cash": avg_cash,
                "status_label": status_label,
            })

        models_list.sort(key=lambda x: x["total"], reverse=True)

        total_models_count = len(models_list)
        total_atms_count = sum(m["total"] for m in models_list)
        overall_online = sum(m["online"] for m in models_list)
        overall_uptime = cls.round_val((overall_online / total_atms_count * 100) if total_atms_count > 0 else 0.0)

        top_popular = models_list[0] if models_list else None
        top_cash = max(models_list, key=lambda x: x["total_cash"]) if models_list else None

        return {
            "total_models_count": total_models_count,
            "total_atms_count": total_atms_count,
            "overall_uptime": overall_uptime,
            "top_popular_model": {
                "model": top_popular["model"] if top_popular else "",
                "vendor": top_popular["vendor"] if top_popular else "",
                "total": top_popular["total"] if top_popular else 0,
            } if top_popular else None,
            "top_cash_model": {
                "model": top_cash["model"] if top_cash else "",
                "total_cash": top_cash["total_cash"] if top_cash else 0,
            } if top_cash else None,
            "models": models_list,
        }


class AnnualFinancialsService(BaseAnalyticsHelper):
    """
    7. Bankning yillik (2024, 2025, 2026) moliyaviy daromad va haqiqiy rasxodlar tahlili.
    - 100% aniq real bazadagi raqamlar asosida.
    - Xarajatlar taqsimoti: Maintenance (Zapchast va ta'mirlash - to'liq so'mda),
      Rent (Ijara - *1000), Electricity (Tok - *1000), Incassation (Inkassatsiya - *1000),
      BTech & Glob (Shartnoma to'lovlari - *1000).
    """

    @classmethod
    def get(cls):
        years_data = []

        for yr in [2026, 2025, 2024]:
            # 1. Income from ATMMonthlyStatistic (*1000)
            inc_row = ATMMonthlyStatistic.objects.filter(year=yr).aggregate(tot=Sum('income'))
            income = cls.money(inc_row['tot'])

            # 2. Cash withdrawal (expense column in ATMMonthlyStatistic)
            cw_row = ATMMonthlyStatistic.objects.filter(year=yr).aggregate(tot=Sum('expense'))
            cash_withdrawal = cls.money(cw_row['tot'])

            # 3. MaintenanceItem (in full UZS sums!)
            m_row = MaintenanceItem.objects.filter(protocol_date__year=yr).aggregate(tot=Sum('total_with_vat'))
            maint_cost = float(m_row['tot'] or 0)

            # 4. ATMServicePayment (RENT, ELECTRICITY, INCASSATION - in thousands of UZS, * 1000)
            rent_row = ATMServicePayment.objects.filter(year=yr, payment_type='RENT').aggregate(tot=Sum('amount'))
            rent_cost = cls.money(rent_row['tot'])

            elec_row = ATMServicePayment.objects.filter(year=yr, payment_type='ELECTRICITY').aggregate(tot=Sum('amount'))
            elec_cost = cls.money(elec_row['tot'])

            incass_row = ATMServicePayment.objects.filter(year=yr, payment_type='INCASSATION').aggregate(tot=Sum('amount'))
            incass_cost = cls.money(incass_row['tot'])

            # 5. Contracts (BTech + Glob)
            months_count = 12 if yr in [2024, 2025] else 6
            contract_row = ATMServiceContract.objects.aggregate(
                btech=Sum('btech_monthly_fee'),
                glob=Sum('glob_monthly_fee')
            )
            btech_cost = cls.money(contract_row['btech']) * months_count
            glob_cost = cls.money(contract_row['glob']) * months_count
            btech_glob_total = btech_cost + glob_cost

            total_expense = maint_cost + rent_cost + elec_cost + incass_cost + btech_glob_total
            net_profit = income - total_expense
            margin = cls.round_val((net_profit / income * 100) if income > 0 else 0.0)

            label = f"{yr}-yil (6 oy)" if yr == 2026 else (f"{yr}-yil (To'liq)" if yr == 2025 else f"{yr}-yil")

            years_data.append({
                "year": yr,
                "label": label,
                "income": income,
                "cash_withdrawal": cash_withdrawal,
                "total_expense": total_expense,
                "net_profit": net_profit,
                "profit_margin": margin,
                "expenses_breakdown": {
                    "maintenance": maint_cost,
                    "rent": rent_cost,
                    "electricity": elec_cost,
                    "incassation": incass_cost,
                    "btech_glob": btech_glob_total,
                    "btech_fee": btech_cost,
                    "glob_fee": glob_cost,
                }
            })

        return {"years": years_data}




class YearlyComparisonService(BaseAnalyticsHelper):
    """
    4. Yillar bo'yicha moliyaviy ko'rsatkichlarni oylar kesimida taqqoslash (Comparison Service).
    """

    MONTH_NAMES = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]

    @classmethod
    def get(cls, year_a=2025, year_b=2026):
        try:
            year_a = int(year_a)
            year_b = int(year_b)
        except (ValueError, TypeError):
            year_a, year_b = 2025, 2026

        # 1. Daromad va naqd pul yechish aylanmasi
        stats_a = ATMMonthlyStatistic.objects.filter(year=year_a).values("month").annotate(inc=Sum("income"), cw=Sum("expense"))
        stats_b = ATMMonthlyStatistic.objects.filter(year=year_b).values("month").annotate(inc=Sum("income"), cw=Sum("expense"))

        map_a = {r["month"]: (cls.money(r["inc"]), cls.money(r["cw"])) for r in stats_a}
        map_b = {r["month"]: (cls.money(r["inc"]), cls.money(r["cw"])) for r in stats_b}

        # 2. Xarajatlar
        maint_a = MaintenanceItem.objects.filter(protocol_date__year=year_a).values("protocol_date__month").annotate(tot=Sum("total_with_vat"))
        maint_b = MaintenanceItem.objects.filter(protocol_date__year=year_b).values("protocol_date__month").annotate(tot=Sum("total_with_vat"))
        maint_map_a = {r["protocol_date__month"]: float(r["tot"] or 0) for r in maint_a}
        maint_map_b = {r["protocol_date__month"]: float(r["tot"] or 0) for r in maint_b}

        serv_a = ATMServicePayment.objects.filter(year=year_a).values("month").annotate(tot=Sum("amount"))
        serv_b = ATMServicePayment.objects.filter(year=year_b).values("month").annotate(tot=Sum("amount"))
        serv_map_a = {r["month"]: cls.money(r["tot"]) for r in serv_a}
        serv_map_b = {r["month"]: cls.money(r["tot"]) for r in serv_b}

        # Oylik shartnoma to'lovi (BTech + Glob): ~288.65 mln so'm / oy
        btech_glob_monthly = 288651800.0

        months = []
        tot_inc_a, tot_inc_b = 0.0, 0.0
        tot_exp_a, tot_exp_b = 0.0, 0.0
        tot_cw_a, tot_cw_b = 0.0, 0.0

        for m in range(1, 13):
            inc_a, cw_a = map_a.get(m, (0.0, 0.0))
            inc_b, cw_b = map_b.get(m, (0.0, 0.0))

            has_data_a = inc_a > 0 or cw_a > 0 or m in maint_map_a or m in serv_map_a
            has_data_b = inc_b > 0 or cw_b > 0 or m in maint_map_b or m in serv_map_b

            exp_a = maint_map_a.get(m, 0.0) + serv_map_a.get(m, 0.0) + (btech_glob_monthly if has_data_a else 0.0)
            exp_b = maint_map_b.get(m, 0.0) + serv_map_b.get(m, 0.0) + (btech_glob_monthly if has_data_b else 0.0)

            net_a = inc_a - exp_a
            net_b = inc_b - exp_b

            tot_inc_a += inc_a
            tot_inc_b += inc_b
            tot_exp_a += exp_a
            tot_exp_b += exp_b
            tot_cw_a += cw_a
            tot_cw_b += cw_b

            months.append({
                "month": m,
                "name": cls.MONTH_NAMES[m - 1],
                "income_a": inc_a,
                "income_b": inc_b,
                "expense_a": exp_a,
                "expense_b": exp_b,
                "net_profit_a": net_a,
                "net_profit_b": net_b,
                "cash_withdrawal_a": cw_a,
                "cash_withdrawal_b": cw_b,
            })

        net_profit_a = tot_inc_a - tot_exp_a
        net_profit_b = tot_inc_b - tot_exp_b

        inc_diff = tot_inc_b - tot_inc_a
        inc_growth = round((inc_diff / tot_inc_a * 100), 2) if tot_inc_a > 0 else 0.0

        exp_diff = tot_exp_b - tot_exp_a
        exp_growth = round((exp_diff / tot_exp_a * 100), 2) if tot_exp_a > 0 else 0.0

        net_diff = net_profit_b - net_profit_a
        net_growth = round((net_diff / abs(net_profit_a) * 100), 2) if net_profit_a != 0 else 0.0

        cw_diff = tot_cw_b - tot_cw_a
        cw_growth = round((cw_diff / tot_cw_a * 100), 2) if tot_cw_a > 0 else 0.0

        return {
            "year_a": year_a,
            "year_b": year_b,
            "summary": {
                "income_a": tot_inc_a,
                "income_b": tot_inc_b,
                "income_diff": inc_diff,
                "income_growth_pct": inc_growth,
                "expense_a": tot_exp_a,
                "expense_b": tot_exp_b,
                "expense_diff": exp_diff,
                "expense_growth_pct": exp_growth,
                "net_profit_a": net_profit_a,
                "net_profit_b": net_profit_b,
                "net_profit_diff": net_diff,
                "net_profit_growth_pct": net_growth,
                "cash_withdrawal_a": tot_cw_a,
                "cash_withdrawal_b": tot_cw_b,
                "cash_withdrawal_diff": cw_diff,
                "cash_withdrawal_growth_pct": cw_growth,
            },
            "months": months,
        }
