from flask import Blueprint, jsonify, request
from models import db, Customer
from app import limiter

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('', methods=['POST'])
@limiter.limit("10/minute")
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@customer_bp.route('', methods=['GET'])
@limiter.limit("15/minute")
def get_customers():
    customers = Customer.query.all()
    result = [{'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone} for cust in customers]
    return jsonify(result), 200
