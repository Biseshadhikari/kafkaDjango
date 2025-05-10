from django.apps import AppConfig

class LocationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .kafka_consumer import start_consumer_thread
        start_consumer_thread()
