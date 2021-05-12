from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    words = ['дурак', 'сука']
    for word in words:
        if word in value:
            value = value.replace(word, '***')
    return str(value)
