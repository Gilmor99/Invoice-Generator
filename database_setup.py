# Database Configuration file using SQLAlchemy
import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

""" Table Class """
Base = declarative_base()

# Each class represent Table
# Each Column Represent field within the table


class Account(Base):
    """ Account Table """
    __tablename__ = 'account'

    # Columns ####
    id = Column(Integer, primary_key=True)
    company = Column(String(250), nullable=False)
    address = Column(String(80))
    city = Column(String(80))
    state = Column(String(2))
    zipcode = Column(String(5))
    tel = Column(String(10))
    fax = Column(String(10))

    @property
    def serialize(self):
        """Return Account data in easily serializeable format"""
        return {
            'company': self.company,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'tel': self.tel,
            'fax': self.fax,
            'id': self.id
        }


class Invoice(Base):
    """ Invoice Table """
    __tablename__ = 'invoice'

    # Columns ####
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    fromName = Column(String(80), nullable=False)
    billTo = Column(String(250), nullable=False)
    date = Column(String(8))
    paymentTerms = Column(String(6))
    dueDate = Column(String(8))
    balanceDue = Column(Integer)
    subTotal = Column(Integer)
    taxFlag = Column(String(1))
    tax = Column(Integer)
    discountFlag = Column(String(1))
    discount = Column(Integer)
    shipping = Column(Integer)
    total = Column(Integer)
    amountPaid = Column(Integer)
    account_id = Column(Integer, ForeignKey('account.id'))
    company = relationship(Account)
    toAddress = Column(String(80))
    toCity = Column(String(80))
    toState = Column(String(2))
    toZipcode = Column(String(5))
    toTel = Column(String(10))
    toFax = Column(String(10))

    @property
    def serialize(self):
        """Return Invoice data in easily serializeable format"""
        return {
            'id': self.id,
            'number': self.number,
            'fromName': self.fromName,
            'billTo': self.billTo,
            'date': self.date,
            'total': self.total,
            'amountPaid': self.amountPaid,
            'balanceDue': self.balanceDue
        }


class InvoiceLine(Base):
    """ Invoice line Table """
    __tablename__ = 'invoice_line'

    #  Columns ####
    id = Column(Integer, primary_key=True)
    description = Column(String(80), nullable=False)
    quantity = Column(Integer)
    rate = Column(Integer)
    amount = Column(Integer)
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    account_id = Column(Integer, ForeignKey('account.id'))

    @property
    def serialize(self):
        """Return Invoice Line data in easily serializeable format"""
        return {
            'id': self.id,
            'description': self.description,
            'quantity': self.quantity,
            'rate': self.rate,
            'amount': self.amount,
        }

# Create the DB ################


# engine = create_engine('sqlite:///invoices.db')
engine = engine = create_engine('postgresql://invoice:invoice@localhost/invoice')

Base.metadata.create_all(engine)
