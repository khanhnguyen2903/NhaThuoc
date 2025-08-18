from django.shortcuts import render, redirect
from NhaThuoc.firebase import *
from firebase_admin import db

# Danh sách loại thuốc
medicine_types = [
  "Giảm đau, hạ sốt",
  "Kháng sinh",
  "Chống dị ứng",
  "Thuốc dạ dày",
  "Vitamin bổ sung",
  "Thuốc tim mạch",
  "Thuốc huyết áp",
  "KH"
]

def display_product(request):
  # Tham chiếu đến nút 'products' trong Realtime Database
  ref = db.reference('products')
  snapshot = ref.get()

  # Chuyển dữ liệu về dạng list các dicts có id
  products = []
  if snapshot:
    for key, value in snapshot.items():
      product = value
      product['id'] = key  # Thêm key Firebase vào để tiện xử lý nếu cần
      products.append(product)

  return render(request, 'products/display_product.html', {'products': products})

def add_product(request):
  message = None
  # Lấy danh sách các danh mục sản phẩm
  categories_ref = db.reference('categories')
  categories_data = categories_ref.get() or {}
  categories = [
    {'id': key, 'name': value.get('name', 'Unknown')}
    for key, value in categories_data.items()
  ]
  
  if request.method == 'POST':
    name = request.POST.get('name')
    medicine_type = request.POST.get('medicine_type')
    quantity = int(request.POST.get('quantity'))
    dvt = request.POST.get('dvt')
    import_price = float(request.POST.get('import_price'))
    sale_price = float(request.POST.get('sale_price'))

    data = {
      'name': name,
      'medicine_type': medicine_type,
      'quantity': quantity,
      'dvt': dvt,
      'import_price': import_price,
      'sale_price': sale_price
    }

    # Lưu vào Realtime Database
    ref = db.reference('products')
    ref.push(data)

    message = "Đã lưu sản phẩm thành công!"

  return render(request, 'products/add_product.html', {'message': message, 'categories': categories})

def edit_product(request, product_id):
  ref = db.reference(f'products/{product_id}')
  product = ref.get()

  product['id'] = product_id
  type = product['medicine_type']
  # Lấy danh sách các danh mục sản phẩm
  categories_ref = db.reference('categories')
  categories_data = categories_ref.get() or {}
  categories = [
    {'id': key, 'name': value.get('name', 'Unknown')}
    for key, value in categories_data.items()
  ] 
  
  return render(request, 'products/edit_product.html', {'product': product, 'categories': categories, 'type': type})

def update_product(request, product_id):
  ref = db.reference(f'products/{product_id}')
  
  if request.method == 'POST':
    updated_data = {
      'name': request.POST['name'],
      'medicine_type': request.POST['medicine_type'],
      'quantity': int(request.POST['quantity']),
      'dvt': request.POST['dvt'],
      'import_price': float(request.POST['import_price']),
      'sale_price': float(request.POST['sale_price']),
    }
    ref.update(updated_data)
    return redirect('display_product') 
  return redirect('display_product')

def delete_product(request, product_id):
  if request.method == 'POST':
    ref = db.reference(f'products/{product_id}')
    ref.delete()
    return redirect('display_product')  # Chuyển về trang danh sách sản phẩm

  # Nếu không phải POST, có thể cho về lại danh sách
  return redirect('display_product')