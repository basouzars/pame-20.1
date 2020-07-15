from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data-dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False


db = SQLAlchemy(app)


def get_user_info(data):
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    return name, email, age


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, default=0)

    def json(self):
        user__json = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
        }
        return user__json


@app.route('/users/', methods=['GET'])
def index():
    data = request.args
    age = data.get('age')

    if not age:
        users = User.query.all()

    else:
        age = age.split('-')

        if len(age) == 1:
            users = User.query.filter_by(age=age[0])
        
        else:
            users = User.query.filter(db.and_(User.age>=age[0], User.age<=age[1]))

    return jsonify([user.json() for user in users]), 200


@app.route('/users', methods=['POST'])
def create():
    data = request.json

    name, email, age = get_user_info(data)

    if not name or not email:
        return {'error': 'Dados insuficientes'}, 400

    user = User(name=name, email=email, age=age)

    db.session.add(user)
    db.session.commit()

    return user.json(), 200


@app.route('/users', methods=['DELETE'])
def delete_all():
    try:
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
    except:
        return {'error': 'Erro ao deletar usuarios'}, 400

    return {'ok': True}, 200


@app.route('/users', methods=['PUT'])
def replace():
    data = request.json

    id = data.get('id')
    name, email, age = get_user_info(data)

    if not name or not email or not id:
        return {'error': 'Dados insuficientes'}, 400

    user = User.query.get_or_404(id)
    user.name = name
    user.email = email
    user.age = age
    
    db.session.add(user)
    db.session.commit()
    
    return {'ok': True}, 200


@app.route('/users', methods=['PATCH'])
def update():
    data = request.json

    id = data.get('id')
    if not id:
        return {'error': 'Usuário não informado'}, 400

    user = User.query.get_or_404(id)

    name, email, age = get_user_info(data)

    if name:
        user.name = name
    if email:
        user.email = email
    if age:
        user.age = age

    db.session.add(user)
    db.session.commit()

    return {'ok': True}, 200


@app.route('/users/<int:id>', methods=['GET'])
def user_detail(id):
    if request.method == 'GET':
        user = User.query.get_or_404(id)
        return user.json(), 200


if __name__ == '__main__':
    app.run(debug=True)
