from django.apps import AppConfig


class HostelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hostel'
    
    def ready(self):
        from .scheduler import schedule_tasks
        schedule_tasks()

