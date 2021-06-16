from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category
from datetime import datetime, timedelta


@shared_task
def notify_users(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    for category in categories:
        subject = f'Новая статья в категории {category}'
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            html_content = render_to_string(
                'news/mail_new_post_for_subscribers.html',
                {
                    'username': subscriber,
                    'post': post,
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


@shared_task
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
