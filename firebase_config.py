import firebase_admin
from firebase_admin import credentials, db

# Khởi tạo Firebase app nếu chưa khởi tạo
if not firebase_admin._apps:
  cred = credentials.Certificate('firebase_key.json')
  firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nha-thuoc-ede91-default-rtdb.firebaseio.com/'
  })

# Truy cập database
firebase_db = db
