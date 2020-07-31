from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User, Product, Order


order_api = Blueprint('order_api', __name__)


@order_api.route('/orders', methods=['POST'])
@jwt_required
def create():
    data = request.json
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    amount = data.get('amount')
    address = data.get('address')
    date = data.get('date')
    product = data.get('product')
    if not amount or not address or not date or not product:
        return {'error': 'Dados insuficientes'}, 400

    product = Product.query.get_or_404(product)

    order = Order(customer_id=user.id, product_id=product.id, address=address, amount=amount, date=date)

    db.session.add(order)
    db.session.commit()
    
    return {}, 201

