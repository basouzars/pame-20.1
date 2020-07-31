from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User, Product


product_api = Blueprint('product_api', __name__)


@product_api.route('/market', methods=['POST'])
@jwt_required
def create():
    data = request.json
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if not user.admin:
        return {'error': 'Não tem permissão'}, 400

    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    if not name or not price or not stock:
        return {'error': 'Dados insuficientes'}, 400

    product = Product(name=name, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()
    
    return {}, 201


@product_api.route('/market/<int:id>', methods=['DELETE'])
@jwt_required
def delete(id):
    current_user = get_jwt_identity()
    product = Post.query.get_or_404(id)
    user = User.query.filter_by(email=current_user).first()

    if user.admin:
        db.session.delete(product)
        db.session.commit()
        return {}, 204
    
    return {"error": "Não foi possível deletar a productagem"}, 400

