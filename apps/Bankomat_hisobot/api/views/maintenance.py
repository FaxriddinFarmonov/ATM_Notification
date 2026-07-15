from rest_framework.generics import ListAPIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

from ..serializers.maintenance_detail import (
    MaintenanceDetailSerializer,
)

from apps.maintenance.models import MaintenanceItem
from ..pagination import MaintenancePagination
from ..serializers.maintenance import MaintenanceListSerializer
from ..serializers.maintenance_filter import (
    MaintenanceFilterSerializer,
)

from ...services.maintenance_queryset import (
    MaintenanceQuerySet,
)

from ...services.maintenance_search import (
    MaintenanceSearchService,
)

from ...services.maintenance_filters import (
    MaintenanceFilterService,
)


class MaintenanceListAPIView(ListAPIView):

    serializer_class = MaintenanceListSerializer
    pagination_class = MaintenancePagination

    def get_queryset(self):

        # 1. Base QuerySet
        queryset = MaintenanceQuerySet.list()

        # 2. Validate filters
        serializer = MaintenanceFilterSerializer(
            data=self.request.query_params
        )

        serializer.is_valid(
            raise_exception=True
        )

        filters = serializer.validated_data

        # 3. Search
        queryset = MaintenanceSearchService.apply(
            queryset=queryset,
            search=filters.get("search"),
        )

        # 4. Filters
        queryset = MaintenanceFilterService.apply(
            queryset=queryset,
            filters=filters,
        )

        return queryset

class MaintenanceDetailAPIView(
    RetrieveAPIView
):

    serializer_class = (
        MaintenanceDetailSerializer
    )

    queryset = (
        MaintenanceItem.objects.all()
    )