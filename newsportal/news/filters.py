from django_filters import FilterSet, CharFilter, DateFilter
from django.forms import DateInput


class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    author = CharFilter(field_name='author_id__user_id__username', lookup_expr='icontains', label='Автор')
    datetime = DateFilter(field_name='created_at', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt', label='Позже даты')
