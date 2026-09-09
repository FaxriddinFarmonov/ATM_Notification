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


from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

@extend_schema(
    tags=["Maintenance"],
    summary="Ta'mirlash va ehtiyot qismlar ro'yxati",
    description="Protokollar bo'yicha bankomatlarga o'rnatilgan ehtiyot qismlar, bajarilgan ta'mirlash ishlari va xarajatlar ro'yxati (qidiruv va filtrlar bilan).",
    parameters=[
        OpenApiParameter(name="search", type=OpenApiTypes.STR, required=False, description="Ehtiyot qism nomi, seriya raqami yoki filial bo'yicha qidiruv"),
        OpenApiParameter(name="region", type=OpenApiTypes.STR, required=False, description="Viloyat"),
        OpenApiParameter(name="terminal_id", type=OpenApiTypes.STR, required=False, description="Terminal ID (TID)"),
        OpenApiParameter(name="serial_number", type=OpenApiTypes.STR, required=False, description="Seriya raqami"),
        OpenApiParameter(name="part_name", type=OpenApiTypes.STR, required=False, description="Ehtiyot qism nomi"),
        OpenApiParameter(name="protocol_number", type=OpenApiTypes.STR, required=False, description="Protokol raqami"),
        OpenApiParameter(name="date_from", type=OpenApiTypes.DATE, required=False, description="Boshlang'ich sana (YYYY-MM-DD)"),
        OpenApiParameter(name="date_to", type=OpenApiTypes.DATE, required=False, description="Tugash sanasi (YYYY-MM-DD)"),
    ],
    responses={200: MaintenanceListSerializer(many=True)},
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


@extend_schema(
    tags=["Maintenance"],
    summary="Bitta ta'mirlash elementi batafsil ma'lumoti",
    description="Tanlangan ta'mirlash yozuvining barcha parametrlari (ehtiyot qism narxi, QQS, miqdori va protokol ma'lumotlari).",
    responses={200: MaintenanceDetailSerializer},
)
class MaintenanceDetailAPIView(
    RetrieveAPIView
):

    serializer_class = (
        MaintenanceDetailSerializer
    )

    queryset = (
        MaintenanceItem.objects.all()
    )