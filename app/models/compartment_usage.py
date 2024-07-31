from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .. import db
from flask import session

class CompartmentUsage(db.Model):
    __tablename__ = 'compartment_usage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    open_time = Column(DateTime, nullable=False)
    close_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='compartment_usage', lazy=True)
    compartment_id = Column(Integer, ForeignKey('compartment.id'), nullable=False)
    compartments = relationship('Compartment', back_populates='compartment_usage', lazy=True)

    def __init__(self, id_user, id_compartment, open_time, close_time):
        self.user_id = id_user
        self.compartment_id = id_compartment
        self.open_time = open_time
        self.close_time = close_time
    
    def get_id(self):
        return str(self.id)