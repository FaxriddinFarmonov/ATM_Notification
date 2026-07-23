from .header_classifier import HeaderClassifier
# from ..service_registry import ServiceRegistry
from .header_classifier import HeaderClassifier
# from .service_registry import ServiceRegistry

from .header_classifier import HeaderClassifier
from .header_classifier import HeaderClassifier


class SchemaBuilder:

    @classmethod
    def build(cls, headers):

        schema = []

        for index, header in enumerate(headers):

            column = HeaderClassifier.classify(
                index=index,
                header=header,
            )

            schema.append(column)

        return schema