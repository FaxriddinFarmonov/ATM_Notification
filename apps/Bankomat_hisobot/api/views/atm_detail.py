
from django.http import Http404
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema

from ...services.atm_detail_queryset import ATMDetailQuerySet
from ..serializers.atm_detail import ATMDetailSerializer


@extend_schema(
    tags=["ATM"],
    summary="ATM detail",
    description=(
        "Returns complete information about "
        "a single ATM including business data, "
        "technical data, monthly statistics "
        "and maintenance information."
    ),
)
class ATMDetailAPIView(RetrieveAPIView):

    serializer_class = ATMDetailSerializer

    lookup_field = "pk"

    def get_object(self):
        try:
            return ATMDetailQuerySet.get(
                self.kwargs["pk"]
            )
        except Exception:
            raise Http404("ATM not found")