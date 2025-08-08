from django.urls import path
from . import views

urlpatterns = [
    path('list-category/', views.list_category, name='list_category'),
    path('create-category/', views.create_category, name='create_category'),
    path('delete-category/<str:category_id>/', views.delete_category, name='delete_category'),
]
