import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category
from datetime import datetime, timedelta
from django.core.mail import send_mail

logger = logging.getLogger(__name__)



def send_weekly_email():
    week_ago = datetime.today() - timedelta(weeks=1)
    new_posts = Post.objects.filter(publication_date__gt=week_ago)

    for tag in Category.objects.all():
        for user in tag.subscribers.all():
            posts_tagged = new_posts.filter(category=tag.pk)
            if posts_tagged is not None and user.email != '':
                text = f"Hi, {user.username}. Your weekly dose of content in category {tag.tag.lower()}! " \
                        f"\nHere's a list of what you might've missed: \n\n"
                for post in posts_tagged:
                    text += f"{post.title}\nhttp://127.0.0.1:8000/news/{post.pk}\n\n"
                text += "NewsPaper - 99% news, 1% masterpiece, 0% paper"

                send_mail(
                    subject=f"Weekly update from NewsPaper on {tag.tag}",
                    message=text,
                    from_email='biorival@yandex.ru',
                    recipient_list=[user.email],
                    fail_silently=False,
                )



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_email,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="send_weekly_email",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_email'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
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