import sqlite3

DB_PATH = "khach.db"

def get_signature_by_email(email):
    """Lấy đường dẫn file chữ ký từ email"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT Sign FROM Khach WHERE Email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"static/signatures/{row[0]}"  # Đường dẫn đến ảnh chữ ký
    return None
