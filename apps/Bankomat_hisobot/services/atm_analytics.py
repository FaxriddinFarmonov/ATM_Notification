from statistics import mean
from django.db.models import Sum
from statistics import mean


class ATMAnalyticsService:
    MONEY_MULTIPLIER = 1000

    @classmethod
    def money(cls, value):
        return float(value or 0) * cls.MONEY_MULTIPLIER

    def __init__(self, atm):

        self.atm = atm

        self.monthly = list(
            atm.monthly_statistics.all()
        )

        self.yearly = list(
            atm.year_statistics.all()
        )

        self.contract = getattr(
            atm,
            "service_contract",
            None,
        )

        self.technical = getattr(
            atm,
            "technical",
            None,
        )

    def build(self):

        return {

            "summary": self.summary(),

            "financial": self.financial(),

            "technical": self.technical_information(),

            "service": self.service_information(),

            "trend": self.trend_analysis(),

            "risk": self.risk_analysis(),

            "health": self.health_score(),

            "forecast": self.forecast(),
            "last_6_months": self.last_6_months(),

        }

    def summary(self):
        latest = self.monthly[0] if self.monthly else None

        return {

            "region": self.atm.region,

            "name": self.atm.name,

            "terminal_id": (
                self.technical.terminal_id
                if self.technical else None
            ),

            "status": (
                self.technical.status
                if self.technical else None
            ),

            "model": self.atm.model,

            "latest_year": (
                latest.year if latest else None
            ),

            "latest_month": (
                latest.month if latest else None
            ),

        }

    def financial(self):
        if not self.monthly:
            return {}

        incomes = [
            self.money(i.income)
            for i in self.monthly
        ]

        expenses = [
            self.money(i.expense)
            for i in self.monthly
        ]

        return {

            "average_income": round(
                mean(incomes),
                2,
            ),

            "average_expense": round(
                mean(expenses),
                2,
            ),

            "max_income": max(incomes),

            "min_income": min(incomes),

            "max_expense": max(expenses),

            "min_expense": min(expenses),

            "last_income": incomes[0],

            "last_expense": expenses[0],

        }

    def technical_information(self):

        if not self.technical:
            return {}

        return {

            "status": self.technical.status,

            "serial_number": self.technical.serial_number,

            "inventory_number": self.technical.inventory_number,

        }

    def maintenance_summary(self):

        if not self.technical:
            return {
                "repair_cost": 0,
                "quantity": 0,
            }

        data = self.technical.maintenance_items.aggregate(

            repair_cost=Sum("total_with_vat"),

            quantity=Sum("quantity"),

        )

        return {

            "repair_cost": float(
                data["repair_cost"] or 0
            ),

            "quantity": data["quantity"] or 0,

        }

    def service_information(self):

        if not self.contract:
            return {}

        total = sum(
            self.money(p.amount)
            for p in self.contract.payments.all()
        )

        return {

            "btech_monthly_fee": self.money(
                self.contract.btech_monthly_fee
            ),

            "glob_monthly_fee": self.money(
                self.contract.glob_monthly_fee
            ),

            "payment_count": self.contract.payments.count(),

            "total_payment": total,

        }

    def build(self):

        return {

            "summary": self.summary(),

            "financial": self.financial(),

            "technical": self.technical_information(),

            "service": self.service_information(),

            "trend": self.trend_analysis(),

            "risk": self.risk_analysis(),

            "health": self.health_score(),

            "forecast": self.forecast(),
            "anomalies": self.anomalies(),

        }

    def trend_analysis(self):

        if len(self.monthly) < 2:
            return {}

        latest = self.monthly[0]

        previous = self.monthly[1]

        income_change = float(latest.income) - float(previous.income)

        expense_change = float(latest.expense) - float(previous.expense)

        return {

            "income_change": round(
                income_change,
                2,
            ),

            "expense_change": round(
                expense_change,
                2,
            ),

            "income_trend": (
                "UP"
                if income_change > 0
                else "DOWN"
                if income_change < 0
                else "STABLE"
            ),

            "expense_trend": (
                "UP"
                if expense_change > 0
                else "DOWN"
                if expense_change < 0
                else "STABLE"
            ),

        }

    def health_score(self):

        score = 100

        if self.technical:

            if self.technical.status != "SOZ":
                score -= 30

        maintenance = self.maintenance_summary()

        if maintenance["repair_cost"] > 0:
            score -= 20

        return {

            "score": max(score, 0),

            "status": (

                "Excellent"

                if score >= 90

                else "Good"

                if score >= 75

                else "Average"

                if score >= 60

                else "Critical"

            ),

        }

    def risk_analysis(self):

        risk = 0

        maintenance = self.maintenance_summary()

        if maintenance["repair_cost"] > 0:
            risk += 30

        if self.technical:

            if self.technical.status != "SOZ":
                risk += 40

        if self.contract:

            if self.contract.payments.count() == 0:
                risk += 10

        return {

            "score": risk,

            "level": (

                "LOW"

                if risk < 30

                else "MEDIUM"

                if risk < 60

                else "HIGH"

            ),

        }
    def forecast(self):

        if len(self.monthly) < 3:
            return {}

        income = round(

            mean(

                self.money(i.income)

                for i in self.monthly[:3]

            ),

            2,

        )

        expense = round(

            mean(

                self.money(i.expense)

                for i in self.monthly[:3]

            ),

            2,

        )

        return {

            "expected_income": income,

            "expected_expense": expense,

        }

    def last_6_months(self):

        months = self.monthly[:6]

        if not months:
            return {}

        incomes = [
            self.money(i.income)
            for i in months
        ]

        expenses = [
            self.money(i.expense)
            for i in months
        ]

        highest_income = max(
            months,
            key=lambda x: float(x.income),
        )

        lowest_income = min(
            months,
            key=lambda x: float(x.income),
        )

        highest_expense = max(
            months,
            key=lambda x: float(x.expense),
        )

        lowest_expense = min(
            months,
            key=lambda x: float(x.expense),
        )

        growth = 0

        if incomes[-1] > 0:
            growth = (

                             (incomes[0] - incomes[-1])

                             / incomes[-1]

                     ) * 100

        return {

            "months": len(months),

            "average_income": round(
                mean(incomes),
                2,
            ),

            "average_expense": round(
                mean(expenses),
                2,
            ),

            "highest_income": {

                "year": highest_income.year,

                "month": highest_income.month,

                "amount": self.money(
                    highest_income.income
                ),

            },

            "lowest_income": {

                "year": lowest_income.year,

                "month": lowest_income.month,

                "amount": self.money(
                    lowest_income.income
                ),

            },

            "highest_expense": {

                "year": highest_expense.year,

                "month": highest_expense.month,

                "amount": self.money(
                    highest_expense.expense
                ),

            },

            "lowest_expense": {

                "year": lowest_expense.year,

                "month": lowest_expense.month,

                "amount": self.money(
                    lowest_expense.expense
                ),

            },

            "income_growth_percent": round(
                growth,
                2,
            ),

        }

    def anomalies(self):

        result = []

        if len(self.monthly) < 2:
            return result

        for i in range(len(self.monthly) - 1):

            current = self.monthly[i]
            previous = self.monthly[i + 1]

            current_income = float(current.income)
            previous_income = float(previous.income)

            current_expense = float(current.expense)
            previous_expense = float(previous.expense)

            # Daromad o'zgarishi
            if previous_income > 0:

                income_change = (
                                        (current_income - previous_income)
                                        / previous_income
                                ) * 100

                if abs(income_change) >= 20:
                    result.append({

                        "type": "income",

                        "year": current.year,

                        "month": current.month,

                        "change_percent": round(
                            income_change,
                            2,
                        ),

                        "message": (
                            "Daromad keskin oshgan"
                            if income_change > 0
                            else "Daromad keskin pasaygan"
                        ),

                    })

            # Xarajat o'zgarishi
            if previous_expense > 0:

                expense_change = (
                                         (current_expense - previous_expense)
                                         / previous_expense
                                 ) * 100

                if abs(expense_change) >= 20:
                    result.append({

                        "type": "expense",

                        "year": current.year,

                        "month": current.month,

                        "change_percent": round(
                            expense_change,
                            2,
                        ),

                        "message": (
                            "Xarajat keskin oshgan"
                            if expense_change > 0
                            else "Xarajat keskin kamaygan"
                        ),

                    })

            # Nol xarajat
            if current_expense == 0:
                result.append({

                    "type": "expense_zero",

                    "year": current.year,

                    "month": current.month,

                    "message": "Xarajat 0 bo'lgan",

                })

        return result
