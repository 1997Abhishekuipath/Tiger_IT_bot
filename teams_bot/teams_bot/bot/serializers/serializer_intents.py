from rest_framework import serializers
from bot.models.model_bot import Bot
from organization.models.model_organization import Organization
from bot.models.model_nlp_agent import Agent


class BotSerializer(serializers.ModelSerializer):
    bot_id = serializers.PrimaryKeyRelatedField(
        queryset=Bot.objects.all()
    )

    class Meta:
        model = Bot
        fields = [
            'id',
            'name',
            'bot_id',
            'webhook',
            'response',
        ]
