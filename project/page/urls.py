from django.urls import path
from .views import *

urlpatterns = [
    path('', PageListView.as_view(), name='pages'),
    path('<int:pk>', PageDetailView.as_view(), name='page1'),
]