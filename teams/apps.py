from django.apps import AppConfig


class TeamsConfig(AppConfig):
    name = 'teams'

    def ready(self):
        import teams.signals
