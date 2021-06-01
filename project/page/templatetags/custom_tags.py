from django import template
from page.models import Category, Page

register = template.Library()


@register.simple_tag()
def get_categories():
    all_categories = Category.objects.all()
    return all_categories


@register.simple_tag()
def get_pages(category_id):
    category = Category.objects.get(pk=category_id)
    pages = Page.objects.filter(category=category)
    print(pages)
    return pages