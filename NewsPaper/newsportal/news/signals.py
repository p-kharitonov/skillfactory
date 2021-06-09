from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from allauth.account.signals import email_confirmed
from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def notify_users(sender, instance, **kwargs):
    action = kwargs['action']
    if action == 'post_add':
        categories = instance.category.all()
        for category in categories:
            subject = f'Новая статья в категории {category}'
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                html_content = render_to_string(
                    'news/mail_new_post_for_subscribers.html',
                    {
                        'username': subscriber,
                        'post': instance,
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


@receiver(email_confirmed)
def email_confirmed(request, email_address, **kwargs):
    html_content = render_to_string(
        'news/mail_registration_users.html',
        {
            'username': User.objects.get(email=email_address),
        }
    )
    msg = EmailMultiAlternatives(
        subject='Спасибо за регистрацию на сайте News Portal',
        from_email=settings.EMAIL_HOST_USER,
        to=[email_address],
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()

