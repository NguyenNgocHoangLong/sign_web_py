import pymupdf as fitz
import os
from datetime import datetime
from config import Config
from models import Khach

def get_signature_by_email(email):
    khach = Khach.query.filter_by(Email=email).first()
    if khach:
        return khach.Sign
    return None

def add_signature_to_pdf(pdf_path, signature_path, position):
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Xác định vị trí chữ ký theo chức vụ
    pos_dict = {
        "staff": (100, 700),
        "manager": (100, 650),
        "director": (400, 700),
        "evgm": (400, 650)
    }
    
    x, y = pos_dict.get(position, (100, 750))  # Mặc định nếu không xác định

    rect = fitz.Rect(x, y, x + 150, y + 50)
    page.insert_image(rect, filename=signature_path)

    # Thêm ngày giờ dưới chữ ký nếu cấp cao
    if position in ["director", "evgm"]:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        page.insert_text((x, y + 60), f"Signed on: {current_time}", fontsize=10, color=(0, 0, 0))

    signed_pdf_path = os.path.join(Config.SIGNED_PDF_FOLDER, "signed_" + os.path.basename(pdf_path))
    doc.save(signed_pdf_path)
    doc.close()
    
    return signed_pdf_path
