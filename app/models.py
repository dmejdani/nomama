from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, date


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    shop = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    payer = db.Column(db.String(10), nullable=True)
    location = db.Column(db.String(40), nullable=True)
    posts = db.relationship("Item", backref="receipt", lazy=True)

    def __repr__(self):
        return f"Receipt({self.date}, {self.shop}, {self.cost})"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(30), nullable=True)
    category = db.Column(db.String(30), nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey(
        'receipt.id'), nullable=False)

    def __repr__(self):
        return f"Item({self.name}, {self.price}, receipt={self.receipt_id})"
