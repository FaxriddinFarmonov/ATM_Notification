from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.Bankomat_hisobot.filters.atm_filter import ATMFilter
from apps.Bankomat_hisobot.models import ATMTURON
from apps.Bankomat_hisobot.services.atm_detail_queryset import ATMDetailQuerySet
from apps.Bankomat_hisobot.services.excel_exporter import ATMExcelExporter
from apps.Bankomat_hisobot.services.full_excel_exporter import FullATMExcelExporter


from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiResponse

class ATMExcelExportAPIView(APIView):
    """
    Download Excel report for a single ATM.

    GET /api/v1/atms/<terminal_id>/export/
    """

    @extend_schema(
        tags=["ATM"],
        operation_id="v1_atm_single_excel_export",
        summary="Bitta bankomatning to'liq Excel hisoboti",
        description="Ko'rsatilgan ID yoki TID dagi bitta bankomatning barcha moliyaviy va texnik ma'lumotlarini .xlsx Excel fayl ko'rinishida yuklab olish.",
        responses={
            (200, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"): OpenApiTypes.BINARY,
        },
    )
    def get(self, request, pk):

        atm = ATMDetailQuerySet.get(pk)

        exporter = ATMExcelExporter(
            atm=atm,
        )

        return exporter.build_response()


class FullATMExcelExportAPIView(GenericAPIView):

    """
    Download Excel report for all ATMs.

    Supports all ATM filters.

    Example:

    /api/v1/atms/export/

    /api/v1/atms/export/?region=МАБ

    /api/v1/atms/export/?card_type=UZCARD

    /api/v1/atms/export/?region=МАБ&card_type=UZCARD
    """

    queryset = (
        ATMTURON.objects
        .all()
    )

    filter_backends = (
        DjangoFilterBackend,
    )

    filterset_class = ATMFilter

    serializer_class = None

    @extend_schema(
        tags=["ATM"],
        operation_id="v1_atms_bulk_excel_export",
        summary="Barcha bankomatlarning umumiy Excel hisoboti",
        description=(
            "Barcha yoki filtrlangan bankomatlar ro'yxatini to'liq Excel (.xlsx) fayl qilib yuklab olish. "
            "Filtrlar: region, card_type, model, terminal_id, is_active."
        ),
        responses={
            (200, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"): OpenApiTypes.BINARY,
        },
    )
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(
            self.get_queryset()
        )

        exporter = FullATMExcelExporter(
            queryset=queryset,
        )

        output = exporter.export()

        response = HttpResponse(
            output.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )

        response["Content-Disposition"] = (
            'attachment; filename="ATM_Report.xlsx"'
        )

        return response