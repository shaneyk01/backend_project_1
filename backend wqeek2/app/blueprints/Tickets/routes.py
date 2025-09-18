from .schemas import ticket_schema, tickets_schema
from flask import request ,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Ticket, Mechanic, ticket_mechanic, db
from . import tickets_bp
from app.blueprints.mechanics.schemas import mechanic_schema   


@tickets_bp.route('/', methods=['POST'])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_ticket = Ticket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

@tickets_bp.route('/', methods = ['GET'])
def get_tickets():
        query  = select(Ticket)
        tickets = db.session.execute(query).scalars().all()
        return tickets_schema.jsonify(tickets), 200
    
    
@tickets_bp.route('/<int:ticket_id>/add-mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if ticket and mechanic:
        if mechanic not in ticket_mechanic:
            ticket_mechanic.append(mechanic)
    db.session.commit()
    
    return jsonify({
        'message': 'Successfully added mechanic to ticket',
        'ticket': ticket_schema.dump(ticket),
        'mechanic': mechanic_schema.dump(mechanic)
    }), 200

@tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if ticket and mechanic:
        if mechanic in ticket_mechanic:
            ticket_mechanic.remove(mechanic)
            db.session.commit()
            return jsonify({
                'message': 'successfully removed mechanic from ticket',
                'ticket': ticket_schema.dump(ticket),
                'mechanic': mechanic_schema.dump(mechanic)
        }), 200
        return jsonify({'error': 'This Mechanic is not assigned to this ticket'}), 404
    return jsonify({'error': 'invalid mechanic_id or ticket_id'}), 404