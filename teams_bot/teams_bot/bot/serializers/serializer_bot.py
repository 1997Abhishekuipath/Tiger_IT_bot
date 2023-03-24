from rest_framework import serializers
from bot.models.model_bot import Bot
from organization.models.model_organization import Organization
from bot.models.model_nlp_agent import Agent


class BotSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all()
    )
    nlp_agent = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all()
    )

    class Meta:
        model = Bot
        fields = [
            'id',
            'name',
            'organization_id',
            'nlp_agent',
        ]
