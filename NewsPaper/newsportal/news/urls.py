from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='news'),
    path('<int:pk>', PostDetailView.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
]