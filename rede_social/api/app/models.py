from .extensions import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import enum


class CategoryType(enum.Enum):
    ELECTRONICS = 'Eletrõnicos'
    TOYS = 'Brinquedos'
    GARDENING = 'Jardinagem'
    INSTRUMENTS = 'Instrumentos'
    PETS = 'Pets'
    CLOTHING = 'Vestuário'


postlike = db.Table('post likes', 
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('posts_id', db.Integer, db.ForeignKey('posts.id'))
)


commentlike = db.Table('comment likes',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('comments_id', db.Integer, db.ForeignKey('comments.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, default=0)
    activated = db.Column(db.Boolean, default=False)
    post_likes = relationship("Post", secondary=postlike, backref=backref("users", cascade="all, delete"))
    comment_likes = relationship("Comment", secondary=commentlike, backref=backref("users", cascade="all, delete"))

    def json(self):
        user__json = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
        }
        return user__json


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", backref=backref("posts", cascade="all, delete"))
    description = db.Column(db.String(280), nullable=False)
    products = relationship("Product", uselist=False, backref=backref("posts", cascade="all, delete"))

    def json(self):
        post__json = {
            "id": self.id,
            "description": self.description,
            "author_id": self.author_id,
        }
        return post__json


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = relationship('Post', backref=backref("products", cascade="all, delete"))
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10,2), default=0)
    discount = db.Column(db.Numeric(3,2), default=0)
    stock = db.Column(db.Integer, default=0)
    sold = db.Column(db.Integer, default=0)
    category = db.Column(db.Enum(CategoryType))

    def json(self):
        product__json = {
            "id": self.id,
            "post_id": self.post_id,
            "name": self.name,
            "price": self.price,
            "discount": self.discount,
            "stock": self.stock,
            "sold": self.sold,
            "category": self.category,
        }
        return product__json

class Star(db.Model):
    __tablename__ = 'stars'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = relationship('User', backref=backref("stars", cascade="all, delete"))
    product_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    product = relationship('Product', backref=backref("stars", cascade="all, delete"))
    amount = db.Column(db.String(1), nullable=False)

    def json(self):
        star__json = {
            "id": self.id,
            "author_id": self.author_id,
            "product_id": self.product_id,
            "amount": self.amount,
        }
        return star__json


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = relationship('User', backref=backref("comments", cascade="all, delete"))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = relationship('Post', backref=backref("comments", cascade="all, delete"))
    description = db.Column(db.String(280), nullable=False)

    def json(self):
        comment__json = {
            "id": self.id,
            "description": self.description,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
        return comment__json
