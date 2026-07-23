from .analytics_question import (
    AnalyticsQuestionService,
)

from .analytics_response_formatter import (
    AnalyticsResponseFormatter,
)


class AnalyticsReportService:

    @classmethod
    def generate(
            cls,
            question: str,
    ) -> dict:

        result = (
            AnalyticsQuestionService
            .ask(
                question
            )
        )

        if not result:
            return {
                "success": False,
                "question": question,
                "error": (
                    "Savolni tahlil qilib bo'lmadi."
                ),
            }

        intent = result.get(
            "intent"
        )

        parameters = result.get(
            "parameters",
            {}
        )

        data = result.get(
            "result"
        )

        if data is None:
            return {
                "success": False,
                "question": question,
                "intent": intent,
                "parameters": parameters,
                "error": (
                    "Analitik ma'lumot topilmadi."
                ),
            }

        report = (
            AnalyticsResponseFormatter
            .format(
                intent=intent,
                result=data,
            )
        )

        return {
            "success": True,
            "question": question,
            "intent": intent,
            "parameters": parameters,
            "data": data,
            "report": report,
        }