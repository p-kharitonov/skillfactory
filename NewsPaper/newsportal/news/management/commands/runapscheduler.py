import logging

from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Category, Post


logger = logging.getLogger(__name__)


def weekly_mailing():
    for category in Category.objects.all():
        subject = f'Последнии статьи за неделю в категории {category}'
        end_date = datetime.now()
        start_date = end_date - timedelta(days=8)
        posts = Post.objects.filter(category=category, created_at__range=(start_date, end_date))
        if posts.exists():
            for subscriber in category.subscribers.all():
                html_content = render_to_string(
                    'news/weekly_mailing.html',
                    {
                        'username': subscriber,
                        'posts': posts,
                        'category': category,
                        'site': settings.BASE_URL,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=subject,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_mailing,
            trigger=CronTrigger(
                day_of_week="wed", hour="15", minute="34"
            ),
            id="weekly_mailing",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_mailing'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")