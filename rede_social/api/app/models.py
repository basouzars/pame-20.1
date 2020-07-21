from .extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, default=0)
    activated = db.Column(db.Boolean, default=False)

    def json(self):
        user__json = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
        }
        return user__json

    # def validate_email(self):
    #     return not db.session.query(exists().where(User.email==self.email)).scalar()