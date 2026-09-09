from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from ..serializers.dashboard import DashboardSerializer
from ...services.dashboard import DashboardService


@extend_schema(
    tags=["Dashboard"],
    summary="Dashboard to'liq tahliliy ko'rsatkichlari",
    description=(
        "Asosiy boshqaruv paneli uchun barcha ko'rsatkichlar: "
        "Umumiy holat (jami/faol/soz/nosoz), Moliya (daromad/xarajat/foyda), "
        "Ta'mirlash statistikasi, Top viloyatlar, Status grafigi, Karta turlari grafigi, "
        "Oylik moliyaviy dinamika, Modellar bo'yicha taqsimot, Ta'mirlash trendi va "
        "oxirgi 10 ta ta'mirlash aktlari."
    ),
    responses={200: DashboardSerializer},
)
class DashboardAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(
            DashboardService.dashboard()
        )