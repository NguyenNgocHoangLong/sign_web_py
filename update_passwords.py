from app import create_app, db
from models import Khach
from werkzeug.security import generate_password_hash

app = create_app()  # ✅ Dùng create_app để tránh lỗi nhiều instance
with app.app_context():
    khach_list = Khach.query.all()
    
    for khach in khach_list:
        hashed_password = generate_password_hash(khach.Password)
        khach.Password = hashed_password  # ✅ Cập nhật mật khẩu đã mã hóa
        print(f"🔹 Đã mã hóa mật khẩu cho: {khach.Email}")

    db.session.commit()
    print("✅ Cập nhật xong tất cả mật khẩu trong database!")
