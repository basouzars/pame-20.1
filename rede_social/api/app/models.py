from .extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


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
    post = relationship("Post")
    post_likes = relationship("Post", secondary=postlike, backref="users")
    comment_likes = relationship("Comment", secondary=commentlike, backref="users")

    def json(self):
        user__json = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "post": self.post,
        }
        return user__json


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(280), nullable=False)
    comments = relationship("Comment", backref="posts")
    products = relationship("Product", uselist=False, backref="posts")

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


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    description = db.Column(db.String(280), nullable=False)

    def json(self):
        comment__json = {
            "id": self.id,
            "description": self.description,
            "author_id": self.author_id,
        }
        return comment__json
