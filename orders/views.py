# orders/views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from firebase_config import firebase_db  # Import Firebase config
from datetime import datetime
from django.utils.dateparse import parse_datetime
import json

def add_order(request):
    # Truy vấn sản phẩm từ Firebase
    products_ref = firebase_db.reference('products')
    products_data = products_ref.get() or {}

    # Chuyển sản phẩm sang dạng list
    products = []
    for key, value in products_data.items():
        value['id'] = key
        products.append(value)

    if request.method == 'POST':
        print('Lưu đơn hàng...')
        try:
            # Lấy dữ liệu từ POST request
            cart_data = json.loads(request.POST.get('cart', '[]'))
            id_customer = request.POST.get('id_customer')
            print(id_customer)
            if not id_customer or not cart_data:
                return render(request, 'orders/add_order.html', {
                    'products': products,
                    'error': 'Vui lòng nhập mã khách hàng và đảm bảo giỏ hàng không trống.'
                })

            # Tính tổng tiền đơn hàng
            total_order_amount = sum(item['total_item'] for item in cart_data)

            # Tạo dữ liệu đơn hàng
            order_data = {
                'id_customer': id_customer,
                'items': cart_data,
                'total_amount': total_order_amount,
                'created_at': timezone.now().isoformat(),
                'status': 'completed'  # Trạng thái mặc định
            }

            # Kiểm tra và cập nhật số lượng tồn kho
            for item in cart_data:
                product_name = item['name']
                ordered_quantity = item['quantity']

                # Tìm sản phẩm trong Firebase
                product = next((p for p in products if p['name'] == product_name), None)
                if not product:
                    return render(request, 'orders/add_order.html', {
                        'products': products,
                        'error': f'Sản phẩm {product_name} không tồn tại.'
                    })

                # Kiểm tra số lượng tồn kho
                current_quantity = int(product.get('quantity', 0))
                if ordered_quantity > current_quantity:
                    return render(request, 'orders/add_order.html', {
                        'products': products,
                        'error': f'Số lượng tồn kho của {product_name} không đủ (còn {current_quantity}).'
                    })

                # Cập nhật số lượng tồn kho
                updated_quantity = current_quantity - ordered_quantity
                products_ref.child(product['id']).update({'quantity': updated_quantity})

            # Lưu đơn hàng vào Firebase
            orders_ref = firebase_db.reference('orders')
            new_order_ref = orders_ref.push(order_data)

            # Xóa giỏ hàng sau khi lưu đơn hàng (tùy thuộc vào yêu cầu)
            # Nếu giỏ hàng được lưu ở client-side (localStorage), bạn có thể yêu cầu client xóa thông qua JavaScript.

            return redirect('list_orders')

        except json.JSONDecodeError:
            return render(request, 'orders/add_order.html', {
                'products': products,
                'error': 'Dữ liệu giỏ hàng không hợp lệ.'
            })
        except Exception as e:
            return render(request, 'orders/add_order.html', {
                'products': products,
                'error': f'Đã xảy ra lỗi: {str(e)}'
            })

    return render(request, 'orders/add_order.html', {'products': products})

def list_orders(request):
    try:
        # Fetch all orders from the 'orders' node in Realtime Database
        ref = firebase_db.reference('orders')
        orders_data = ref.get()
        
        orders = []
        if orders_data:
            for order_id, order_info in orders_data.items():
                # Process items in the order
                items = []
                if 'items' in order_info and isinstance(order_info['items'], list):
                    for item_data in order_info['items']:
                        items.append({
                            'name': item_data.get('name', 'Unknown'),
                            'type': item_data.get('type', 'Unknown'),
                            'price': float(item_data.get('price', 0)),
                            'quantity': int(item_data.get('quantity', 0)),
                            'dvt': item_data.get('dvt', 'Unknown'),
                            'total_item': float(item_data.get('total_item', 0))
                        })
                
                # Process order details
                order = {
                    'id': order_id,
                    'id_customer': order_info.get('id_customer', 'Unknown'),
                    'items': items,
                    'total_amount': float(order_info.get('total_amount', 0)),
                    'created_at': datetime.fromisoformat(order_info.get('created_at', '1970-01-01T00:00:00')),
                    'status': order_info.get('status', 'pending')
                }
                orders.append(order)
        
        # Sort orders by created_at (newest first)
        orders.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Render the template with orders data
        return render(request, 'orders/list_orders.html', {'orders': orders})
    
    except Exception as e:
        # Handle errors (e.g., database connection issues)
        print(f"Error fetching orders: {str(e)}")
        return render(request, 'orders/list_orders.html', {'orders': [], 'error': 'Không thể tải danh sách đơn hàng'})
