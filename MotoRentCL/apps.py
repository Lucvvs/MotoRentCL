from django.apps import AppConfig

class MotorentclConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MotoRentCL'

    def ready(self):
        import MotoRentCL.signals