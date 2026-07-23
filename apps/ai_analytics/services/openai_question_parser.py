import json

from django.conf import settings
from openai import OpenAI

from .question_understanding import ParsedQuestion


class OpenAIQuestionParser:

    MODEL = "gpt-4o-mini"

    SYSTEM_PROMPT = """
You are an analytics question parser for an ATM banking analytics system.

Your job is ONLY to understand the user's question and return valid JSON.

Supported intents:

1. count_by_region
Parameters:
{
    "region": string
}

2. revenue_by_region
Parameters:
{
    "region": string
}

3. performance_by_atm
Parameters:
{
    "atm_id": integer
}

4. trend_analysis
Parameters:
{
    "atm_id": integer,
    "months": integer
}

Return ONLY JSON in this format:

{
    "intent": "intent_name",
    "parameters": {}
}

Rules:

- Never answer the user's question.
- Never invent ATM IDs.
- Never invent regions.
- If months are not specified for trend_analysis, use 3.
- The user may make spelling mistakes.
- Understand Uzbek, Russian and English.
- Understand words like:
  ATM, bankomat, банкомат.
- Region may be written in different languages or with spelling mistakes.
"""
    @classmethod
    def parse(
        cls,
        question: str,
    ) -> ParsedQuestion:

        if not question or not question.strip():

            raise ValueError(
                "Savol bo'sh bo'lishi mumkin emas."
            )

        client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        response = client.chat.completions.create(

            model=cls.MODEL,

            temperature=0,

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",
                    "content": cls.SYSTEM_PROMPT,
                },

                {
                    "role": "user",
                    "content": question,
                },

            ],
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        data = json.loads(content)

        return cls._validate_result(
            data
        )
    @classmethod
    def _validate_result(
        cls,
        data: dict,
    ) -> ParsedQuestion:

        if not isinstance(data, dict):

            raise ValueError(
                "AI noto'g'ri format qaytardi."
            )

        intent = data.get(
            "intent"
        )

        parameters = data.get(
            "parameters"
        )

        supported_intents = {

            "count_by_region",

            "revenue_by_region",

            "performance_by_atm",

            "trend_analysis",

        }

        if intent not in supported_intents:

            raise ValueError(
                f"Noma'lum intent: {intent}"
            )

        if not isinstance(
            parameters,
            dict,
        ):

            raise ValueError(
                "AI parameters noto'g'ri formatda."
            )

        if intent in {

            "count_by_region",

            "revenue_by_region",

        }:

            region = parameters.get(
                "region"
            )

            if not region:

                raise ValueError(
                    "Region aniqlanmadi."
                )

        if intent in {

            "performance_by_atm",

            "trend_analysis",

        }:

            atm_id = parameters.get(
                "atm_id"
            )

            if not isinstance(
                atm_id,
                int,
            ):

                raise ValueError(
                    "ATM ID noto'g'ri."
                )

        if intent == "trend_analysis":

            months = parameters.get(
                "months",
                3,
            )

            if not isinstance(
                months,
                int,
            ):

                raise ValueError(
                    "Months noto'g'ri."
                )

            parameters["months"] = min(
                max(months, 1),
                24,
            )

        return ParsedQuestion(

            intent=intent,

            parameters=parameters,

        )
    