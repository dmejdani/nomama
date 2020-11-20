from app import create_app, db, bcrypt
from app.models import User, Receipt, Item

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    username = input("Enter username: ")
    password = input("Enter password: ")
    password = bcrypt.generate_password_hash(password)
    admin = User(username=username, password=password)
    db.session.add(admin)
    db.session.commit()
