from __future__ import annotations

from typing import Any

from apps.ai_analytics.services.ollama_entity_parser import (
    OllamaEntityParser,
)

from apps.ai_analytics.services.entity_resolver import (
    ATMEntityResolver,
)


class AIEntitySearchService:

    @classmethod
    def search(
        cls,
        question: str,
    ) -> dict:

        # 1. Ollama savolni tushunadi
        entities = (
            OllamaEntityParser.parse(
                question
            )
        )

        # 2. AI natijasini tozalaymiz
        entities = cls.normalize_entities(
            entities
        )

        # 3. Real bazadan qidiramiz
        result = (
            ATMEntityResolver.resolve(
                **entities
            )
        )

        return {

            "question": question,

            "entities": entities,

            "result": result,

        }

    @staticmethod
    def normalize_entities(
        entities: dict[str, Any],
    ) -> dict[str, Any]:

        """
        Ollama noto'g'ri fieldga
        joylashtirgan qiymatlarni
        professional tarzda tuzatadi.
        """

        entities = dict(entities)

        # ---------------------------------
        # MODEL DETECTION
        # ---------------------------------

        serial_number = (
            entities.get(
                "serial_number"
            )
        )

        model = (
            entities.get(
                "model"
            )
        )

        if serial_number and not model:

            if AIEntitySearchService.is_model(
                serial_number
            ):

                entities["model"] = (
                    serial_number
                )

                entities[
                    "serial_number"
                ] = None

        # ---------------------------------
        # STATUS DETECTION
        # ---------------------------------

        status = (
            entities.get(
                "status"
            )
        )

        if not status:

            status = (
                AIEntitySearchService.detect_status(
                    entities
                )
            )

            if status:

                entities["status"] = (
                    status
                )

        # ---------------------------------
        # CARD TYPE
        # ---------------------------------

        card_type = (
            entities.get(
                "card_type"
            )
        )

        if card_type:

            entities["card_type"] = (
                card_type.upper()
            )

        return entities

    @staticmethod
    def is_model(
        value: str,
    ) -> bool:

        value = (
            str(value)
            .strip()
            .upper()
        )

        model_keywords = (

            "NCR",

            "WINCOR",

            "DIEBOLD",

            "HYOSUNG",

            "HANTLE",

            "GRG",

            "OKI",

        )

        return value.startswith(
            model_keywords
        )

    @staticmethod
    def detect_status(
        entities: dict,
    ) -> str | None:

        """
        AI statusni o'tkazib yuborsa,
        mavjud entity qiymatlaridan
        aniqlashga harakat qiladi.
        """

        for value in entities.values():

            if not value:

                continue

            value = (
                str(value)
                .strip()
                .upper()
            )

            if value in {

                "SOZ",

                "NOSOZ",

            }:

                return value

        return None