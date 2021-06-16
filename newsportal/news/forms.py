from django.forms import ModelForm, BooleanField, Select, TextInput, Textarea, SelectMultiple, CheckboxInput
from .models import Post
from django.contrib.auth.models import Group
from django.dispatch import receiver
from allauth.account.forms import SignupForm
from allauth.account.signals import user_signed_up


class PostForm(ModelForm):
    check_box = BooleanField(label='Подтвердить')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'type_post', 'check_box']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Заголовок'}),
            'content': Textarea(attrs={'class': 'form-control mb-1', 'placeholder': 'Введите текст'}),
            'category': SelectMultiple(attrs={'class': 'form-control mb-1'}),
            'type_post': Select(attrs={'class': 'form-control mb-1'}),
            'check_box': CheckboxInput(attrs={'class': 'form-check-input btn mb-1'}),
        }


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    Group.objects.get(name='common').user_set.add(user)
    user.save()
