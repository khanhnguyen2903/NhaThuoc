from django.shortcuts import render, redirect
from django.http import JsonResponse
from firebase_config import firebase_db
from datetime import datetime

def list_category(request):
    # Truy cập đến nút "categories" trong Firebase
    ref = firebase_db.reference('categories')
    data = ref.get()

    # Chuyển dữ liệu về dạng danh sách để hiển thị
    category_list = []
    if data:
        for key, value in data.items():
            created_raw = value.get('created_at', '')
            try:
                created_at = datetime.fromisoformat(created_raw)
            except:
                created_at = None

            category_list.append({
                'id': key,
                'name': value.get('name', ''),
                'created_at': created_at
            })

    return render(request, 'categories/list_category.html', {'categories': category_list})

def create_category(request):
    message = None
    error = None

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            error = 'Tên danh mục không được để trống'
        else:
            # Lấy danh sách danh mục hiện có từ Firebase
            ref = firebase_db.reference('categories')
            existing_categories = ref.get()

            # Kiểm tra tên đã tồn tại (không phân biệt hoa thường)
            is_duplicate = False
            if existing_categories:
                for item in existing_categories.values():
                    existing_name = item.get('name', '').strip().lower()
                    if existing_name == name.lower():
                        is_duplicate = True
                        break

            if is_duplicate:
                error = 'Danh mục sản phẩm đã tồn tại'
            else:
                # Nếu không trùng thì thêm mới
                new_category = {
                    'name': name,
                    'created_at': datetime.now().isoformat()
                }
                ref.push(new_category)
                message = 'Đã lưu danh mục thành công'
                return redirect('list_category')

    return render(request, 'categories/create_category.html', {
        'message': message,
        'error': error,
        'name': request.POST.get('name', '') if request.method == 'POST' else ''
    })


def delete_category(request, category_id):
    ref = firebase_db.reference(f'categories/{category_id}')
    category = ref.get()

    if not category:
        return JsonResponse({'status': 'error', 'message': 'Danh mục không tồn tại'}, status=404)

    if request.method == 'GET':
        ref.delete()
        return redirect('list_category')

    return redirect('list_category')
