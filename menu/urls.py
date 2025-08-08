from django.urls import path
from .views import list_menu

urlpatterns = [
  path('', list_menu, name='list_menu'),
]