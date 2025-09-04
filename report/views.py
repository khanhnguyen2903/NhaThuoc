from django.shortcuts import render
from collections import defaultdict
from datetime import datetime
from NhaThuoc.firebase import *
from firebase_admin import db

def report(request):
    ref = db.reference("orders")
    orders = ref.get() or {}

    monthly_revenue = defaultdict(float)

    for key, order in orders.items():
        amount = order.get("total_amount", 0)
        created_at = order.get("created_at")  # giả sử dạng ISO string hoặc timestamp

        try:
            # Nếu là timestamp (số), chuyển đổi sang datetime
            if isinstance(created_at, (int, float)):
                date = datetime.fromtimestamp(created_at)
            else:
                # Nếu là ISO string
                date = datetime.fromisoformat(created_at)
        except Exception:
            continue

        month = f"{date.month:02d}/{date.year}"
        monthly_revenue[month] += float(amount)

    # Sắp xếp theo thời gian
    labels = sorted(monthly_revenue.keys(), key=lambda x: datetime.strptime(x, "%m/%Y"))
    values = [monthly_revenue[m] for m in labels]

    context = {
        "labels": labels,
        "values": values
    }
    return render(request, "report/report.html", context)
