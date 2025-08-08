# orders/urls.py
from django.urls import path
from .views import add_order, list_orders

urlpatterns = [
    path('add-order/', add_order, name='add_order'),
    path('list-orders/', list_orders, name='list_orders'),
]
