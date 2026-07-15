from rest_framework.views import APIView
from rest_framework.response import Response

from ...services.charts import DashboardChartService
from ..serializers.dashboard import DashboardSerializer
from ...services.dashboard import DashboardService

#
# class DashboardAPIView(APIView):
#
#     def get(self, request):
#         print("DASHBOARD VIEW IS NEW")
#
#         return Response({
#
#             "summary": DashboardService.summary(),
#
#             "finance": DashboardService.finance(),
#
#             "maintenance": DashboardService.maintenance(),
#
#             "top_regions": DashboardService.top_regions(),
#
#             "status_chart": DashboardChartService.status_chart(),
#
#             "card_chart": DashboardChartService.card_chart(),
#
#         })


class DashboardAPIView(APIView):

    def get(self, request):
        return Response(
            DashboardService.dashboard()
        )