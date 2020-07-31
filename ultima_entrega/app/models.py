from .extensions import db
from sqlalchemy.orm import relationship, backref
import enum


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    telephone = db.Column(db.String(14))
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False)

    def json(self):
        user__json = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "admin": self.admin,
        }
        return user__json


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10,2), default=0)
    stock = db.Column(db.Integer, default=0)

    def json(self):
        product__json = {
            "id": self.id,
            "name": self.name,
            "price": str(self.price),
            "stock": self.stock,
        }
        return product__json


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer = relationship("User", backref=backref("orders", cascade="all, delete"))
    product_id =  db.Column(db.Integer, db.ForeignKey('products.id'))
    product = relationship("Product", backref=backref("product_orders", cascade="all, delete"))
    amount = db.Column(db.Integer, default=1, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(18), nullable=False)

    def json(self):
        post__json = {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "amount": self.amount,
            "address": self.address,
            "date": self.date,
        }
        return post__json
