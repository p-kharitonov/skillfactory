from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view()),
    path('search/', PostSearch.as_view()),
    path('add/', PostCreate.as_view()),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>', PostDetail.as_view()),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
]