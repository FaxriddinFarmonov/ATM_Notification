from dataclasses import dataclass
from typing import Any


from .query_router import (
    AnalyticsQueryRouter,
)
from .query_router import AnalyticsQueryRouter


@dataclass(frozen=True)
class ParsedQuestion:

    intent: str

    parameters: dict[str, Any]

class QuestionUnderstandingService:

    SUPPORTED_INTENTS = {

        "count_by_region",

        "revenue_by_region",

        "performance_by_atm",

        "trend_analysis",

    }

    @classmethod
    def understand(
        cls,
        question: str,
    ) -> ParsedQuestion:

        question = question.strip()

        if not question:

            raise ValueError(
                "Savol bo'sh bo'lishi mumkin emas."
            )

        normalized = question.lower()

        if (
            "nechta" in normalized
            and "bankomat" in normalized
        ):

            region = cls._extract_region(
                question
            )

            return ParsedQuestion(
                intent="count_by_region",

                parameters={
                    "region": region,
                },
            )

        raise ValueError(
            "Savolni tushunib bo'lmadi."
        )

    @staticmethod
    def _extract_region(
        question: str,
    ) -> str:

        regions = [

            "МАБ",

            "Тошкент",

            "Самарканд",

            "Навоий",

            "Бухоро",

            "Андижон",

            "Фарғона",

            "Наманган",

        ]

        question_lower = question.lower()

        for region in regions:

            if region.lower() in question_lower:

                return region

        raise ValueError(
            "Savolda region aniqlanmadi."
        )



    class AnalyticsQuestionService:

        @classmethod
        def ask(
                cls,
                question: str,
        ) -> dict:
            parsed = (
                QuestionUnderstandingService
                .understand(question)
            )

            result = AnalyticsQueryRouter.route(
                intent=parsed.intent,
                **parsed.parameters,
            )

            return {
                "question": question,

                "intent": parsed.intent,

                "parameters": parsed.parameters,

                "result": result,
            }

        @classmethod
        def understand(
                cls,
                question: str,
        ) -> ParsedQuestion:

            question = question.strip()

            if not question:
                raise ValueError(
                    "Savol bo'sh bo'lishi mumkin emas."
                )

            normalized = question.lower()

            # 1. ATM COUNT
            if (
                    "nechta" in normalized
                    and "bankomat" in normalized
            ):
                region = cls._extract_region(
                    question
                )

                return ParsedQuestion(
                    intent="count_by_region",
                    parameters={
                        "region": region,
                    },
                )

            # 2. REGION REVENUE
            if (
                    (
                            "daromad" in normalized
                            or "daromadi" in normalized
                            or "income" in normalized
                    )
                    and (
                    "region" in normalized
                    or "viloyat" in normalized
                    or "filial" in normalized
            )
            ):
                region = cls._extract_region(
                    question
                )

                return ParsedQuestion(
                    intent="revenue_by_region",
                    parameters={
                        "region": region,
                    },
                )

            # 3. ATM PERFORMANCE
            if (
                    "bankomat" in normalized
                    and (
                    "ishlayapti" in normalized
                    or "holati" in normalized
                    or "performance" in normalized
                    or "daromadi" in normalized
            )
            ):
                atm_id = cls._extract_atm_id(
                    question
                )

                return ParsedQuestion(
                    intent="performance_by_atm",
                    parameters={
                        "atm_id": atm_id,
                    },
                )

            # 4. ATM TREND
            if (
                    (
                            "oxirgi" in normalized
                            or "oylik" in normalized
                            or "trend" in normalized
                            or "oyda" in normalized
                    )
                    and (
                    "bankomat" in normalized
                    or "atm" in normalized
            )
            ):
                atm_id = cls._extract_atm_id(
                    question
                )

                months = cls._extract_months(
                    question
                )

                return ParsedQuestion(
                    intent="trend_analysis",
                    parameters={
                        "atm_id": atm_id,
                        "months": months,
                    },
                )

            raise ValueError(
                "Savolni tushunib bo'lmadi."
            )

        @staticmethod
        def _extract_atm_id(
                question: str,
        ) -> int:

            import re

            match = re.search(
                r"\b(?:atm|bankomat|id)\s*#?\s*(\d+)\b",
                question.lower(),
            )

            if not match:
                raise ValueError(
                    "Savolda ATM ID aniqlanmadi."
                )

            return int(
                match.group(1)
            )

        @staticmethod
        def _extract_months(
                question: str,
        ) -> int:

            import re

            match = re.search(
                r"(\d+)\s*oy",
                question.lower(),
            )

            if match:
                months = int(
                    match.group(1)
                )

                return min(
                    max(months, 1),
                    24,
                )

            return 3