from django_filters import FilterSet
from django.forms import DateInput
import django_filters


class PostFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    author = django_filters.CharFilter(field_name='author_id__user_id__username', lookup_expr='icontains', label='Автор')
    datetime = django_filters.DateFilter(field_name='created_at', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt', label='Позже даты')

