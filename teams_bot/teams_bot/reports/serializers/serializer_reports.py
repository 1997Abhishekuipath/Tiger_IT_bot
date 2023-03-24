from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    organization_id = serializers.IntegerField()
    bot_id = serializers.IntegerField(allow_null=True)
    platform = serializers.CharField(allow_null=True)
    report_type = serializers.CharField()
