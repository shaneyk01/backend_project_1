from app.extensions import ma
from app.models import Ticket

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        include_relationships = False
        load_instance = True
        include_fk = True
        fields = ('id', 'date', 'customer_id', 'service_desc')
        dump_only = ('id', 'date')
        
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)