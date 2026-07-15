# dasdasdasd
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema
from ..pagination import ATMListPagination
from ..serializers.atm_filter import ATMFilterSerializer
from ..serializers.atm_list import ATMListSerializer
from ...services.atm_filters import ATMFilterService
from ...services.atm_queryset import ATMQuerySet
from ...services.atm_search import ATMSearchService
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
@extend_schema(
    tags=["ATM"],

    summary="ATM list",

    description=(
        "Returns a paginated list of ATMs. "
        "Supports search and filtering by "
        "status, region, card type, model "
        "and active status."
    ),

    parameters=[

        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Search by ATM name, region, "
                "terminal ID, merchant ID, "
                "serial number, address or model."
            ),
        ),

        OpenApiParameter(
            name="status",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "ATM technical status. "
                "Available values: SOZ, NOSOZ."
            ),
        ),

        OpenApiParameter(
            name="region",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter ATMs by region.",
        ),

        OpenApiParameter(
            name="card_type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Card type. "
                "Available values: UZCARD, HUMO."
            ),
        ),

        OpenApiParameter(
            name="model",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter ATMs by model.",
        ),

        OpenApiParameter(
            name="is_active",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Filter by active status. "
                "true or false."
            ),
        ),

    ],
)
class ATMListAPIView(ListAPIView):

    serializer_class = ATMListSerializer

    pagination_class = ATMListPagination

    def get_queryset(self):

        queryset = ATMQuerySet.list()

        search = (
            self.request.query_params.get(
                "search"
            )
        )

        queryset = ATMSearchService.apply(
            queryset=queryset,
            search=search,
        )

        serializer = ATMFilterSerializer(
            data=self.request.query_params
        )

        serializer.is_valid(
            raise_exception=True
        )

        queryset = ATMFilterService.apply(
            queryset=queryset,
            filters=serializer.validated_data,
        )

        return queryset