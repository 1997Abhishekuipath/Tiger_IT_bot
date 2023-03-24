from django.contrib import admin
from bot.models.model_bot import Agent, Bot
from bot.models.model_intents import Intent
from bot.models.model_web_bot import WebBot


class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'config',
        'type'
    ]


admin.site.register(Agent, AgentAdmin)


class IntentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'response',
        'webhook',
        'bot_id',
    ]


admin.site.register(Intent, IntentAdmin)


class BotAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'organization_id',
        'nlp_agent',
        'web_uid'
    ]


admin.site.register(Bot, BotAdmin)


class WebBotAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'bot_id',
        'web_uid',
    ]


admin.site.register(WebBot, WebBotAdmin)
