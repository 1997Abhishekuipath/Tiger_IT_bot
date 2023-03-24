from django.contrib import admin

from botData.models.model_bot_ratings import BotRating
from botData.models.model_entities import Entity
from botData.models.model_fallbacks import Message, FallbackMessage
from botData.models.model_feedback_form import FeedbackForm


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'bot_id',
        'user_id',
        'message',
        'created_at',
        'updated_at',
    ]


admin.site.register(Message, MessageAdmin)


class FeedbackFormAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'message_id',
        'user_id',
        'user_message',
        'bot_id',
    ]


admin.site.register(FeedbackForm, FeedbackFormAdmin)


class FallbackMessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'message_id',
        'user_id',
        'bot_id',
        'created_at',
        'updated_at',
    ]


admin.site.register(FallbackMessage, FallbackMessageAdmin)


class EntityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'entity_key',
        'entity_value',
        'entity_synonyms',
    ]


admin.site.register(Entity, EntityAdmin)


class BotRatingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user_id',
        'rating',
        'bot_id',
    ]


admin.site.register(BotRating, BotRatingAdmin)
