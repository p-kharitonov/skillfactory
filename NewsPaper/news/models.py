from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = Post.objects.filter(author=self.id)
        rating_posts = sum([int(post.rating) for post in posts]) * 3
        rating_comments = sum([int(comment.rating) for comment in Comment.objects.filter(user=self.id)])
        rating_comments_posts = sum([int(comment.rating) for post in posts for comment in Comment.objects.filter(post=post.id)])
        self.rating = sum([rating_posts, rating_comments, rating_comments_posts])
        self.save()
        return self.rating


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NS'
    POST_CHOICES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2, choices=POST_CHOICES,
                                 default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(str(self.content)) > 124:
            return ''.join((self.content[:124], '...'))

    def __str__(self):
        return f'{self.title}: {self.preview()}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
