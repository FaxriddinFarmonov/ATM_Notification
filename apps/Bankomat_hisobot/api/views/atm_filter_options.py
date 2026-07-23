from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from ...services.atm_filter_options import (
    ATMFilterOptionsService,
)


@extend_schema(
    tags=["ATM"],
    summary="ATM filter options",
    description=(
        "Returns all available filter values for ATM list page. "
        "Frontend should call this endpoint once and use the "
        "returned values to populate filter dropdowns."
    ),
    responses={
        200: OpenApiResponse(
            description="Filter options returned successfully."
        )
    },
)
class ATMFilterOptionsAPIView(APIView):

    permission_classes = (AllowAny,)

    authentication_classes = ()

    def get(self, request):

        return Response(
            ATMFilterOptionsService.get()
        )