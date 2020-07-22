from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db, mail
from ..models import Post, User, Comment


comment_api = Blueprint('comment_api', __name__)


@comment_api.route('/feed/<int:id>/comments', methods=['GET'])
def index(id):
    comments = Comment.query.filter_by(post_id=id)
    return jsonify([comment.json() for comment in comments]), 200


@comment_api.route('/feed/<int:id>', methods=['POST'])
@jwt_required
def create(id):
    data = request.json
    current_user = get_jwt_identity()

    author_id = User.query.filter_by(email=current_user).first()
    description = data.get('description')
    
    if not description:
        return {'error': 'Dados insuficientes'}, 400

    comment = Comment(author_id=author_id.id, post_id=id, description=description)

    db.session.add(comment)
    db.session.commit()
    
    return comment.json(), 201



@comment_api.route('/feed/<int:id_post>/<int:id_comment>', methods=['DELETE'])
@jwt_required
def delete(id_post,id_comment):
    current_user = get_jwt_identity()
    comment = Comment.query.get_or_404(id_comment)

    if comment.author.email == current_user or comment.post.author.email == current_user:
        db.session.delete(comment)
        db.session.commit()
        return {}, 204
    
    return {"error": "Não foi possível deletar a commentagem"}, 400

