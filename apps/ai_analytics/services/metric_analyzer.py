
from decimal import Decimal


class MetricAnalyzer:

    @classmethod
    def analyze(
        cls,
        data: dict,
    ) -> dict:

        return {
            "income": cls.analyze_metric(
                "income",
                data.get("income", {}),
            ),
            "expense": cls.analyze_metric(
                "expense",
                data.get("expense", {}),
            ),
            "profit": cls.analyze_metric(
                "profit",
                data.get("profit", {}),
            ),
        }

    @classmethod
    def analyze_metric(
            cls,
            name: str,
            metric: dict,
    ) -> dict:
        previous = Decimal(
            str(
                metric.get(
                    "first",
                    0,
                )
            )
        )

        current = Decimal(
            str(
                metric.get(
                    "last",
                    0,
                )
            )
        )
        difference = current - previous
        if previous == 0:

            percent = None

        else:

            percent = (
                              difference
                              / abs(previous)
                      ) * 100
        if difference > 0:

            trend = "up"

        elif difference < 0:

            trend = "down"

        else:

            trend = "stable"
        status = "normal"

        if name == "profit":

            if current < 0:
                status = "critical"

        elif name == "expense":

            if difference > 0:
                status = "warning"

        elif name == "income":

            if difference > 0:
                status = "good"
        return {

            "metric": name,

            "previous": previous,

            "current": current,

            "difference": difference,

            "percent_change": percent,

            "trend": trend,

            "status": status,
        }