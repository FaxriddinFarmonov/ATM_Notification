import json

from ollama import chat

from .question_understanding import ParsedQuestion


class OllamaQuestionParser:

    MODEL = "qwen3:4b"

    SYSTEM_PROMPT = """
You are an intent parser for an ATM banking analytics system.

Your task is NOT to answer the user.

Your task is ONLY to understand the question
and return structured JSON.

Supported intents:

1. count_by_region

Example:
"МАБ regionida nechta bankomat bor?"

Return:
{
    "intent": "count_by_region",
    "parameters": {
        "region": "МАБ"
    }
}

2. revenue_by_region

Example:
"МАБ regionining daromadi qancha?"

Return:
{
    "intent": "revenue_by_region",
    "parameters": {
        "region": "МАБ"
    }
}

3. performance_by_atm

Example:
"56-raqamli bankomat qanday ishlayapti?"

Return:
{
    "intent": "performance_by_atm",
    "parameters": {
        "atm_id": 56
    }
}

4. trend_analysis

Example:
"56-raqamli bankomatning oxirgi 3 oylik trendi qanday?"

Return:
{
    "intent": "trend_analysis",
    "parameters": {
        "atm_id": 56,
        "months": 3
    }
}

Rules:

- Understand Uzbek, Russian and English.
- Understand spelling mistakes.
- Do not answer the question.
- Do not invent database data.
- Do not explain anything.
- Return ONLY valid JSON.
"""
    @classmethod
    def parse(
        cls,
        question: str,
    ) -> ParsedQuestion:

        response = chat(

            model=cls.MODEL,

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

            format="json",

        )

        content = (
            response["message"]["content"]
        )

        data = json.loads(
            content
        )

        return ParsedQuestion(

            intent=data["intent"],

            parameters=data["parameters"],

        )
    