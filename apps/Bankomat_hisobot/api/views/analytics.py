from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from ..swagger_constants import (
    AVAILABLE_REGIONS,
    AVAILABLE_YEARS,
    AVAILABLE_MONTHS,
    CARD_TYPE_CHOICES,
    PERIOD_CHOICES,
)
from ..serializers.analytics import (
    TopRegionsFilterSerializer,
    TopIncomeFilterSerializer,
    TopExpenseFilterSerializer,
    LossMakingFilterSerializer,
    OverviewFilterSerializer,
    RegionAnalyticsItemSerializer,
    TopIncomeATMSerializer,
    TopExpenseATMSerializer,
    LossMakingATMSerializer,
    ManagementOverviewResponseSerializer,
)
from ...services.analytics_service import (
    TopRegionsAnalyticsService,
    TopIncomeATMsService,
    TopExpenseATMsService,
    LossMakingRelocationService,
    ManagementOverviewService,
)


@extend_schema(
    tags=["Analytics"],
    summary="Viloyatlar kesimida moliyaviy tahlil va reyting (Top Regions)",
    description=(
        "Viloyatlarning haqiqiy daromadi, bankomatlardan yechilgan naqd pul aylanmasi, "
        "haqiqiy xarajatlari (zapchastlar + ijara + tok + inkassatsiya + servis), sof foydasi, "
        "rentabellik marjasi, faol/soz/nosoz bankomatlari soni va bitta bankomatga to'g'ri keluvchi o'rtacha ko'rsatkichlar."
    ),
    parameters=[
        OpenApiParameter(
            name="year",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_YEARS,
            description="Yilni tanlang (bo'sh qoldirilsa, oxirgi davr olinadi)",
        ),
        OpenApiParameter(
            name="month",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_MONTHS,
            description="Oyni tanlang (1-12)",
        ),
        OpenApiParameter(
            name="sort_by",
            type=OpenApiTypes.STR,
            required=False,
            enum=["income", "expense", "profit", "profit_margin", "atms_count", "cash_withdrawal"],
            description="Saralash ustunini tanlang (income, expense, profit, profit_margin, atms_count, cash_withdrawal)",
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            required=False,
            default=20,
            description="Maksimal hududlar soni (default: 20)",
        ),
    ],
    responses={200: RegionAnalyticsItemSerializer(many=True)},
)
class TopRegionsAnalyticsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        serializer = TopRegionsFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = TopRegionsAnalyticsService.get(
            year=data.get("year"),
            month=data.get("month"),
            sort_by=data.get("sort_by", "income"),
            limit=data.get("limit", 20),
        )
        return Response(result)


@extend_schema(
    tags=["Analytics"],
    summary="Eng ko'p daromad keltirgan bankomatlar (Top Revenue ATMs)",
    description=(
        "Bankomatlarning haqiqiy daromadi (income) bo'yicha reytingi. "
        "Yechilgan naqd pul aylanmasi (cash_withdrawal), qilingan haqiqiy xarajatlar (zapchast + ijara + tok + inkassatsiya), "
        "sof foyda (net_profit) va rentabellik marjasi bilan birga to'liq bankomat pasporti."
    ),
    parameters=[
        OpenApiParameter(
            name="period",
            type=OpenApiTypes.STR,
            required=False,
            enum=PERIOD_CHOICES,
            description="Davr turi (all: umumiy, yearly: yillik, monthly: oylik)",
        ),
        OpenApiParameter(
            name="year",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_YEARS,
            description="Yilni tanlang",
        ),
        OpenApiParameter(
            name="month",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_MONTHS,
            description="Oyni tanlang (1-12)",
        ),
        OpenApiParameter(
            name="region",
            type=OpenApiTypes.STR,
            required=False,
            enum=AVAILABLE_REGIONS,
            description="Viloyatni tanlang",
        ),
        OpenApiParameter(
            name="card_type",
            type=OpenApiTypes.STR,
            required=False,
            enum=CARD_TYPE_CHOICES,
            description="Karta turini tanlang (UZCARD yoki HUMO)",
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            required=False,
            default=10,
            description="Qaytariladigan bankomatlar soni (default: 10)",
        ),
    ],
    responses={200: TopIncomeATMSerializer(many=True)},
)
class TopIncomeATMsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        serializer = TopIncomeFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = TopIncomeATMsService.get(
            period=data.get("period", "all"),
            year=data.get("year"),
            month=data.get("month"),
            region=data.get("region"),
            card_type=data.get("card_type"),
            limit=data.get("limit", 10),
        )
        return Response(result)


@extend_schema(
    tags=["Analytics"],
    summary="Eng ko'p haqiqiy rasxod qilgan bankomatlar (Top Expense ATMs)",
    description=(
        "Bank uchun eng ko'p rasxod talab qilgan bankomatlar reytingi. "
        "Xarajatlar taqsimoti: ehtiyot qismlar va ta'mirlash, ijara to'lovi, elektr energiyasi, "
        "inkassatsiya xizmati va shartnoma to'lovlari (BTech, Glob). "
        "Shuningdek, bankomat qancha daromad bergani va sof natijasi (foyda/zarar)."
    ),
    parameters=[
        OpenApiParameter(
            name="expense_type",
            type=OpenApiTypes.STR,
            required=False,
            enum=["all", "maintenance", "rent", "electricity", "incassation"],
            description="Saralash xarajat turi (all, maintenance, rent, electricity, incassation)",
        ),
        OpenApiParameter(
            name="year",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_YEARS,
            description="Yilni tanlang",
        ),
        OpenApiParameter(
            name="month",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_MONTHS,
            description="Oyni tanlang",
        ),
        OpenApiParameter(
            name="region",
            type=OpenApiTypes.STR,
            required=False,
            enum=AVAILABLE_REGIONS,
            description="Viloyatni tanlang",
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            required=False,
            default=10,
            description="Qaytariladigan bankomatlar soni (default: 10)",
        ),
    ],
    responses={200: TopExpenseATMSerializer(many=True)},
)
class TopExpenseATMsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        serializer = TopExpenseFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = TopExpenseATMsService.get(
            expense_type=data.get("expense_type", "all"),
            year=data.get("year"),
            month=data.get("month"),
            region=data.get("region"),
            limit=data.get("limit", 10),
        )
        return Response(result)


@extend_schema(
    tags=["Analytics"],
    summary="Zarardagi bankomatlar va Joyini almashtirish (Relokatsiya) tavsiyalari",
    description=(
        "Haqiqiy xarajati daromadidan oshib ketayotgan muammoli bankomatlarni aniqlash. "
        "Bazadagi real ma'lumotlarga tayangan holda (Ollama ishlatilmaydi) qat'iy amaliy tavsiyalar: "
        "past aylanmali nuqtalarni savdo markazlariga ko'chirish (relokatsiya), yuqori ta'mirlash xarajatlilarni audit qilish, "
        "ijara stavkasini pasaytirish yoki inkassatsiya grafigini optimallashtirish."
    ),
    parameters=[
        OpenApiParameter(
            name="year",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_YEARS,
            description="Yilni tanlang",
        ),
        OpenApiParameter(
            name="month",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_MONTHS,
            description="Oyni tanlang",
        ),
        OpenApiParameter(
            name="region",
            type=OpenApiTypes.STR,
            required=False,
            enum=AVAILABLE_REGIONS,
            description="Viloyatni tanlang",
        ),
        OpenApiParameter(
            name="min_loss",
            type=OpenApiTypes.INT,
            required=False,
            description="Minimal zarar miqdori chegarasi (so'mda)",
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            required=False,
            default=20,
            description="Natijalar sonini tanlang (default: 20)",
        ),
    ],
    responses={200: LossMakingATMSerializer(many=True)},
)
class LossMakingATMsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        serializer = LossMakingFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = LossMakingRelocationService.get(
            year=data.get("year"),
            month=data.get("month"),
            region=data.get("region"),
            min_loss=data.get("min_loss", 0),
            limit=data.get("limit", 20),
        )
        return Response(result)


@extend_schema(
    tags=["Analytics"],
    summary="Boshqaruv uchun o'tgan oy va davriy tezkor KPI xulosasi (Executive Overview)",
    description=(
        "Front-end boshqaruv paneli va monitoring uchun to'liq moliyaviy KPI xulosa: "
        "tarmoqning jami daromadi, yechilgan naqd pul aylanmasi, jami haqiqiy xarajatlar, sof foyda, "
        "tarmoq rentabelligi, eng serdaromad bankomat, eng xarajatli bankomat, eng foydali viloyat va "
        "zararda ishlayotgan (joyini almashtirish tavsiya etilgan) bankomatlar soni."
    ),
    parameters=[
        OpenApiParameter(
            name="year",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_YEARS,
            description="Yilni tanlang (bo'sh qoldirilsa, oxirgi to'liq oy avtomatik hisoblanadi)",
        ),
        OpenApiParameter(
            name="month",
            type=OpenApiTypes.INT,
            required=False,
            enum=AVAILABLE_MONTHS,
            description="Oyni tanlang (1-12)",
        ),
    ],
    responses={200: ManagementOverviewResponseSerializer},
)
class AnalyticsOverviewAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        serializer = OverviewFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = ManagementOverviewService.get(
            year=data.get("year"),
            month=data.get("month"),
        )
        return Response(result)


class ModelAnalyticsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        from ...services.analytics_service import ModelAnalyticsService
        result = ModelAnalyticsService.get()
        return Response(result)


class AnnualFinancialsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        from ...services.analytics_service import AnnualFinancialsService
        result = AnnualFinancialsService.get()
        return Response(result)




class YearlyComparisonAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        from ...services.analytics_service import YearlyComparisonService
        year_a = request.query_params.get("year_a", 2025)
        year_b = request.query_params.get("year_b", 2026)
        result = YearlyComparisonService.get(year_a=year_a, year_b=year_b)
        return Response(result)
