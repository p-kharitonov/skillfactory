import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.weekly_mailing',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
app.autodiscover_tasks()
