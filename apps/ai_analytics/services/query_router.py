from .atm_analytics import ATMAnalyticsService


class AnalyticsQueryRouter:

    @staticmethod
    def route(
        intent: str,
        **kwargs,
    ):

        if intent == "count_by_region":

            return ATMAnalyticsService.count_by_region(
                kwargs["region"]
            )

        if intent == "revenue_by_region":

            return ATMAnalyticsService.revenue_by_region(
                kwargs["region"]
            )

        if intent == "performance_by_atm":

            return ATMAnalyticsService.performance_by_atm(
                kwargs["atm_id"]
            )

        if intent == "trend_analysis":

            return ATMAnalyticsService.trend_analysis(
                atm_id=kwargs["atm_id"],
                months=kwargs.get(
                    "months",
                    3,
                ),
            )

        raise ValueError(
            f"Unknown analytics intent: {intent}"
        )