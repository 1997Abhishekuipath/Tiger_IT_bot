from rest_framework import generics, response

from bot.models import Bot
from bot.serializers.serializer_bot import BotSerializer


class BotViewSet(generics.GenericAPIView):
    permission_classes = []
    serializer_class = BotSerializer

    def post(self, request):
        print(request.data)
        bot_obj = Bot.objects.filter(organization_id=request.data['organization_id'])
        queryset = bot_obj
        serializer = BotSerializer(queryset, many=True)
        res = {"bots": serializer.data}
        return response.Response(res)
