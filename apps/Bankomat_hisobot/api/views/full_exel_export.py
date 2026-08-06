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


class ATMExcelExportAPIView(APIView):
    """
    Download Excel report for a single ATM.

    GET /api/v1/atms/<terminal_id>/export/
    """


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