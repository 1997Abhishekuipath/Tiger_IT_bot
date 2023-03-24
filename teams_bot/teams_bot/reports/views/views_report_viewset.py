from django.http import FileResponse
from rest_framework import generics, response, status

from reports.serializers.serializer_reports import ReportSerializer
from reports.views.views_reports import ReportData


# Create your views here.
class ReportViewSet(generics.GenericAPIView):
    permission_set = []
    permission_classes = []
    serializer_class = ReportSerializer

    def post(self, request):
        print(request.data)
        serializer_request = self.serializer_class(data=request.data)
        serializer_request.is_valid(raise_exception=True)
        request_data = serializer_request.validated_data
        report = ReportData(organization_id=request_data['organization_id'],
                            bot_id=request_data['bot_id'],
                            platform=request_data['platform'],
                            start_date=request_data['start_date'],
                            end_date=request_data['end_date']
                            )

        if request_data.get('report_type') == 'fallback_messages':
            res = report.fallback_messages()

        elif request_data.get('report_type') == 'feedback_messages':
            res = report.feedback_forms()
        elif request_data.get('report_type') == 'bot_users':
            res = report.bot_users()
        elif request_data.get('report_type') == 'total_messages':
            res = report.total_messages()
        elif request_data.get('report_type') == 'new_users':
            res = report.new_users()
        elif request_data.get('report_type') == 'bot_ratings':
            res = report.bot_ratings()

        if res == "Error":
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            file = open(res, 'rb')
            resp = FileResponse(file)
            return resp
