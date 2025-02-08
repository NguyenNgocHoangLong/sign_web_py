import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import fitz  # PyMuPDF

app = Flask(__name__)

# Thư mục lưu tệp tạm thời
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "pdf" not in request.files or "signature" not in request.files:
        return "Vui lòng tải lên cả PDF và ảnh chữ ký!", 400

    # Nhận file từ form
    pdf_file = request.files["pdf"]
    sig_file = request.files["signature"]

    if pdf_file.filename == "" or sig_file.filename == "":
        return "Tên tệp không hợp lệ!", 400

    # Lưu tệp vào thư mục tạm
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(pdf_file.filename))
    sig_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(sig_file.filename))
    pdf_file.save(pdf_path)
    sig_file.save(sig_path)

    # Gọi hàm chèn chữ ký vào PDF
    output_pdf = os.path.join(app.config["UPLOAD_FOLDER"], "signed_" + pdf_file.filename)
    add_signature_to_pdf(pdf_path, sig_path, output_pdf)

    return send_file(output_pdf, as_attachment=True)


def add_signature_to_pdf(pdf_path, sig_path, output_pdf, position=(100, 100), page_number=0):
    """
    Chèn ảnh chữ ký vào PDF và điều chỉnh kích thước tương đương chữ viết hoa size 24 (~34px).
    """
    doc = fitz.open(pdf_path)
    page = doc[page_number]  # Lấy trang cần đặt chữ ký

    # Lấy kích thước trang PDF
    page_width = page.rect.width
    page_height = page.rect.height

    # Mở ảnh chữ ký
    sig_img = Image.open(sig_path)
    sig_width, sig_height = sig_img.size

    # Điều chỉnh kích thước chữ ký (Chiều cao chuẩn hóa về 34 px)
    target_height = 34
    scale_factor = target_height / sig_height
    new_width = int(sig_width * scale_factor)
    new_height = target_height
    sig_img = sig_img.resize((new_width, new_height), Image.LANCZOS)

    # Lưu ảnh đã chỉnh sửa
    resized_sig_path = os.path.join(app.config["UPLOAD_FOLDER"], "resized_signature.png")
    sig_img.save(resized_sig_path)

    # Xác định vị trí chèn ảnh vào PDF
    img_rect = fitz.Rect(position[0], position[1], position[0] + new_width, position[1] + new_height)
    page.insert_image(img_rect, filename=resized_sig_path)

    # Lưu PDF mới có chữ ký
    doc.save(output_pdf)
    doc.close()

if __name__ == "__main__":
    app.run(debug=True)
