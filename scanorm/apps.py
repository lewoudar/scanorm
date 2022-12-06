from django.apps import AppConfig

from .inspector import create_model_schema


class ScanormConfig(AppConfig):
    name = 'scanorm'

    def ready(self):
        create_model_schema()
