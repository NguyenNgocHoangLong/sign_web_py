from app import app, db, Khach  # Import đúng model

with app.app_context():
    khach_list = Khach.query.all()
    for khach in khach_list:
        print(f"ID: {khach.id}, Name: {khach.Khach_Name}, Position: {khach.Position}, Email: {khach.Email}, Sign: {khach.Sign}")
