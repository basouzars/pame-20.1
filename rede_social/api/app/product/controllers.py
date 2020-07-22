from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from ..extensions import db, mail
from ..models import Post, User, Product


product_api = Blueprint('product_api', __name__)


@product_api.route('/market', methods=['GET'])
def index():
    posts = Post.query.options(joinedload(Post.comments)).filter_by(products=not [])
    return dict(Market=[dict(c.json(), comments=[i.json() for i in c.comments]) for c in posts]), 200


@product_api.route('/market/<category>', methods=['GET'])
def category(category):
    posts = Post.query.options(joinedload(Post.comments)).join(Post.products).filter_by(Product.category==category)
    return dict(Market=[dict(c.json(), comments=[i.json() for i in c.comments]) for c in posts]), 200


@product_api.route('/market/<int:id>', methods=['GET'])
def show_one(id):
    product = Post.query.get_or_404(id)
    return product.json(), 200


@product_api.route('/market', methods=['POST'])
@jwt_required
def create():
    data = request.json
    current_user = get_jwt_identity()

    author_id = User.query.filter_by(email=current_user).first()
    description = data.get('description')
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    category = data.get('category')
    if not description or not name or not price or not stock or not category:
        return {'error': 'Dados insuficientes'}, 400

    post = Post(author_id=author_id.id, description=description)
    db.session.add(post)
    db.session.commit()

    product = Product(post_id=post.id, name=name, price=price, stock=stock, category=category)
    db.session.add(product)
    db.session.commit()

    
    return product.json(), 201


@product_api.route('/market/<int:id>', methods=['DELETE'])
@jwt_required
def delete(id):
    current_user = get_jwt_identity()
    product = Post.query.get_or_404(id)

    if product.author.email == current_user:
        db.session.delete(product)
        db.session.commit()
        return {}, 204
    
    return {"error": "Não foi possível deletar a productagem"}, 400

