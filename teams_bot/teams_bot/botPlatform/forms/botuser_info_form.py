from django import forms
from botPlatform.models.model_botuser import BotUserInfo


class BotUserInfoForm(forms.ModelForm):
        class Meta:
            model = BotUserInfo
            fields = ["name", "platform_id", "email", "info" ]