from flask import Blueprint, jsonify, request
from models import db, Employee
from app import limiter

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('', methods=['POST'])
@limiter.limit("10/minute")
def create_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully'}), 201

@employee_bp.route('', methods=['GET'])
@limiter.limit("15/minute")
def get_employees():
    employees = Employee.query.all()
    result = [{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees]
    return jsonify(result), 200
