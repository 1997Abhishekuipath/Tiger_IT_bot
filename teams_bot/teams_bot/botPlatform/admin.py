from django.contrib import admin
from botPlatform.models.model_botuser import Platform, BotUserInfo


class BotUserInfoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'platform_id',
        'info',
        'created_at',
        'updated_at',
    ]


admin.site.register(BotUserInfo, BotUserInfoAdmin)


class PlatformAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'bot_id',
        'config',
        'created_at',
        'updated_at',
    ]


admin.site.register(Platform, PlatformAdmin)
