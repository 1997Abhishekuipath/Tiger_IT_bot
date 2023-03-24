from django.apps import AppConfig


class WebbotConfig(AppConfig):
    name = 'webbot'

    def ready(self):
        from scheduler import scheduler
        scheduler.start()
