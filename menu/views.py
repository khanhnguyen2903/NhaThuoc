from django.shortcuts import render
from firebase_config import firebase_db

def list_menu(request):
    ref = firebase_db.reference('products')
    product_data = ref.get()
    products = []

    if product_data:
        for key, value in product_data.items():
            product = value
            product['id'] = key 
            products.append(product)

    return render(request, 'menu/list_menu.html', {'products': products})