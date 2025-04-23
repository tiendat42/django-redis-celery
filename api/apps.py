from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        import json

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=10, period="seconds"
        )

        PeriodicTask.objects.update_or_create(
            name="Say Hello Task",
            defaults={
                "interval": schedule,
                "task": "api.tasks.cron_task",
                "args": json.dumps([]),
            }
        )
