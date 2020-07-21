from flask import Blueprint
from sqlalchemy import exists
from flask import request, jsonify
from flask_mail import Message
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ..extensions import db, mail
from ..models import User
import bcrypt


user_api = Blueprint('user_api', __name__)


def validate_email(email):
    return not db.session.query(exists().where(User.email==email)).scalar()


def validate_access(user):
    current_user = get_jwt_identity()
    if user.email != current_user:
        return {"error": "Acesso negado"}, 401


@user_api.route('/users/', methods=['GET'])
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


@user_api.route('/users', methods=['POST'])
def create():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    password = data.get('password')
    if password:
        password = password.encode()

    if not name or not email or not password:
        return {'error': 'Dados insuficientes'}, 406

    if not validate_email(email):
        return {'error': 'Email já cadastrado'}, 406

    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(name=name, email=email, age=age, password_hash=password_hash)

    db.session.add(user)
    db.session.commit()
    
    # msg = Message(
    #     sender='brunoasouza@poli.ufrj.br',
    #     recipients=[email],
    #     subject='Bem Vindo!',
    #     body=f'Olá {name}'
    # )
    # mail.send(msg)
    
    return user.json(), 201


@user_api.route('/users/<int:id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
@jwt_required
def user_detail(id):
    user = User.query.get_or_404(id)
    validate_access(user)
    data = request.json


    if request.method == 'GET':
        return user.json(), 200


    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {}, 204


    if request.method == 'PUT':
        if not data:
            return {'error': 'Requisição precisa de body'}, 400

        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        password = data.get('password')
        if password:
            password = password.encode()

        if not name or not email or not password:
            return {'error': 'Dados insuficientes'}, 400

        if email != user.email and not validate_email(email):
            return {'error': 'Email já cadastrado'}, 400

        user = User.query.get_or_404(id)
        user.name = name
        user.email = email
        user.age = age
        user.password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

        db.session.add(user)
        db.session.commit()

        return user.json(), 200
    

    if request.method == 'PATCH':
        if not data:
            return {'error': 'Requisição precisa de body'}, 400
        
        user.name = data.get('name', user.name)
        if not user.name:
            return {'error': 'Nome inválido'}, 400

        email = data.get('email')
        if not validate_email(email) and email != user.email:
            return {'error': 'Email já cadastrado'}, 400
        
        user.email = data.get('email', user.email)
        if not user.email:
            return {'error': 'Email inválido'}, 400

        user.age = data.get('age', user.age)
        if not isinstance(user.age, int):
            return {'error': 'Idade deve ser um número'}, 400

        password = data.get('password')
        if password:
            user.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        db.session.add(user)
        db.session.commit()

        return user.json(), 200


@user_api.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "JSON não enviado"}), 400

    data = request.json
    
    email = data.get('email')
    password = data.get('password')

    if not email:
        return jsonify({"error": "E-mail não enviado"}), 400
    if not password:
        return jsonify({"error": "Senha não enviada"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.checkpw(password.encode(), user.password_hash):
        return jsonify({"error": "E-mail ou senha inválidos"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
