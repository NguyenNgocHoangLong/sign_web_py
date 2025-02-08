import sqlite3
import os

db_path = "Khach.db"

if os.path.exists(db_path):
    print(f"✅ Database '{db_path}' tồn tại.")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        print("📌 Các bảng trong database:", tables)
    else:
        print("⚠️ Database chưa có bảng nào.")
    conn.close()
else:
    print(f"❌ Database '{db_path}' không tồn tại.")
