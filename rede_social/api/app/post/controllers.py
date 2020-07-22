from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from ..extensions import db, mail
from ..models import Post, User


post_api = Blueprint('post_api', __name__)


@post_api.route('/feed', methods=['GET'])
def index():
    posts = Post.query.options(joinedload(Post.comments)).all()
    return dict(Feed=[dict(c.json(), comments=[i.json() for i in c.comments]) for c in posts]), 200


@post_api.route('/feed/<int:id>', methods=['GET'])
def show_one(id):
    post = Post.query.get_or_404(id)
    return post.json(), 200


@post_api.route('/feed', methods=['POST'])
@jwt_required
def create():
    data = request.json
    current_user = get_jwt_identity()

    author_id = User.query.filter_by(email=current_user).first()
    description = data.get('description')
    if not description:
        return {'error': 'Dados insuficientes'}, 400

    post = Post(author_id=author_id.id, description=description)

    db.session.add(post)
    db.session.commit()
    
    return post.json(), 201


@post_api.route('/feed/<int:id>', methods=['DELETE'])
@jwt_required
def delete(id):
    current_user = get_jwt_identity()
    post = Post.query.get_or_404(id)

    if post.author.email == current_user:
        db.session.delete(post)
        db.session.commit()
        return {}, 204
    
    return {"error": "Não foi possível deletar a postagem"}, 400

