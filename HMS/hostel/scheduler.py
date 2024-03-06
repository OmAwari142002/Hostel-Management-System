from apscheduler.schedulers.background import BackgroundScheduler
from .views import mark_users_as_absent

def schedule_tasks():
    scheduler = BackgroundScheduler()
    # Schedule the mark_users_as_absent function to run every day at 23:45
    scheduler.add_job(mark_users_as_absent, 'cron', hour=23, minute=45)
    scheduler.start()
