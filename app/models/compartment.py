from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .. import db

class Compartment(db.Model):
    __tablename__ = 'compartment'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(Integer, nullable=False)
    locker_id = Column(Integer, ForeignKey('locker.id'), nullable=False)

    locker = relationship('Lockers', back_populates='compartments', lazy='select')
    compartment_usage = relationship("CompartmentUsage", back_populates='compartments', lazy=True)
    locker_schedules = relationship("LockerSchedules", back_populates='compartment', lazy=True)

    
    __table_args__ = (
        UniqueConstraint('locker_id', 'number', name='unique_locker_number'),
    )
    def __init__(self, locker_id, number):
        self.locker_id = locker_id
        self.number = number

    def get_number(self):
        return self.number
    
    def get_id(self):
        return str(self.id)