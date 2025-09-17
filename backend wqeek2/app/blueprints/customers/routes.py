from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer
from app.extensions import db
from . import customers_bp



@customers_bp.route('', methods=["POST"])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # Check for existing customer
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    
    if existing_customer:
        return jsonify({"error": "Customer email already has account"}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()     
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/', methods = ['GET'])
def get_customers():
        query  = select(Customer)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200

@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer)
    return jsonify({"error": "Customer not found"}), 404

@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    try:        
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key,value in customer_data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200   

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'error':'Customer noy found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer {customer_id} deleted successfully'}), 200