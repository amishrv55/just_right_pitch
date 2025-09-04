# proposals/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.core.management import call_command

scheduler = None

def run_daily_reminders():
    """Wrapper so APScheduler can pickle it properly"""
    call_command("send_daily_reminders")

def start_scheduler():
    global scheduler
    if scheduler and scheduler.running:
        return  # already started

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Daily reminders at 9 AM
    scheduler.add_job(
        run_daily_reminders,
        "cron",
        hour=9,
        minute=0,
        id="daily_reminders",
        replace_existing=True,
    )

    register_events(scheduler)
    scheduler.start()
    print("✅ APScheduler started for daily reminders")
