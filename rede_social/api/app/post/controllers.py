from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db, mail
from ..models import Post, User


post_api = Blueprint('post_api', __name__)


@post_api.route('/feed', methods=['GET'])
def index():
    posts = Post.query.all()
    return jsonify([post.json() for post in posts]), 200


@post_api.route('/feed', methods=['POST'])
@jwt_required
def create():
    data = request.json
    current_user = get_jwt_identity()

    author_id = User.query.filter_by(email=current_user).first()
    description = data.get('description')
    
    print(author_id)
    print(description)
    
    if not description:
        return {'error': 'Dados insuficientes'}, 400

    post = Post(author_id=author_id.id, description=description)

    db.session.add(post)
    db.session.commit()
    
    return post.json(), 201


# @user_api.route('/users/<int:id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
# @jwt_required
# def user_detail(id):
#     user = User.query.get_or_404(id)
#     validate_access(user)
#     data = request.json


#     if request.method == 'GET':
#         return user.json(), 200


#     if request.method == 'DELETE':
#         db.session.delete(user)
#         db.session.commit()
#         return {}, 204


#     if request.method == 'PUT':
#         if not data:
#             return {'error': 'Requisição precisa de body'}, 400

#         name = data.get('name')
#         email = data.get('email')
#         age = data.get('age')
#         password = data.get('password')
#         if password:
#             password = password.encode()

#         if not name or not email or not password:
#             return {'error': 'Dados insuficientes'}, 400

#         if email != user.email and not validate_email(email):
#             return {'error': 'Email já cadastrado'}, 400

#         user = User.query.get_or_404(id)
#         user.name = name
#         user.email = email
#         user.age = age
#         user.password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

#         db.session.add(user)
#         db.session.commit()

#         return user.json(), 200
    

#     if request.method == 'PATCH':
#         if not data:
#             return {'error': 'Requisição precisa de body'}, 400
        
#         user.name = data.get('name', user.name)
#         if not user.name:
#             return {'error': 'Nome inválido'}, 400

#         email = data.get('email')
#         if not validate_email(email) and email != user.email:
#             return {'error': 'Email já cadastrado'}, 400
        
#         user.email = data.get('email', user.email)
#         if not user.email:
#             return {'error': 'Email inválido'}, 400

#         user.age = data.get('age', user.age)
#         if not isinstance(user.age, int):
#             return {'error': 'Idade deve ser um número'}, 400

#         password = data.get('password')
#         if password:
#             user.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

#         db.session.add(user)
#         db.session.commit()

#         return user.json(), 200


# @user_api.route('/login', methods=['POST'])
# def login():
#     if not request.is_json:
#         return jsonify({"error": "JSON não enviado"}), 400

#     data = request.json
    
#     email = data.get('email')
#     password = data.get('password')

#     if not email:
#         return jsonify({"error": "E-mail não enviado"}), 400
#     if not password:
#         return jsonify({"error": "Senha não enviada"}), 400

#     user = User.query.filter_by(email=email).first()

#     if not user or not bcrypt.checkpw(password.encode(), user.password_hash):
#         return jsonify({"error": "E-mail ou senha inválidos"}), 401

#     access_token = create_access_token(identity=email)
#     return jsonify(access_token=access_token), 200
