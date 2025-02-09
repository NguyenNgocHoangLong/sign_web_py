from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ✅ Không import từ app.py để tránh vòng lặp

class Khach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Khach_Name = db.Column(db.String(100), nullable=False)
    Position = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(150), unique=True, nullable=False)
    Sign = db.Column(db.String(150), nullable=False)
    Password = db.Column(db.String(150), nullable=False)  # Cần mã hóa sau

    def __repr__(self):
        return f"<Khach {self.Khach_Name}>"
