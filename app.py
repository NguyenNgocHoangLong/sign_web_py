import os
from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
from PIL import Image
import fitz  # PyMuPDF
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from forms import RegisterForm
from models import db, Khach
from config import Config  # ✅ Thêm dòng này vào

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///khach.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"  # ✅ Định nghĩa trước khi sử dụng

# Khởi tạo database
db.init_app(app)
# Tạo thư mục nếu chưa có
import os
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

with app.app_context():
    db.create_all()  # ✅ Đảm bảo bảng được tạo trước khi truy vấn

db = SQLAlchemy()  # ✅ Không import models trước khi tạo app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # ✅ Khởi tạo SQLAlchemy với app

    with app.app_context():
        from models import Khach  # ✅ Import model bên trong app context
        db.create_all()

    return app

app = create_app()  # ✅ Tạo app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Khach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# Mô hình User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Form đăng ký
class RegisterForm(FlaskForm):
    username = StringField("Tên đăng nhập", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mật khẩu", validators=[DataRequired()])
    confirm_password = PasswordField("Xác nhận mật khẩu", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Đăng ký")

# Form đăng nhập
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mật khẩu", validators=[DataRequired()])
    submit = SubmitField("Đăng nhập")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("index.html")  # Nếu đã đăng nhập, vào trang chính
    return redirect(url_for("login"))  # Nếu chưa đăng nhập, chuyển đến trang login

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        khach = Khach.query.filter_by(email=form.email.data).first()  # Đổi Email -> email
        if khach and check_password_hash(khach.password, form.password.data):  # Đổi Password -> password
            login_user(khach)
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("home"))  # Chuyển hướng đến trang chính
        else:
            flash("Sai email hoặc mật khẩu", "danger")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))  # Sau khi logout, quay lại trang login


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if "pdf" not in request.files or "signature" not in request.files:
            flash("Vui lòng tải lên cả PDF và ảnh chữ ký!", "danger")
            return redirect(url_for("upload"))

        pdf_file = request.files["pdf"]
        sig_file = request.files["signature"]

        if pdf_file.filename == "" or sig_file.filename == "":
            flash("Tên tệp không hợp lệ!", "danger")
            return redirect(url_for("upload"))

        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(pdf_file.filename))
        sig_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(sig_file.filename))
        pdf_file.save(pdf_path)
        sig_file.save(sig_path)

        output_pdf = os.path.join(app.config["UPLOAD_FOLDER"], "signed_" + pdf_file.filename)
        add_signature_to_pdf(pdf_path, sig_path, output_pdf)

        return send_file(output_pdf, as_attachment=True)
    
    return render_template("upload.html")

def add_signature_to_pdf(pdf_path, sig_path, output_pdf, position=(80, 450), page_number=0):
    doc = fitz.open(pdf_path)
    page = doc[page_number]
    sig_img = Image.open(sig_path)
    sig_width, sig_height = sig_img.size
    target_height = 34
    scale_factor = target_height / sig_height
    new_width = int(sig_width * scale_factor)
    new_height = target_height
    sig_img = sig_img.resize((new_width, new_height), Image.LANCZOS)
    resized_sig_path = os.path.join(app.config["UPLOAD_FOLDER"], "resized_signature.png")
    sig_img.save(resized_sig_path)
    img_rect = fitz.Rect(position[0], position[1], position[0] + new_width, position[1] + new_height)
    page.insert_image(img_rect, filename=resized_sig_path)
    doc.save(output_pdf)
    doc.close()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
