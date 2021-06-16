from django import template
from news.models import Post

register = template.Library()


@register.filter(name='censor')
def censor(value):
    words = ['дурак', 'сука']
    for word in words:
        if word in value:
            value = value.replace(word, '***')
    return str(value)


@register.simple_tag(name='param_replace', takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag(name='is_not_author', takes_context=True)
def is_not_author(context):
    request = context["request"]
    is_not_author = not request.user.groups.filter(name='authors').exists()
    return is_not_author
