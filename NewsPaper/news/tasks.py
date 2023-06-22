from celery import shared_task
from news.models import Post, Category
from datetime import datetime, timedelta
from django.core.mail import send_mail

@shared_task
def send_email_weekly():
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
    print("WEEKLY EMAILS HAVE BEEN SENT!")