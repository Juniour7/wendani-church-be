from django.apps import AppConfig


class ChurchAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'church_app'

    def ready(self):
        import church_app.signals

