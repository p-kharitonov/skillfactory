from django.db import models
from django.contrib.auth.models import User, Group


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(verbose_name='Основной контент')
    content_additional = models.TextField(blank=True, null=True, verbose_name='Дополнительный контент')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, verbose_name='Имя автора')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    group = models.ManyToManyField(Group, blank=True, verbose_name='Группы')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/page/{self.pk}'

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
