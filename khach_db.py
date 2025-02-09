import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ✅ Chỉ khai báo 1 lần, KHÔNG truyền `app` vào đây ban đầu

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///khach.db"
    app.config["SECRET_KEY"] = "your_secret_key"

    db.init_app(app)  # ✅ Khởi tạo SQLAlchemy với Flask app

    return app