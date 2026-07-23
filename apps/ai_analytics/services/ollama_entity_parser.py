from __future__ import annotations
from .database_context import (
    DatabaseContextService
)
import json

import ollama


class OllamaEntityParser:

    MODEL = "qwen2.5:7b"

    SYSTEM_PROMPT = """
You are an ATM analytics entity extraction engine.

Your task is to extract ATM filters from the user's question.

Return ONLY valid JSON.

Allowed fields:

{
    "atm_id": null,
    "serial_number": null,
    "terminal_id": null,
    "merchant_id": null,
    "region": null,
    "model": null,
    "name": null,
    "status": null,
    "card_type": null,
    "is_active": null
}

Rules:

1. Never invent values.
2. If a value is not mentioned, return null.
3. Preserve the original value from the user question.
4. "soz" means "SOZ".
5. "nosoz", "nosoz bankomat" means "NOSOZ".
6. "humo" means "HUMO".
7. "uzcard" means "UZCARD".
8. Return JSON only.
"""

    @classmethod
    def parse(
        cls,
        question: str,
    ) -> dict:

        response = ollama.chat(

            model=cls.MODEL,

            messages=[

                {
                    "role": "system",

                    "content": (
                        cls.SYSTEM_PROMPT
                    ),
                },

                {
                    "role": "user",

                    "content": question,
                },

            ],

            format="json",

        )

        content = response["message"]["content"]

        data = json.loads(content)

        return cls._normalize(data)

    @staticmethod
    def _normalize(
        data: dict,
    ) -> dict:

        allowed_fields = {

            "atm_id",

            "serial_number",

            "terminal_id",

            "merchant_id",

            "region",

            "model",

            "name",

            "status",

            "card_type",

            "is_active",

        }

        result = {}

        for field in allowed_fields:

            value = data.get(field)

            if value in ("", "null"):

                value = None

            result[field] = value

        return result

    @classmethod
    def parse(
            cls,
            question: str,
    ) -> dict:

        database_context = (
            DatabaseContextService
            .get_context()
        )

        system_prompt = cls.build_prompt(
            database_context
        )

        response = ollama.chat(

            model=cls.MODEL,

            messages=[

                {
                    "role": "system",

                    "content": system_prompt,
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

        data = json.loads(content)

        return cls._normalize(data)

    @classmethod
    def build_prompt(
            cls,
            database_context: dict,
    ) -> str:

        return f"""
    You are an ATM database entity extraction engine.

    Your job is to extract entities from the user's question.

    IMPORTANT:

    You MUST use only values that exist
    in the database context below.

    DATABASE CONTEXT:

    Regions:
    {database_context["regions"]}

    Models:
    {database_context["models"]}

    Card types:
    {database_context["card_types"]}

    Statuses:
    {database_context["statuses"]}

    Return ONLY valid JSON.

    JSON schema:

    {{
        "atm_id": null,
        "serial_number": null,
        "terminal_id": null,
        "merchant_id": null,
        "region": null,
        "model": null,
        "name": null,
        "status": null,
        "card_type": null,
        "is_active": null
    }}

    RULES:

    1. Never invent a region.

    2. Never invent a model.

    3. Never invent a status.

    4. Never invent a card type.

    5. Match user words to the closest
    existing database value.

    6. "nosoz" means "NOSOZ".

    7. "soz" means "SOZ".

    8. "humo" means "HUMO".

    9. "uzcard" means "UZCARD".

    10. If a value is not found in the database,
    return null.

    11. NCR6622 is a MODEL if it exists
    in the database models list.

    12. Return JSON only.
    """