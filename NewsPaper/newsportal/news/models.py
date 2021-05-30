from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        posts = Post.objects.filter(author=self.id)
        rating_posts = sum([int(post.rating) for post in posts]) * 3
        rating_comments = sum([int(comment.rating) for comment in Comment.objects.filter(user=self.id)])
        rating_comments_posts = sum([int(comment.rating) for post in posts for comment in Comment.objects.filter(post=post.id)])
        self.rating = sum([rating_posts, rating_comments, rating_comments_posts])
        self.save()
        return self.rating

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True, verbose_name='Категория')

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NS'
    POST_CHOICES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Имя автора')
    type_post = models.CharField(max_length=2, choices=POST_CHOICES,
                                 default=ARTICLE, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Новость')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def preview(self):
        if len(str(self.content)) > 124:
            return ''.join((self.content[:124], '...'))
        else:
            return str(self.content)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
