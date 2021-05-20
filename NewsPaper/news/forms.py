from django.forms import ModelForm, BooleanField
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Подтверждение')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'category', 'type_post', 'check_box']