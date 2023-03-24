"""teams_integration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from webbot.views.views_webbot import WebbotWebhook

urlpatterns = [
    path('bot/', WebbotWebhook.as_view()),
    path('bot/load_test', WebbotWebhook.rasa_load_test),
    path('bot/user_info', WebbotWebhook.user_info),
    path('bot/submit_form', WebbotWebhook.submit_form),
]
