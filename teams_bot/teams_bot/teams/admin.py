from django.contrib import admin
from bot.models.model_nlp_agent import Agent
from teams.models.teams_config import TeamsConfig
from teams.models.intents import Intent
from teams.models.user_info import UserInfo
from teams.models.conversation_parameters import ConversationParameters
from teams.models.entities import EntitiesParsing
from teams.models.user_feedback import UserFeedback


# class TeamsConfigAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'access_token',
#         'app_id',
#         'app_secret',
#     ]
#
#
# admin.site.register(TeamsConfig, TeamsConfigAdmin)


# class IntentAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'name',
#         'response',
#         'webhook',
#     ]
#
#
# admin.site.register(Intent, IntentAdmin)
#
#
# class UserInfoAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'name',
#         'teams_id',
#         'aad_id',
#         'email_address',
#     ]
#
#
# admin.site.register(UserInfo, UserInfoAdmin)
#
#
class ConversationParametersAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'conversation_id',
        'parameters',
        'time',
    ]


admin.site.register(ConversationParameters, ConversationParametersAdmin)
#
#
# class EntitiesParsingAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'entity_key',
#         'entity_value',
#         'entity_synonyms',
#     ]
#
#
# admin.site.register(EntitiesParsing, EntitiesParsingAdmin)
#
#
# class UserFeedbackAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'username',
#         'useremail',
#         'feedback',
#     ]
#
#
# admin.site.register(UserFeedback, UserFeedbackAdmin)
