from .ollama_question_parser import (
    OllamaQuestionParser,
)

from .query_router import (
    AnalyticsQueryRouter,
)


class AnalyticsQuestionService:

    @staticmethod
    def ask(question: str):

        parsed = (
            OllamaQuestionParser
            .parse(question)
        )

        result = (
            AnalyticsQueryRouter
            .route(
                intent=parsed.intent,
                **parsed.parameters,
            )
        )

        return {

            "question": question,

            "intent": parsed.intent,

            "parameters": parsed.parameters,

            "result": result,

        }