
from .extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from sqlalchemy import ForeignKey, Date
from datetime import date as date_type




ticket_mechanic = db.Table(
    "ticket_mechanic",
    db.Column("ticket_id",ForeignKey("tickets.id")),
    db.Column("mechanic_id",ForeignKey("mechanics.id"))
    )

class Customer(Base):
    __tablename__ = 'customers'
    id : Mapped[int] = mapped_column(primary_key=True)
    name :Mapped[str] = mapped_column(db.String(255), nullable=False)
    email : Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone : Mapped[str] = mapped_column(db.String(20), nullable=False)

    tickets : Mapped[List['Ticket']] = db.relationship(back_populates='customer')



class Mechanic(Base):
    __tablename__ = 'mechanics'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(db.String(255), nullable=False)
    email : Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    salary : Mapped[float] = mapped_column(db.Float(20), nullable=False)
    password : Mapped[str] = mapped_column(db.String(255), nullable=False)

    tickets : Mapped[List['Ticket']] = db.relationship(secondary=ticket_mechanic, back_populates='mechanics')


class Ticket(Base):
    __tablename__ = 'tickets'
    id : Mapped[int] = mapped_column(primary_key=True)
    date : Mapped[date_type] = mapped_column(Date, default=date_type.today)
    customer_id : Mapped[int] = mapped_column(ForeignKey('customers.id'),nullable=False)
    service_desc : Mapped[str] = mapped_column(db.String(500))
    
    customer : Mapped['Customer'] = db.relationship(back_populates='tickets')
    mechanics : Mapped[List['Mechanic']] = db.relationship(secondary=ticket_mechanic, back_populates='tickets')

