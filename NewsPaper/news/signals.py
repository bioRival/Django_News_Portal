from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, PostCategory


@receiver(post_save, sender=Post)
def send_email_to_subscribers(sender, instance, created, **kwargs):
    pass

@receiver(m2m_changed, sender=PostCategory)
def send_email_to_subs(sender, instance, action, **kwargs):
    if action == "post_add":
        tags = list(instance.category.all())
        sent_emails = [] # keeping track of emails to which message has been already sent to avoid duplication
        for tag in tags:
            for user in tag.subscribers.all():
                if user.email not in sent_emails and user.email != '':
                    sent_emails.append(user.email)

                    send_mail(
                        subject=instance.title,
                        message = f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе {tag.tag}! " \
                              f"\n{instance.content[:50]}... \n" \
                              f"See the whole content: http://127.0.0.1:8000/news/{instance.pk}",
                        from_email='biorival@yandex.ru',
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
