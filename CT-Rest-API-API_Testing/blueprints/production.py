from flask import Blueprint, jsonify, request
from models import db, Production
from app import limiter

production_bp = Blueprint('production_bp', __name__)

@production_bp.route('', methods=['POST'])
@limiter.limit("10/minute")
def create_production():
    data = request.get_json()
    new_production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(new_production)
    db.session.commit()
    return jsonify({'message': 'Production record created successfully'}), 201

@production_bp.route('', methods=['GET'])
@limiter.limit("15/minute")
def get_productions():
    productions = Production.query.all()
    result = [{'id': prod.id, 'product_id': prod.product_id, 'quantity_produced': prod.quantity_produced, 'date_produced': prod.date_produced} for prod in productions]
    return jsonify(result), 200
