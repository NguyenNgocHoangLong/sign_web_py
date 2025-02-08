import sqlite3

# Kết nối hoặc tạo database SQLite
conn = sqlite3.connect("Khach.db")
cursor = conn.cursor()

# Tạo bảng Khach nếu chưa tồn tại
cursor.execute("""
CREATE TABLE IF NOT EXISTS Khach (
    KhachID INTEGER PRIMARY KEY AUTOINCREMENT,
    Khach_Name TEXT NOT NULL,
    Position TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Sign TEXT NOT NULL,
    Password TEXT NOT NULL
)
""")

# Danh sách dữ liệu khách hàng mẫu
khach_list = [
    ("nhanvien1", "staff", "nhanvien1@gmail.com", "NV1.jpg", "nv123"),
    ("manager1", "manager", "manager1@gmail.com", "MGR1.jpg", "mgr123"),
    ("director1", "director", "director1@gmail.com", "DIR.jpg", "dir123"),
    ("evgm1", "evgm", "evgm1@gmail.com", "EVGM1.jpg", "evgm123"),
]

# Chèn dữ liệu mẫu nếu chưa có
for khach in khach_list:
    try:
        cursor.execute("INSERT INTO Khach (Khach_Name, Position, Email, Sign, Password) VALUES (?, ?, ?, ?, ?)", khach)
    except sqlite3.IntegrityError:
        pass  # Tránh chèn trùng dữ liệu nếu đã tồn tại

conn.commit()  # Lưu thay đổi
conn.close()  # Đóng kết nối
