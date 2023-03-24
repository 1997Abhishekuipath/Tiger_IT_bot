from rest_framework import serializers
from bot.models.model_nlp_agent import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = [
            'id',
            'name',
            'config',
            'is_active',
        ]
