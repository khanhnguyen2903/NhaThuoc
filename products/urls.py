from django.urls import path
from .views import add_product, display_product, edit_product, delete_product, update_product

urlpatterns = [
  path('products/add/', add_product, name='add_product'),
  path('products/', display_product, name='display_product'),
  path('products/edit/<str:product_id>/', edit_product, name='edit_product'),
  path('products/delete/<str:product_id>/', delete_product, name='delete_product'),
  path('products/update/<str:product_id>/', update_product, name='update_product'),
]
