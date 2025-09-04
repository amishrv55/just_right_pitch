# proposals/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings

class ProposalsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proposals"

    def ready(self):
        from .scheduler import start_scheduler

        def start_scheduler_once(*args, **kwargs):
            # In development, we check DEBUG to avoid duplicate schedulers on code reload
            if settings.DEBUG:
                start_scheduler()
            else:
                # In production, just start scheduler without this check
                start_scheduler()

        post_migrate.connect(start_scheduler_once, sender=self)
