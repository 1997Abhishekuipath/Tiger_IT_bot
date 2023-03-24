from rest_framework import generics, response

from kpi.serializers.serializer_kpi import KpiSerializer
from kpi.views.views_kpi import Kpi


# Create your views here.
class KpiViewSet(generics.GenericAPIView):
    permission_set = []
    permission_classes = []
    serializer_class = KpiSerializer

    def post(self, request):
        print(request.data)
        serializer_request = self.serializer_class(data=request.data)
        serializer_request.is_valid(raise_exception=True)
        request_data = serializer_request.validated_data
        kpi = Kpi(organization_id=request_data['organization_id'],
                  bot_id=request_data['bot_id'],
                  platform=request_data['platform'],
                  start_date=request_data['start_date'],
                  end_date=request_data['end_date']
                  )

        if request_data['bot_id']:
            kpi.fallback_messages()
            kpi.feedback_forms()
            kpi.get_top_queries()
            kpi.total_messages()
            kpi.bot_users()
            kpi.new_users()
            kpi.bot_ratings()

        kpi.counts()
        print(kpi.data)
        return response.Response(kpi.data)
